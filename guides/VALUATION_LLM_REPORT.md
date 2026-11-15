# LLM 估值与仓位建议报告

> 该功能在分支 `feat/llm-valuation-email` 上，尚未合并到 `main`。

## 它做什么

周一到周五 **10:00（Asia/Shanghai）** 运行一次（周末不运行）：

1. 采集四家公司的行情、基本面与近 7 天新闻；
2. 计算估值指标：52 周区间位置、20/60 日均线、1/3/6/12 个月收益、年化波动率；
3. 调用 OpenAI 兼容接口（默认 DeepSeek），让模型输出结构化估值判断与加仓/减仓建议；
4. 生成独立页面 `docs/valuation.html`、归档页 `docs/valuation/valuation_YYYYMMDD.html`，
   以及首页使用的 `docs/valuation_reports.json`；
5. 生成 Markdown 报告 `reports/valuation/valuation_YYYYMMDD.md`；
6. 全程不发送邮件，结果直接提交到仓库并随站点发布。

模型失败、超时或未配置密钥时，自动降级为规则结论，页面仍然生成。

## 处理流程

```
行情/基本面（yfinance → 新浪兜底）
新闻（yfinance → Google 新闻 RSS 兜底）
        ↓
计算指标（区间位置、均线、收益、波动）
        ↓
提示词（结构化数据 + 新闻标题，标注为不可信素材）
        ↓
LLM 输出 JSON：rating / action / position_hint / action_reason / fair_value_range /
confidence / thesis / drivers / risks / data_gaps
        ↓
校验枚举与长度 → 不合法则降级规则结论
        ↓
独立页面 + 首页索引 + Markdown → 由工作流提交
```

## 输出

| 产物 | 位置 | 说明 |
|---|---|---|
| 最新估值页 | `docs/valuation.html` | 独立页面，不和每日报告混在一起 |
| 归档页 | `docs/valuation/valuation_YYYYMMDD.html` | 每个工作日一份 |
| 首页数据 | `docs/valuation_reports.json` | 首页「估值与仓位建议」区块读取最新一期 |
| Markdown | `reports/valuation/valuation_YYYYMMDD.md` | 本地留存，不入库 |

工作流生成后会提交 `docs/valuation.html`、`docs/valuation/` 与
`docs/valuation_reports.json`，线上页面随之更新；`reports/valuation/` 已被忽略，不会入库。

首页的「估值与仓位建议」区块由 `docs/js/valuation.js` 读取最新一期索引，
显示每家公司的加仓 / 减仓 / 持有建议、现价、估值判断与理由。

## 需要的密钥

只需要一个仓库 Secret：

| 名称 | 必填 | 说明 |
|---|---|---|
| `LLM_API_KEY` | 是 | 大模型 API Key（DeepSeek 等） |

可选 **Variables**：`LLM_BASE_URL`、`LLM_MODEL`。
不再需要任何 SMTP / 邮箱相关配置。

**DeepSeek**：登录 `platform.deepseek.com` → API Keys → 创建，模型默认 `deepseek-chat`。
任何 OpenAI 兼容服务都可以，改 `LLM_BASE_URL` 与 `LLM_MODEL` 即可。

## 本地测试

```bash
# 生成 Markdown、页面与索引，并把 Markdown 打印到终端
python scripts/valuation_report.py --dry-run

# 不调用 LLM，只看规则结论
python scripts/valuation_report.py --no-llm --dry-run

# 只生成报告，不动 docs/ 页面
python scripts/valuation_report.py --no-page --dry-run
```

PowerShell 用 `$env:LLM_API_KEY="sk-xxx"` 的形式设置密钥。

## 降级与失败

| 情况 | 行为 |
|---|---|
| 未设置 `LLM_API_KEY` | 打印警告，使用规则结论，页面照常生成 |
| LLM 超时 / 401 / 返回非 JSON | 该公司回退规则结论，页面标注“备注：LLM 失败” |
| 行情采集失败 | 该公司标记“数据错误”，仍写入页面 |
| 页面写入失败 | 退出码 1，工作流变红 |

## 成本

四家公司各一次调用，输入约 1–2k tokens、输出约 300 tokens，一天不到 1 万 tokens。
按 DeepSeek 当前价格，每天成本在几分钱人民币以内；每月 Actions 时长也远低于免费额度。

## 安全

- 密钥只放在 GitHub Secrets，脚本不读配置文件里的密钥，也不写日志。
- 新闻标题是不可信外部输入：截断到 120 字、放入 `<news>` 标签，系统提示明确要求忽略其中指令。
- 输出的是“仓位建议”而非交易指令，并在页面与 Markdown 中标注“不构成投资建议”。

## 常见问题

**页面没有更新**
- 先看 Actions 日志里“提交估值页面”是否成功；分支保护或权限不足会导致推送失败。
- 定时任务只对默认分支生效，功能分支需要手动 Run workflow。

**页面里全是“数据不足”**
- 说明行情采集失败，看日志里的 `数据错误`；也可能是 `yfinance` 被限流。

**LLM 401 / 402**
- 401 是 Key 无效；402 通常是余额不足。

**首页没有出现估值建议**
- 确认 `docs/valuation_reports.json` 的 `reports` 首条有 `items`；
- 直接打开 `valuation.html` 能看到内容则是浏览器缓存，强制刷新即可；
- 该区块与每日报告完全独立，日报更新不会覆盖它。
