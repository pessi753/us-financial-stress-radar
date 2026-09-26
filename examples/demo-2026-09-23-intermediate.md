# 【模拟数据 / DEMO，非市场实况】 US Financial Stress Radar / 美国金融压力雷达

观察截止日：2026-09-23；生成时间：2026-09-23T06:18:51.495691+00:00；模式：intermediate

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

## 跨市场解释与历史参照

OAS 是调整债券期权条款后的额外风险补偿；Z-score 表示偏离自身历史均值的标准差数，非正态分布时不能换算概率；percentile 是历史排序位置。
CCC-BB 扩大说明信用分层加剧；HY-BBB 扩大说明非投资级相对承压。差距收窄也可能因为较强一端恶化，必须同时看两端。
信用、隔夜资金与银行指标共同异常比多个重叠信用指数更有说服力。NFCI/STLFSI含有重叠成分，不单独计为独立确认。

### SOFR minus EFFR / 抵押借钱与银行隔夜拆借的利率差
Secured Overnight Financing Rate minus Effective Federal Funds Rate, same observation date.
关注：与另一项隔夜利率差、企业融资和银行借款共同观察；留意季末。 限制：并非纯粹的银行信用风险价差；两市场参与者、抵押和交易结构不同。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 4.99；P90 5.26。
- COVID_2020 压力方向极值：5.29（2020-03-11）
- Banking_2023 压力方向极值：5.31（2023-05-16）
来源：[SOFR](https://fred.stlouisfed.org/series/SOFR)、[EFFR](https://fred.stlouisfed.org/series/EFFR)

### SOFR minus IORB / 市场隔夜融资与央行付息的利率差
SOFR minus Interest Rate on Reserve Balances, matched observation dates.
关注：与准备金下降、央行借款上升是否同时出现。 限制：非银行机构不能直接获得准备金利息；套利受限；政策利率调整可造成跳变。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 0.00；P90 0.00。
- COVID_2020 压力方向极值：0.00（2020-02-03）
- Banking_2023 压力方向极值：0.00（2023-03-01）
来源：[SOFR](https://fred.stlouisfed.org/series/SOFR)、[IORB](https://fred.stlouisfed.org/series/IORB)

### BBB OAS / 较稳健企业的额外融资补偿
ICE BofA BBB OAS; option-adjusted spread to a Treasury spot curve.
关注：由最弱企业、整体高风险企业到较稳健企业是否共同扩大，并与资金和银行指标核对。 限制：既含违约补偿也含流动性和风险偏好；指数成分会变；2026年4月起FRED仅保留约三年，历史不足不补造。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 1.30；P90 1.37。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB)

### HY OAS / 高风险企业的额外融资补偿
ICE BofA HY OAS; option-adjusted spread to a Treasury spot curve.
关注：由最弱企业、整体高风险企业到较稳健企业是否共同扩大，并与资金和银行指标核对。 限制：既含违约补偿也含流动性和风险偏好；指数成分会变；2026年4月起FRED仅保留约三年，历史不足不补造。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 3.81；P90 4.02。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)

### BB OAS / 高风险组中较强企业的融资补偿
ICE BofA BB OAS; option-adjusted spread to a Treasury spot curve.
关注：由最弱企业、整体高风险企业到较稳健企业是否共同扩大，并与资金和银行指标核对。 限制：既含违约补偿也含流动性和风险偏好；指数成分会变；2026年4月起FRED仅保留约三年，历史不足不补造。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 2.39；P90 2.52。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A1HYBB](https://fred.stlouisfed.org/series/BAMLH0A1HYBB)

### B OAS / 高风险组中较弱企业的融资补偿
ICE BofA B OAS; option-adjusted spread to a Treasury spot curve.
关注：由最弱企业、整体高风险企业到较稳健企业是否共同扩大，并与资金和银行指标核对。 限制：既含违约补偿也含流动性和风险偏好；指数成分会变；2026年4月起FRED仅保留约三年，历史不足不补造。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 4.11；P90 4.33。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A2HYB](https://fred.stlouisfed.org/series/BAMLH0A2HYB)

### CCC & Lower OAS / 最脆弱企业的额外融资补偿
ICE BofA CCC & Lower OAS; option-adjusted spread to a Treasury spot curve.
关注：由最弱企业、整体高风险企业到较稳健企业是否共同扩大，并与资金和银行指标核对。 限制：既含违约补偿也含流动性和风险偏好；指数成分会变；2026年4月起FRED仅保留约三年，历史不足不补造。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 8.52；P90 8.98。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC)

### CCC minus BB OAS / 最弱与较强高风险企业的融资差距
CCC-and-lower OAS minus BB OAS.
关注：同时检查两端的绝对水平和变化。 限制：派生指标与原始利差高度重叠，降低权重。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 611.49；P90 644.72。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A3HYC](https://fred.stlouisfed.org/series/BAMLH0A3HYC)、[BAMLH0A1HYBB](https://fred.stlouisfed.org/series/BAMLH0A1HYBB)

### HY minus BBB OAS / 高风险与投资级企业的融资差距
HY OAS minus BBB OAS.
关注：若较稳健企业也扩大，压力可能更广。 限制：重叠指数不是独立证据，不能重复计数为跨市场确认。
近三年可得水平历史：n=781；2023-09-25 至 2026-09-22；中位数 250.61；P90 264.39。
- COVID_2020 压力方向极值：N/A（历史覆盖不足）
- Banking_2023 压力方向极值：N/A（历史覆盖不足）
来源：[BAMLH0A0HYM2](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)、[BAMLC0A4CBBB](https://fred.stlouisfed.org/series/BAMLC0A4CBBB)

### Discount Window: Primary Credit / 银行向央行借的主要应急贷款
Federal Reserve primary credit outstanding, Wednesday level, NSA.
关注：与存款流失、准备金及隔夜融资异常核对。 限制：只覆盖主要信贷，不含全部贴现窗口或紧急设施；政策鼓励使用、污名效应都会影响。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 3,492.67；P90 3,678.12。
- COVID_2020 压力方向极值：3,702.28（2020-03-11）
- Banking_2023 压力方向极值：3,713.57（2023-05-17）
来源：[WLCFLPCL](https://fred.stlouisfed.org/series/WLCFLPCL)

### Reserve Balances / 银行放在央行的准备金
Reserve balances with Federal Reserve Banks, weekly average, NSA.
关注：四周下降同时伴随短期借钱变贵才更值得关注。 限制：缩表、财政账户及季节性影响很大；总量不能揭示分布；评分用四周增速。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 3,430,992.63；P90 3,581,810.75。
- COVID_2020 压力方向极值：3,313,051.44（2020-02-05）
- Banking_2023 压力方向极值：3,438,310.26（2023-03-22）
来源：[WRESBAL](https://fred.stlouisfed.org/series/WRESBAL)

### Commercial Bank Deposits / 商业银行存款
All commercial bank deposits, weekly, seasonally adjusted.
关注：持续四周收缩并伴随央行借款增加。 限制：系统总量掩盖银行间迁移；季调数据会修订；四周增速评分，不直接给规模评分。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 19,299.33；P90 20,147.69。
- COVID_2020 压力方向极值：18,635.91（2020-02-05）
- Banking_2023 压力方向极值：19,340.50（2023-03-22）
来源：[DPSACBW027SBOG](https://fred.stlouisfed.org/series/DPSACBW027SBOG)

### Commercial Bank Credit / 商业银行信贷资产
All commercial banks bank credit, weekly, seasonally adjusted; securities plus loans and leases.
关注：与存款下降、信用融资变贵共同观察。 限制：含证券；供给与需求难区分；四周增速评分存在经济周期误报。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 19,835.43；P90 20,707.34。
- COVID_2020 压力方向极值：19,153.58（2020-02-05）
- Banking_2023 压力方向极值：19,877.73（2023-03-22）
来源：[TOTBKCR](https://fred.stlouisfed.org/series/TOTBKCR)

### VIX / 美股未来波动预期
Cboe VIX daily close, option-implied 30-day volatility.
关注：与企业融资补偿扩大和短期融资异常核对。 限制：并非股市跌幅预测，也不是危机概率；单日事件可推升。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 18.95；P90 19.98。
- COVID_2020 压力方向极值：20.10（2020-03-11）
- Banking_2023 压力方向极值：20.16（2023-05-16）
来源：[VIXCLS](https://fred.stlouisfed.org/series/VIXCLS)

### NFCI / 全美金融条件指数
Chicago Fed National Financial Conditions Index.
关注：观察是否与企业和银行指标一致。 限制：成分与本雷达重叠，不作为独立市场确认；历史值会修订。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 -0.30；P90 -0.26。
- COVID_2020 压力方向极值：-0.25（2020-03-11）
- Banking_2023 压力方向极值：-0.25（2023-05-17）
来源：[NFCI](https://fred.stlouisfed.org/series/NFCI)

### STLFSI4 / 圣路易斯金融压力指数
St. Louis Fed Financial Stress Index, version 4.
关注：与波动预期、企业融资和银行指标交叉检查。 限制：与其他指标有重叠；版本不同不拼接；修订可能改变历史。
近三年可得水平历史：n=156；2023-09-20 至 2026-09-16；中位数 -0.20；P90 -0.16。
- COVID_2020 压力方向极值：-0.15（2020-03-11）
- Banking_2023 压力方向极值：-0.15（2023-05-17）
来源：[STLFSI4](https://fred.stlouisfed.org/series/STLFSI4)

### 2s10s / 十年与两年国债利率差
10-year Treasury yield minus shorter maturity Treasury yield.
关注：倒挂后快速转正且信用压力上升时，不能因转正就解除警报。 限制：宏观背景指标；评分只刻画倒挂深度的相对位置，不是即时资金压力或衰退概率。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 0.20；P90 0.24。
- COVID_2020 压力方向极值：0.22（2020-06-30）
- Banking_2023 压力方向极值：0.22（2023-03-20）
来源：[T10Y2Y](https://fred.stlouisfed.org/series/T10Y2Y)

### 3m10y / 十年与三个月国债利率差
10-year Treasury yield minus shorter maturity Treasury yield.
关注：倒挂后快速转正且信用压力上升时，不能因转正就解除警报。 限制：宏观背景指标；评分只刻画倒挂深度的相对位置，不是即时资金压力或衰退概率。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 -0.10；P90 -0.06。
- COVID_2020 压力方向极值：-0.08（2020-06-30）
- Banking_2023 压力方向极值：-0.08（2023-03-20）
来源：[T10Y3M](https://fred.stlouisfed.org/series/T10Y3M)

### 10Y Real Yield / 十年期扣除通胀因素后的国债收益率
10-year constant-maturity inflation-indexed Treasury yield.
关注：快速上升与企业融资补偿扩大是否共振。 限制：不是个人贷款实际利率；还含流动性与期限溢价；低值未必安全。
近三年可得水平历史：n=782；2023-09-22 至 2026-09-22；中位数 1.70；P90 1.79。
- COVID_2020 压力方向极值：1.80（2020-03-11）
- Banking_2023 压力方向极值：1.80（2023-05-16）
来源：[DFII10](https://fred.stlouisfed.org/series/DFII10)

方法：启发式分位评分，未经危机预测回测校准。50/75/90 为关注/压力/严重门槛；数据缺失不按零分处理。
缺失、过期和备用缓存不参与评分。原始日期与抓取时间见配套 JSON；历史修订及来源授权条款请参阅使用说明。
