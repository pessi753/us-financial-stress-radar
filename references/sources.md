# 官方数据来源与接口

核对日期：2026-09-23。完整逐指标链接保存在 registry.json。

- [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html)：JSON观测、日期、分页、vintage参数；本实现单序列v1，检查截断，不静默丢分页。
- [FRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html)：历史修订与数据可得性口径。
- [FRED API keys](https://fred.stlouisfed.org/docs/api/api_key.html)：环境变量提供应用自己的key。
- [NY Fed SOFR](https://www.newyorkfed.org/markets/reference-rates/sofr)：通常纽约时间工作日约08:00发布前一工作日利率，可能有修订。
- [NY Fed Markets Data APIs](https://markets.newyorkfed.org/static/docs/markets-api.html)：预留直连接口参考；需核对effectiveDate/百分数单位/发布与修订时间。
- [Federal Reserve H.4.1](https://www.federalreserve.gov/releases/h41/)：主要信贷、准备金；主要信贷使用周三余额，准备金使用周均值，不混同。
- [Federal Reserve H.8](https://www.federalreserve.gov/releases/h8/)：季调商业银行存款与银行信贷，后者包括证券及贷款租赁，不是新增贷款额。
- [Fed FRED User Guide](https://www.federalreserve.gov/data/ddp-fred-user-guide.htm)：DDP到FRED映射与官方数据访问说明。
- [ICE HY OAS系列说明](https://fred.stlouisfed.org/series/BAMLH0A0HYM2)：相对国债即期曲线的期权调整利差；2026年4月后约三年可得历史及版权条款。
- [NFCI](https://fred.stlouisfed.org/series/NFCI)、[STLFSI4](https://fred.stlouisfed.org/series/STLFSI4)：周频金融条件/压力指数，不拼接其他版本。

## 数据源接口

`scripts/providers.py` 中 `fetch(series_id,start,as_of)` 返回 `[{'date':'YYYY-MM-DD','value':'4.25'}, ...]`，数值为该序列官方原生单位。错误抛出不含密钥的 ProviderError。

FRED适配器已实现。NYFedProvider、FederalReserveProvider为显式未实现的扩展接口，调用会报错；它们不是已经可用的备用源。实现新源时须提供单位/频率/日期映射，标注实际来源、抓取时间及修订能力，并新增接口验收后接入路由。不得无声替换为名称相似的不同序列。
