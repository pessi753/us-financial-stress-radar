---
name: us-financial-stress-radar
description: 运行美国金融压力雷达，监测美元融资、信用分层、银行、市场和宏观利率，生成每日晚间 beginner/intermediate/veteran 三种报告。适用于美国金融风险监测、压力日报和跨市场风险扩散检查。
---

# US Financial Stress Radar / 美国金融压力雷达

## 执行

1. 确定模式：默认 `beginner`；用户说进阶选 `intermediate`；老油条/专业压缩选 `veteran`。沿用本次会话已选择的模式。
2. 用可用的 Python 3.10+ 执行本目录 `scripts/radar.py --mode <mode> --output-dir <用户报告目录>`。脚本仅用标准库；相对路径以实际 Skill 目录解析。FRED_API_KEY 从环境读取，勿打印、写入报告或向用户索要明文密钥。
3. 阅读生成的 Markdown 和配套 JSON，先报告压力读数、有效覆盖、日期和跨市场确认，再按模式给内容。若退出码 2，报告已生成但总体证据不足；退出码 1 是配置/执行失败，排除故障后重跑。
4. `beginner` 对全部指标保留：是什么、为什么看、涨跌含义、当前含义、观察项、注意事项。避免直接抛出未解释的缩写；进阶保留完整数据和历史比较；老油条采用紧凑表格及 cross-asset confirmation、信用分层。

## 数据和判断边界

- 没有密钥时说明真实运行未完成，指导用户在本机设置环境变量。只有明确请求演示或验收时才用 `--fixture examples/synthetic-input.json`；标为模拟数据，不能当日报。
- 每个指标显示实际观测日期。中国晚间通常尚未到当日美国收盘；只称“最新已发布”。不要暗示所有市场已同步更新。
- D 是日频有效工作日观测步数；周频 D 必须 N/A，另报 W。不前填缺值，不把无更新说成变化为零。缺失和过期不代表正常。
- 只称 Financial Stress Score，不解释为金融危机发生概率。规则为启发式历史分位、非预测模型；局部与系统性判断依据脚本的独立模块确认。
- CCC→HY→BBB→Funding→Banks 是观察路径。单次共现不能证明时间先后或因果；NFCI、STLFSI和信用子指数不可重复计作独立跨市场证据。
- 数值由脚本计算；解释根据 `registry.json`，不自行编造数字、危机参照或因果。对技术性季末、政策改变、曲线转正等保留替代解释。
- 历史查询使用日期 vintage，不能声称日内历史可得性回测。官方修订和 ICE 三年数据限制见方法说明。

## 文件导航

- [README.md](README.md)：密钥配置、命令、每晚运行和安装。
- [registry.json](registry.json)：19个中英双语指标、源链接、频率、单位与评分参数。扩展指标时先核对官方口径。
- [references/methodology.md](references/methodology.md)：分数、缺数、时间和传导逻辑；用户询问专业口径时阅读。
- [references/sources.md](references/sources.md)：官方来源和保留接口。NY Fed/Federal Reserve 直连接口仅预留，未实现自动回退。
- [examples/](examples/)：三模式模拟样例与可复现输入。

用户每天手动调用即可；本 Skill 不自动创建定时任务。用户另行明确要求自动运行时再配置时间、环境和报告位置。
