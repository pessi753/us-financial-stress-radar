# US Financial Stress Radar / 美国金融压力雷达

19 个指标、5 个模块、三种报告模式。Python 3.10+，无需安装第三方依赖。每次输出 Markdown + JSON，数据来自 FRED 官方 API；模拟示例不使用真实市场数据。

## 安装和配置

把整个 `us-financial-stress-radar` 文件夹放进 `$CODEX_HOME/skills/`（未设置时为用户目录下的 `.codex/skills/`），刷新技能列表或重启应用后使用。不要只复制 SKILL.md。

在 [FRED API Keys](https://fred.stlouisfed.org/docs/api/api_key.html) 申请自己的密钥，并在本机环境配置 `FRED_API_KEY`。不要把密钥粘进聊天、脚本、截图或版本库。

PowerShell 可使用以下隐藏输入设置当前窗口的环境变量；关闭窗口后失效，计划任务需要单独配置其运行账户环境：

```powershell
$radarSecret = Read-Host 'FRED API Key' -AsSecureString
$env:FRED_API_KEY = [System.Net.NetworkCredential]::new('', $radarSecret).Password
```

macOS / Linux 当前 shell：

```bash
read -r -s -p 'FRED API Key: ' FRED_API_KEY
export FRED_API_KEY
```

Python 应在 PATH；若没有，把命令里的 `python` 替换为 Python 可执行文件绝对路径。Codex 可使用宿主提供的 Python。

## 每晚使用

直接对 Codex 说：

- “用美国金融压力雷达，跑今晚的小白版。”
- “用 us-financial-stress-radar，intermediate 模式。”
- “跑今晚的老油条版，重点看信用分层和跨市场确认。”

或者在 Skill 目录运行：

```bash
python scripts/radar.py --mode beginner
python scripts/radar.py --mode intermediate
python scripts/radar.py --mode veteran
```

默认小白模式，输出到当前目录 `radar-reports/`，缓存到 `radar-data/cache/`。文件名含数据截止日与模式，同日同模式再次运行会更新对应报告；需要保存多次快照时，为每次运行指定不同 `--output-dir`。

中国晚间 21:00–23:00 可手动运行一次，获取彼时最新已发布数据；当日美国市场可能尚未收盘。脚本不自动调度，也不创建后台任务。周末仍可运行，但金融市场日度数据可能没有新观测。

```bash
python scripts/radar.py --mode intermediate --as-of 2026-09-23 --output-dir reports/2026-09-23
```

`--as-of` 默认 UTC 日期；中国晚间与 UTC 通常是同一个日期。FRED 按该日 vintage 获取截至该日的观测，日内时点无法重现。默认请求历史从 2019-01-01 起，用于 2020/2023 对比；可用 `--history-start` 修改。历史不足时不会填造参照值。

## 模式区别

|模式|适合谁|内容|
|---|---|---|
|beginner|金融小白|概览 + 19 张中文解释卡；涨跌含义、当前判断、注意事项|
|intermediate|有一定基础|完整数值表、OAS/bp/Z/P、跨市场联动、各指标历史比较和来源|
|veteran|熟悉市场|压缩 level/delta/Z/P/score 表、周频补表、credit ladder 与 confirmation|

模式只改变表达，不改变评分；JSON 总是保留完整结果。

## 离线演示和验收

```bash
python scripts/make_demo.py
python scripts/radar.py --fixture examples/synthetic-input.json --as-of 2026-09-23 --mode beginner --output-dir examples
python scripts/radar.py --fixture examples/synthetic-input.json --as-of 2026-09-23 --mode intermediate --output-dir examples
python scripts/radar.py --fixture examples/synthetic-input.json --as-of 2026-09-23 --mode veteran --output-dir examples
python -m unittest discover -s tests -v
```

示例文件标题和 JSON 都标注模拟。没有密钥时真实命令失败，绝不自动改用模拟数据。验收覆盖日期对齐、单位换算、周频、缺失/陈旧、缓存、零方差、增长评分、历史覆盖和跨市场确认；网络接口测试用模拟响应，不代表已经通过真实密钥联调。

## 数据问题和退出码

- `0`：生成可计算总分的报告；仍应阅读覆盖率与局部数据问题。
- `1`：密钥缺失、参数错误或文件/执行故障。
- `2`：报告生成，但关键模块或覆盖率不足，总分 N/A。
- 网络请求每序列最多尝试三次，单次超时 25 秒；400/401/403 等不会重复重试。大量序列网络失败可能需要数分钟。
- 默认失败即缺失。可加 `--allow-cache` 使用同一截止日缓存，明确标注并排除评分；不从其他 vintage 偷换数据。
- 配套 JSON 存观测日、源、抓取时间、历史样本数和覆盖率；缓存保留响应观测，不保存 API key。

评分及边界见 [methodology](references/methodology.md)。官方接口见 [sources](references/sources.md)。真实 ICE 数据涉及再分发限制，默认用于自己的监测；所交付示例为人工模拟。
