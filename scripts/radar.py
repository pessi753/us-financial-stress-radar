#!/usr/bin/env python3
"""US Financial Stress Radar. Python 3.10+, standard library only."""
import argparse
import bisect
import json
import math
import os
from pathlib import Path
import statistics
import sys
from datetime import date, datetime, timedelta, timezone

from providers import FredProvider, ProviderError

ROOT = Path(__file__).resolve().parents[1]
HORIZONS = (1, 5, 20, 60)
UNITS = {'percent': '%', 'bp': '基点', 'million_USD': '百万美元', 'billion_USD': '十亿美元', 'index': '点'}
CATEGORY_CN = {'Funding': '短期资金周转', 'Credit': '企业融资', 'Banking': '银行体系', 'Market': '市场情绪与金融条件', 'Macro': '宏观利率背景'}
LEVEL_CN = {'normal': '常态区间', 'watch': '值得关注', 'stress': '压力较高', 'severe': '压力很高', 'unknown': '无法判断'}


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    tmp.replace(path)


def clean(rows, as_of, daily=False):
    """Do not fill missing values. Drop weekends only for daily analysis."""
    data, rejected = {}, 0
    for row in rows:
        try:
            d = date.fromisoformat(row['date'])
            x = float(row['value'])
            if not math.isfinite(x) or d > as_of or (daily and d.weekday() > 4):
                rejected += 1
                continue
            data[d] = x  # duplicate date: last observation wins
        except (ValueError, TypeError, KeyError):
            rejected += 1
    return sorted(data.items()), rejected


def combine(ind, raw, as_of):
    parts = [dict(clean(raw.get(sid, []), as_of, ind['frequency'] == 'daily')[0]) for sid in ind['components']]
    if len(parts) == 1:
        return sorted(parts[0].items())
    # Exact-date join avoids manufacturing spreads with mismatched observations.
    return [(d, (parts[0][d] - parts[1][d]) * 100) for d in sorted(parts[0].keys() & parts[1].keys())]


def percentile(values, current):
    if not values:
        return None
    return 100 * (sum(x < current for x in values) + .5 * sum(x == current for x in values)) / len(values)


def quantile(values, fraction):
    s = sorted(values)
    if not s:
        return None
    i = (len(s) - 1) * fraction
    lo = int(i)
    return s[lo] + (s[min(lo+1, len(s)-1)] - s[lo]) * (i-lo)


def level(score, thresholds):
    if score is None:
        return 'unknown'
    return next(k for k in ('severe', 'stress', 'watch', 'normal') if score >= thresholds[k])


def delta(data, steps, factor=1, weekly=False):
    if len(data) <= steps:
        return None
    elapsed = (data[-1][0] - data[-steps-1][0]).days
    # Reject major gaps instead of calling months-apart readings "1D".
    if elapsed > (steps * 7 + 3 if weekly else math.ceil(steps * 7 / 5) + 5):
        return None
    return (data[-1][1] - data[-steps-1][1]) * factor


def stress_series(ind, data):
    if ind['stress_transform'] == 'level':
        return [(d, x * ind['stress_direction']) for d, x in data]
    out = []
    for i in range(4, len(data)):
        d, x = data[i]
        prev_d, prev = data[i-4]
        if prev != 0 and 25 <= (d-prev_d).days <= 31:
            out.append((d, (x/prev - 1) * 100 * ind['stress_direction']))
    return out


def historical(data, start, end, weekly, direction):
    window = [(d, x) for d, x in data if start <= d <= end]
    expected = (end-start).days / (7 if weekly else 7/5)
    # Never label a partial tail as the full episode's worst reading.
    if len(window) < .8 * expected or not window or (window[0][0]-start).days > 10 or (end-window[-1][0]).days > 10:
        return {'status': 'unavailable', 'value': None}
    d, x = max(window, key=lambda row: direction * row[1])
    return {'status': 'available', 'value': x, 'date': str(d)}


def metrics(ind, data, as_of, thresholds, cached=False):
    out = dict(id=ind['id'], status='missing', observation_date=None, current=None,
               deltas={f'{h}D': None for h in HORIZONS}, weekly_deltas={}, z_score=None,
               percentile=None, score=None, stress_level='unknown', trend='unknown',
               worsening=False, cached=cached, history_n=0)
    if not data:
        return out
    d, x = data[-1]
    weekly = ind['frequency'] == 'weekly'
    factor = 100 if ind['unit'] == 'percent' else 1
    out.update(observation_date=str(d), current=x, age_days=(as_of-d).days,
               status='stale' if (as_of-d).days > ind['stale_after_calendar_days'] else ('cached' if cached else 'ok'))
    if weekly:
        out['weekly_deltas'] = {f'{n}W': delta(data, n, factor, True) for n in (1, 4, 13)}
    else:
        out['deltas'] = {f'{h}D': delta(data, h, factor) for h in HORIZONS}
    baseline = [v for day, v in data if d - timedelta(days=1096) <= day < d]
    out.update(history_n=len(baseline), history_start=str(next(day for day, v in data if day >= d-timedelta(days=1096))),
               history_end=str(d), median_3y=quantile(baseline, .5), p90_3y=quantile(baseline, .9))
    if len(baseline) >= ind['minimum_history']:
        sd = statistics.stdev(baseline)
        out.update(z_score=(x-statistics.mean(baseline))/sd if sd > 1e-12 else None,
                   percentile=percentile(baseline, x))
    ss = stress_series(ind, data)
    sb = [v for day, v in ss if d-timedelta(days=1096) <= day < d]
    sv = ss[-1][1] if ss and ss[-1][0] == d else None
    out['stress_feature'] = sv
    out['stress_feature_unit'] = '4W growth %, direction-adjusted' if ind['stress_transform']=='growth4w' else 'direction-adjusted level'
    valid_history = len(sb) >= ind['minimum_history']
    if valid_history and sv is not None and out['status'] == 'ok':
        out['score'] = percentile(sb, sv)
    out['stress_level'] = level(out['score'], thresholds)
    lag = 4 if weekly else 20
    sdelt = delta(ss, lag, weekly=weekly)
    epsilon = ind['trend_epsilon']
    if sdelt is not None:
        out['trend'] = '↑' if sdelt > epsilon else ('↓' if sdelt < -epsilon else '→')
        out['worsening'] = sdelt > epsilon
    out['history_sufficient'] = valid_history
    out['historical'] = {
        'COVID_2020': historical(data, date(2020,2,1), date(2020,6,30), weekly, ind['stress_direction']),
        'Banking_2023': historical(data, date(2023,3,1), date(2023,5,31), weekly, ind['stress_direction'])}
    return out


def aggregate(reg, rows):
    byid = {r['id']: r for r in rows}
    modules, coverages = {}, {}
    for category in reg['weights']:
        members = [i for i in reg['indicators'] if i['category'] == category]
        available = [i for i in members if byid[i['id']]['score'] is not None]
        w = sum(i['weight'] for i in available)
        coverages[category] = w / sum(i['weight'] for i in members)
        modules[category] = sum(byid[i['id']]['score'] * i['weight'] for i in available) / w if w and coverages[category] >= .5 else None
    # Preserve fixed module weights; no renormalization across missing modules.
    coverage = sum(reg['weights'][k]*coverages[k] for k in modules)
    score = sum(reg['weights'][k]*modules[k] for k in modules) if all(v is not None for v in modules.values()) and coverage >= .8 else None

    def active(id):
        r = byid[id]
        return None if r['score'] is None else r['score'] >= 75 and r['worsening']

    def at_least(ids, n):
        values = [active(id) for id in ids]
        yes, unknown = values.count(True), values.count(None)
        return True if yes >= n else (False if yes + unknown < n else None)

    signals = {'Funding': at_least(['sofr_effr','sofr_iorb'],2),
               'Credit': at_least(['hy','bbb'],2),
               'Banking': at_least(['discount_window','reserves','deposits','bank_credit'],2),
               'Market': active('vix')}
    count = sum(v is True for v in signals.values())
    if signals['Funding'] is True and signals['Banking'] is True and signals['Credit'] is True:
        confirmation = 'systemic_pressure_confirmation'
    elif count >= 2:
        confirmation = 'cross_market_pressure'
    elif any(v is None for v in signals.values()):
        confirmation = 'insufficient_confirmation_data'
    elif count == 1:
        confirmation = 'localized_pressure'
    else:
        confirmation = 'not_confirmed'
    chain = {'CCC': active('ccc'), 'HY': active('hy'), 'BBB': active('bbb'),
             'Funding': signals['Funding'], 'Banks': signals['Banking']}
    # Mixed daily/weekly observations cannot establish a causal sequence.
    return dict(financial_stress_score=score, stress_level=level(score,reg['thresholds']),
                modules=modules, coverage=coverage, module_coverage=coverages,
                confirmation=confirmation, confirmation_signals=signals, transmission_chain=chain,
                transmission_caveat='这是不同更新频率下的共现核对，不证明风险沿箭头先后传播或存在因果关系。')


CONFIRM_CN = {
 'systemic_pressure_confirmation':'企业融资、短期资金与银行指标同时异常，出现系统性压力的交叉证据；这不是危机预测。',
 'cross_market_pressure':'至少两个市场同时给出压力信号，需要继续观察是否扩散至银行和短期资金。',
 'localized_pressure':'目前仅一个市场满足联合异常规则，更多表现为局部压力。',
 'not_confirmed':'尚未满足多市场共同恶化规则；这不能保证没有风险，也可能已有高位压力但未继续恶化。',
 'insufficient_confirmation_data':'关键确认数据不足，暂时不能判断压力是否广泛扩散。'}


def fmt(value):
    return 'N/A' if value is None else f'{value:,.2f}'


def render(report, reg, mode):
    s = report['summary']
    prefix = '【模拟数据 / DEMO，非市场实况】' if report['demo'] else ''
    lines = [f'# {prefix} US Financial Stress Radar / 美国金融压力雷达', '',
             f"观察截止日：{report['as_of']}；生成时间：{report['generated_at_utc']}；模式：{mode}", '',
             f"Financial Stress Score：**{fmt(s['financial_stress_score'])} / 100**；{LEVEL_CN[s['stress_level']]}；有效覆盖：{s['coverage']:.0%}。",
             '这是相对历史的压力读数，不是金融危机发生概率。', '', CONFIRM_CN[s['confirmation']], '',
             '中国晚间运行看到的是各指标最新已发布数据，不等于当日美股收盘。周度数据不伪装成日度变化。', '']
    for cat, val in s['modules'].items():
        label = CATEGORY_CN[cat] if mode == 'beginner' else cat
        lines.append(f"- {label}：{fmt(val)} / 100（有效覆盖 {s['module_coverage'][cat]:.0%}）")
    chain_labels = {'CCC':'最脆弱企业','HY':'整体高风险企业','BBB':'较稳健企业','Funding':'短期资金','Banks':'银行'}
    lines += ['', '风险传导核对：' + ' → '.join((chain_labels[k] if mode == 'beginner' else k)+('：异常且恶化' if v is True else '：未知' if v is None else '：未满足') for k,v in s['transmission_chain'].items()),
              s['transmission_caveat'], '']
    ranked = sorted((r for r in report['indicators'] if r['score'] is not None), key=lambda r:r['score'],reverse=True)[:3]
    names = {i['id']:i for i in reg['indicators']}
    lines.append('优先复核：' + ('；'.join(names[r['id']]['name_cn']+'（'+LEVEL_CN[r['stress_level']]+'）' for r in ranked) or '数据不足'))
    if report['errors']:
        lines += ['', '数据问题：' + '；'.join(f'{k}: {v}' for k,v in report['errors'].items())]
    if mode != 'beginner':
        lines += ['', 'D=有效工作日观测步数，排除周末，不跨大段缺口；% 利率的 delta 换算为 bp（100bp=1个百分点）。',
                  '周频 D 列为 N/A，另报 1W/4W/13W。Z/P 使用截至该指标观测日、排除当前值的近三年可得水平历史。',
                  'Score 是压力方向调整后的分位；准备金/存款/信贷使用四周增速，所以不等于水平 P。', '',
                  '|指标|Level|日期 / 状态|1D|5D|20D|60D|Z|P|Score / 趋势|',
                  '|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
        for r in report['indicators']:
            i = names[r['id']]
            lines.append(f"|{i['name_en']}|{fmt(r['current'])} {i['unit']}|{r['observation_date']} / {r['status']}|"+
                         '|'.join(fmt(r['deltas'][f'{h}D']) for h in HORIZONS)+
                         f"|{fmt(r['z_score'])}|{fmt(r['percentile'])}|{fmt(r['score'])} {r['trend']}|")
        lines += ['', '周频增量（保持原始单位）：']
        for r in report['indicators']:
            if r['weekly_deltas']:
                lines.append(f"- {names[r['id']]['name_en']}：" + ' / '.join(k+' '+fmt(v) for k,v in r['weekly_deltas'].items()))
    if mode == 'beginner':
        lines += ['', '读数单位：1个基点等于0.01个百分点；例如借钱利率从4.00%升到4.10%，就是增加10个基点。']
        for r in report['indicators']:
            i = names[r['id']]
            date_text = r['observation_date'] or '未知'
            movement = {'↑':'压力方向正在上升','↓':'压力方向正在缓和','→':'压力方向变化不明显','unknown':'缺少足够数据判断趋势'}[r['trend']]
            status = {'ok':'已获取','stale':'数据过期','missing':'缺失','cached':'备用缓存，不计入评分'}[r['status']]
            change = r['weekly_deltas'].get('4W') if i['frequency']=='weekly' else r['deltas']['20D']
            change_label = '较四个周观测前' if i['frequency']=='weekly' else '较二十个有效日观测前'
            lines += ['', f"## {i['name_cn']}", '', f"当前：{fmt(r['current'])} {UNITS[i['unit']]}；数据日：{date_text}；{status}。",
                      f"近期变化：{change_label}，{'数据不足' if change is None else ('增加' if change>0 else '减少' if change<0 else '持平')+' '+fmt(abs(change))+' '+UNITS[i['delta_unit']]}。",
                      f"是什么：{i['beginner_explanation']}", f"为什么看：{i['why_watch']}",
                      f"上涨意味着：{i['higher_means']}", f"下跌意味着：{i['lower_means']}",
                      f"当前含义：{LEVEL_CN[r['stress_level']]}；{movement}。这个判断只反映已取得的数据。",
                      f"接下来观察：{i['watch_for']}", f"注意：{i['limitations']}",
                      '数据来源：' + '、'.join(f'[{sid}]({url})' for sid,url in zip(i['components'],i['source_urls']))]
    elif mode == 'intermediate':
        lines += ['', '## 跨市场解释与历史参照', '',
                  'OAS 是调整债券期权条款后的额外风险补偿；Z-score 表示偏离自身历史均值的标准差数，非正态分布时不能换算概率；percentile 是历史排序位置。',
                  'CCC-BB 扩大说明信用分层加剧；HY-BBB 扩大说明非投资级相对承压。差距收窄也可能因为较强一端恶化，必须同时看两端。',
                  '信用、隔夜资金与银行指标共同异常比多个重叠信用指数更有说服力。NFCI/STLFSI含有重叠成分，不单独计为独立确认。']
        for r in report['indicators']:
            i = names[r['id']]
            lines += ['', f"### {i['name_en']} / {i['name_cn']}", i['definition'],
                      f"关注：{i['watch_for']} 限制：{i['limitations']}",
                      f"近三年可得水平历史：n={r['history_n']}；{r.get('history_start','N/A')} 至 {r.get('history_end','N/A')}；中位数 {fmt(r.get('median_3y'))}；P90 {fmt(r.get('p90_3y'))}。"]
            for episode, comp in r.get('historical',{}).items():
                lines.append(f"- {episode} 压力方向极值：{fmt(comp['value'])}（{comp.get('date','历史覆盖不足')}）")
            lines.append('来源：'+'、'.join(f'[{sid}]({url})' for sid,url in zip(i['components'],i['source_urls'])))
    else:
        lines += ['', f"Cross-asset confirmation: {s['confirmation']}; " + ', '.join(f'{k}={v}' for k,v in s['confirmation_signals'].items()),
                  'Credit ladder: CCC → HY → BBB; verify both legs of CCC-BB / HY-BBB. Funding/Banks confirmation is co-occurrence, not inferred causality.',
                  'Calibration: trailing available 3Y, min n D126/W52; level Z/P, growth4W score for reserves/deposits/credit; no forward fill. Full provenance/history in JSON + registry.']
    lines += ['', '方法：启发式分位评分，未经危机预测回测校准。50/75/90 为关注/压力/严重门槛；数据缺失不按零分处理。',
              '缺失、过期和备用缓存不参与评分。原始日期与抓取时间见配套 JSON；历史修订及来源授权条款请参阅使用说明。', '']
    return '\n'.join(lines)


def run(args):
    reg = read_json(args.registry)
    as_of = date.fromisoformat(args.as_of)
    if as_of > datetime.now(timezone.utc).date():
        raise ValueError('as-of cannot be in the future')
    fetched = datetime.now(timezone.utc).isoformat()
    sids = sorted({sid for i in reg['indicators'] for sid in i['components']})
    raw, provenance, errors, cached_ids = {}, {}, {}, set()
    demo = bool(args.fixture)
    if demo:
        fixture = read_json(args.fixture)
        if fixture.get('synthetic') is not True:
            raise ValueError('fixture must explicitly declare synthetic=true; use FRED for live data')
        raw = fixture['series']
        provenance = {sid:{'source':'synthetic_fixture','retrieved_at':fetched} for sid in sids}
    else:
        key = os.environ.get('FRED_API_KEY')
        if not key:
            raise ValueError('FRED_API_KEY is not configured; live run stopped. Demo requires explicit --fixture.')
        provider = FredProvider(key)
        for sid in sids:
            cache_path = Path(args.cache_dir)/as_of.isoformat()/(sid+'.json')
            try:
                raw[sid] = provider.fetch(sid,args.history_start,str(as_of))
                record = dict(source='FRED',series_id=sid,as_of=str(as_of),retrieved_at=fetched,observations=raw[sid])
                write_json(cache_path,record)
                provenance[sid] = {k:v for k,v in record.items() if k!='observations'}
            except ProviderError as exc:
                errors[sid] = str(exc)
                if args.allow_cache and cache_path.exists():
                    record = read_json(cache_path)
                    if record.get('as_of') == str(as_of) and record.get('series_id') == sid:
                        raw[sid] = record['observations']
                        provenance[sid] = {k:v for k,v in record.items() if k!='observations'}
                        cached_ids.add(sid)
    cleaning = {sid:clean(raw.get(sid,[]),as_of)[1] for sid in sids}
    rows = [metrics(i,combine(i,raw,as_of),as_of,reg['thresholds'],bool(set(i['components']) & cached_ids)) for i in reg['indicators']]
    report = dict(schema_version=1,methodology_version=reg['methodology_version'],demo=demo,
                  as_of=str(as_of),generated_at_utc=fetched,mode=args.mode,
                  provenance=provenance,cleaning_rejected=cleaning,errors=errors,
                  summary=aggregate(reg,rows),indicators=rows)
    out = Path(args.output_dir)
    out.mkdir(parents=True,exist_ok=True)
    tag = ('demo-' if demo else '')+str(as_of)+'-'+args.mode
    write_json(out/(tag+'.json'),report)
    (out/(tag+'.md')).write_text(render(report,reg,args.mode),encoding='utf-8')
    print(str((out/(tag+'.md')).resolve()))
    return 0 if report['summary']['financial_stress_score'] is not None else 2


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['beginner','intermediate','veteran'],default='beginner')
    p.add_argument('--as-of',default=str(datetime.now(timezone.utc).date()),help='UTC date default; requests FRED date vintage, not intraday replay')
    p.add_argument('--history-start',default='2019-01-01')
    p.add_argument('--registry',default=str(ROOT/'registry.json'))
    p.add_argument('--fixture',help='Explicit synthetic offline fixture only')
    p.add_argument('--cache-dir',default=str(Path.cwd()/'radar-data/cache'))
    p.add_argument('--allow-cache',action='store_true',help='Read same-vintage cache on provider failure; excluded from scoring')
    p.add_argument('--output-dir',default=str(Path.cwd()/'radar-reports'))
    args=p.parse_args()
    try:
        return run(args)
    except (ValueError,OSError,KeyError) as exc:
        print('Radar stopped: '+str(exc),file=sys.stderr)
        return 1


if __name__=='__main__':
    sys.exit(main())
