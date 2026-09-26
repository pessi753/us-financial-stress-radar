import copy
from datetime import date,timedelta
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import urllib.error

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import radar
from providers import FredProvider,ProviderError

REG=radar.read_json(ROOT/'registry.json')
BY={i['id']:i for i in REG['indicators']}

class RadarTests(unittest.TestCase):
    def test_registry_contract(self):
        self.assertEqual(len(BY),19)
        self.assertAlmostEqual(sum(REG['weights'].values()),1)
        for i in BY.values():
            for key in ('name_en','name_cn','source','components','definition','beginner_explanation','why_watch','higher_means','lower_means','watch_for','limitations'):
                self.assertTrue(i[key])

    def test_exact_date_join_and_bp(self):
        raw={'SOFR':[{'date':'2026-09-21','value':'4.2'},{'date':'2026-09-22','value':'4.3'}],
             'EFFR':[{'date':'2026-09-21','value':'4.1'}]}
        out=radar.combine(BY['sofr_effr'],raw,date(2026,9,23))
        self.assertEqual(len(out),1)
        self.assertAlmostEqual(out[0][1],10)
        self.assertAlmostEqual(radar.delta([(date(2026,9,21),4),(date(2026,9,22),4.67)],1,100),67)

    def test_missing_future_nan_and_weekend(self):
        rows=[{'date':'2026-09-21','value':'.'},{'date':'2026-09-22','value':'NaN'},
              {'date':'2026-10-01','value':'2'},{'date':'2026-09-19','value':'3'},
              {'date':'2026-09-18','value':'1'}]
        result,n=radar.clean(rows,date(2026,9,23),True)
        self.assertEqual(result,[(date(2026,9,18),1)])
        self.assertEqual(n,4)

    def test_weekly_is_not_daily(self):
        end=date(2026,9,16)
        data=[(end-timedelta(weeks=60-i),100+i) for i in range(61)]
        row=radar.metrics(BY['discount_window'],data,date(2026,9,23),REG['thresholds'])
        self.assertTrue(all(v is None for v in row['deltas'].values()))
        self.assertEqual(row['weekly_deltas']['4W'],4)
        self.assertEqual(row['score'],100)

    def test_stale_and_cache_excluded(self):
        end=date(2026,8,1)
        data=[(end-timedelta(days=200-i),i) for i in range(201)]
        row=radar.metrics(BY['vix'],data,date(2026,9,23),REG['thresholds'])
        self.assertIsNone(row['score'])
        self.assertEqual(row['status'],'stale')
        row=radar.metrics(BY['vix'],data,end,REG['thresholds'],cached=True)
        self.assertIsNone(row['score'])

    def test_flat_z_and_ties(self):
        end=date(2026,9,22)
        data=[(end-timedelta(days=200-i),4) for i in range(201)]
        row=radar.metrics(BY['vix'],data,date(2026,9,23),REG['thresholds'])
        self.assertIsNone(row['z_score'])
        self.assertEqual(row['percentile'],50)
        self.assertFalse(row['worsening'])

    def test_outlier_uses_past_only(self):
        self.assertEqual(radar.percentile([1,2,3],10),100)
        self.assertEqual(radar.percentile([1,2,3],0),0)

    def test_growth_scoring_not_balance_size(self):
        data=[(date(2025,1,1)+timedelta(weeks=i),100) for i in range(60)]
        data[-1]=(data[-1][0],90)
        row=radar.metrics(BY['deposits'],data,data[-1][0],REG['thresholds'])
        self.assertAlmostEqual(row['stress_feature'],10)
        self.assertEqual(row['score'],100)
        self.assertTrue(row['worsening'])

    def base_rows(self):
        return [dict(id=i['id'],score=20,worsening=False) for i in REG['indicators']]

    def test_confirmation_credit_overlap_not_independent(self):
        rows=self.base_rows()
        for r in rows:
            if r['id'] in ['ccc','hy','bbb','bb','b','ccc_bb','hy_bbb','nfci','stlfsi']:
                r.update(score=99,worsening=True)
        out=radar.aggregate(REG,rows)
        self.assertEqual(out['confirmation'],'localized_pressure')

    def test_systemic_confirmation(self):
        rows=self.base_rows()
        for r in rows:
            if r['id'] in ['hy','bbb','sofr_effr','sofr_iorb','deposits','discount_window']:
                r.update(score=99,worsening=True)
        self.assertEqual(radar.aggregate(REG,rows)['confirmation'],'systemic_pressure_confirmation')

    def test_missing_module_no_false_normal(self):
        rows=self.base_rows()
        for r in rows:
            if r['id'] in ['sofr_effr','sofr_iorb']:
                r['score']=None
        out=radar.aggregate(REG,rows)
        self.assertIsNone(out['financial_stress_score'])
        self.assertEqual(out['confirmation'],'insufficient_confirmation_data')

    def test_gaps_and_unavailable_crisis(self):
        self.assertIsNone(radar.delta([(date(2025,1,1),1),(date(2026,1,1),2)],1))
        out=radar.historical([(date(2023,5,31),1)],date(2023,3,1),date(2023,5,31),False,1)
        self.assertEqual(out['status'],'unavailable')

    def test_http_key_redaction(self):
        with patch('urllib.request.urlopen',side_effect=urllib.error.HTTPError('https://example/?api_key=SECRET',400,'SECRET',None,None)):
            with self.assertRaises(ProviderError) as caught:
                FredProvider('SECRET').fetch('VIXCLS','2020-01-01','2026-09-23')
        self.assertNotIn('SECRET',str(caught.exception))

    def test_retry_and_vintage_request(self):
        from io import StringIO
        payload=json.dumps({'observations':[],'count':0})
        with patch('urllib.request.urlopen',side_effect=[urllib.error.URLError('SECRET'),StringIO(payload)]) as urlopen, patch('time.sleep'):
            self.assertEqual(FredProvider('SECRET').fetch('VIXCLS','2020-01-01','2026-09-23'),[])
            url=urlopen.call_args[0][0].full_url
            self.assertIn('realtime_start=2026-09-23',url)
            self.assertIn('realtime_end=2026-09-23',url)

    def test_all_modes_same_score_and_demo_label(self):
        raw=radar.read_json(ROOT/'examples/synthetic-input.json')['series']
        asof=date(2026,9,23)
        rows=[radar.metrics(i,radar.combine(i,raw,asof),asof,REG['thresholds']) for i in REG['indicators']]
        report=dict(demo=True,as_of=str(asof),generated_at_utc='test',summary=radar.aggregate(REG,rows),indicators=rows,errors={})
        for mode in ['beginner','intermediate','veteran']:
            text=radar.render(report,REG,mode)
            self.assertIn('模拟数据',text)
            self.assertIn(radar.fmt(report['summary']['financial_stress_score']),text)
        beginner=radar.render(report,REG,'beginner')
        self.assertEqual(beginner.count('当前含义：'),19)

if __name__=='__main__':
    unittest.main()
