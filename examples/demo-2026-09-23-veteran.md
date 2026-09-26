# 【模拟数据 / DEMO，非市场实况】 US Financial Stress Radar / 美国金融压力雷达

观察截止日：2026-09-23；生成时间：2026-09-23T06:18:51.667362+00:00；模式：veteran

Financial Stress Score：**54.47 / 100**；值得关注；有效覆盖：100%。
这是相对历史的压力读数，不是金融危机发生概率。

目前仅一个市场满足联合异常规则，更多表现为局部压力。

中国晚间运行看到的是各指标最新已发布数据，不等于当日美股收盘。周度数据不伪装成日度变化。

- Funding：32.54 / 100（有效覆盖 100%）
- Credit：71.70 / 100（有效覆盖 100%）
- Banking：79.49 / 100（有效覆盖 100%）
- Market：18.44 / 100（有效覆盖 100%）
- Macro：61.64 / 100（有效覆盖 100%）

风险传导核对：CCC：异常且恶化 → HY：异常且恶化 → BBB：未满足 → Funding：未满足 → Banks：异常且恶化
这是不同更新频率下的共现核对，不证明风险沿箭头先后传播或存在因果关系。

优先复核：高风险企业的额外融资补偿（压力很高）；高风险组中较弱企业的融资补偿（压力很高）；最脆弱企业的额外融资补偿（压力很高）

D=有效工作日观测步数，排除周末，不跨大段缺口；% 利率的 delta 换算为 bp（100bp=1个百分点）。
周频 D 列为 N/A，另报 1W/4W/13W。Z/P 使用截至该指标观测日、排除当前值的近三年可得水平历史。
Score 是压力方向调整后的分位；准备金/存款/信贷使用四周增速，所以不等于水平 P。

|指标|Level|日期 / 状态|1D|5D|20D|60D|Z|P|Score / 趋势|
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
|SOFR minus EFFR|4.78 bp|2026-09-22 / ok|-0.01|-0.05|-0.21|-0.34|-1.21|15.09|15.09 →|
|SOFR minus IORB|0.00 bp|2026-09-22 / ok|0.00|0.00|0.00|0.00|N/A|50.00|50.00 →|
|BBB OAS|1.24 percent|2026-09-22 / ok|-0.15|-1.18|-5.56|-8.75|-1.21|15.11|15.11 ↓|
|HY OAS|4.39 percent|2026-09-22 / ok|1.08|7.20|26.30|50.42|3.59|100.00|100.00 ↑|
|BB OAS|2.29 percent|2026-09-22 / ok|-0.28|-2.17|-10.27|-16.16|-1.21|15.11|15.11 ↓|
|B OAS|4.74 percent|2026-09-22 / ok|1.17|7.77|28.38|54.40|3.59|100.00|100.00 ↑|
|CCC & Lower OAS|9.82 percent|2026-09-22 / ok|2.42|16.10|58.84|112.78|3.59|100.00|100.00 ↑|
|CCC minus BB OAS|752.86 bp|2026-09-22 / ok|2.70|18.28|69.11|128.94|4.84|100.00|100.00 ↑|
|HY minus BBB OAS|314.88 bp|2026-09-22 / ok|1.23|8.38|31.87|59.17|5.16|100.00|100.00 ↑|
|Discount Window: Primary Credit|3,370.97 million_USD|2026-09-16 / ok|N/A|N/A|N/A|N/A|-1.01|21.79|21.79 ↓|
|Reserve Balances|3,352,266.48 million_USD|2026-09-16 / ok|N/A|N/A|N/A|N/A|-0.52|34.62|98.72 ↑|
|Commercial Bank Deposits|18,856.50 billion_USD|2026-09-16 / ok|N/A|N/A|N/A|N/A|-0.52|34.62|98.72 ↑|
|Commercial Bank Credit|19,380.29 billion_USD|2026-09-16 / ok|N/A|N/A|N/A|N/A|-0.52|34.62|98.72 ↑|
|VIX|18.15 index|2026-09-22 / ok|-0.02|-0.17|-0.81|-1.28|-1.21|15.09|15.09 ↓|
|NFCI|-0.33 index|2026-09-16 / ok|N/A|N/A|N/A|N/A|-1.01|21.79|21.79 ↓|
|STLFSI4|-0.23 index|2026-09-16 / ok|N/A|N/A|N/A|N/A|-1.01|21.79|21.79 ↓|
|2s10s|0.16 percent|2026-09-22 / ok|-0.09|-0.72|-3.42|-5.39|-1.21|15.09|84.91 ↑|
|3m10y|-0.14 percent|2026-09-22 / ok|-0.09|-0.72|-3.42|-5.39|-1.21|15.09|84.91 ↑|
|10Y Real Yield|1.62 percent|2026-09-22 / ok|-0.20|-1.54|-7.27|-11.44|-1.21|15.09|15.09 ↓|

周频增量（保持原始单位）：
- Discount Window: Primary Credit：1W -37.26 / 4W -153.19 / 13W -219.33
- Reserve Balances：1W -33,392.38 / 4W -137,373.98 / 13W -191,796.83
- Commercial Bank Deposits：1W -187.83 / 4W -772.73 / 13W -1,078.86
- Commercial Bank Credit：1W -193.05 / 4W -794.19 / 13W -1,108.83
- NFCI：1W -0.01 / 4W -0.04 / 13W -0.05
- STLFSI4：1W -0.01 / 4W -0.04 / 13W -0.05

Cross-asset confirmation: localized_pressure; Funding=False, Credit=False, Banking=True, Market=False
Credit ladder: CCC → HY → BBB; verify both legs of CCC-BB / HY-BBB. Funding/Banks confirmation is co-occurrence, not inferred causality.
Calibration: trailing available 3Y, min n D126/W52; level Z/P, growth4W score for reserves/deposits/credit; no forward fill. Full provenance/history in JSON + registry.

方法：启发式分位评分，未经危机预测回测校准。50/75/90 为关注/压力/严重门槛；数据缺失不按零分处理。
缺失、过期和备用缓存不参与评分。原始日期与抓取时间见配套 JSON；历史修订及来源授权条款请参阅使用说明。
