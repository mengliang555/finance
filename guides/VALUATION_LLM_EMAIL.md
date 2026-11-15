# LLM 估值分析与邮件日报

> 该功能在分支 `feat/llm-valuation-email` 上，尚未合并到 `main`。

## 它做什么

周一到周五 **10:00（Asia/Shanghai）** 运行一次（周末不运行）：

1. 采集四家公司的行情、基本面与近 7 天新闻；
2. 计算估值指标：52 周区间位置、20/60 日均线、1/3/6/12 个月收益、年化波动率；
3. 调用 OpenAI 兼容接口（默认 DeepSeek），让模型输出结构化估值判断与加仓/减仓建议；
4. 生成独立页面 `docs/valuation.html`、归档页 `docs/valuation/valuation_YYYYMMDD.html`，
   以及首页使用的 `docs/valuation_reports.json`；
5. 生成 Markdown 报告（`reports/valuation/valuation_YYYYMMDD.md`）和 HTML 邮件；
6. 通过 SMTP 发送到你的邮箱。

模型失败、超时或未配置密钥时，自动降级为规则结论，邮件照常发送但不含 LLM 判断。

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
独立页面 + 首页索引 → 由工作流提交
Markdown + HTML 邮件 → SMTP 发送
```

## 输出

| 产物 | 位置 | 说明 |
|---|---|---|
| 最新估值页 | `docs/valuation.html` | 独立页面，不和每日报告混在一起 |
| 归档页 | `docs/valuation/valuation_YYYYMMDD.html` | 每个工作日一份 |
| 首页数据 | `docs/valuation_reports.json` | 首页「估值与仓位建议」区块读取最新一期 |
| Markdown | `reports/valuation/valuation_YYYYMMDD.md` | 本地留存，不入库 |
| 邮件 | 你的邮箱 | 含评级、加仓/减仓建议、理由与风险 |

工作流生成后会提交 `docs/valuation.html`、`docs/valuation/` 与
`docs/valuation_reports.json`，线上页面随之更新；`reports/valuation/` 已被忽略，不会入库。

首页的「估值与仓位建议」区块由 `docs/js/valuation.js` 读取最新一期索引，
显示每家公司的加仓 / 减仓 / 持有建议、现价、估值判断与理由。

## 需要的 Secrets

在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中添加：

| 名称 | 必填 | 说明 |
|---|---|---|
| `LLM_API_KEY` | 是 | 大模型 API Key（DeepSeek 等） |
| `SMTP_HOST` | 是 | 如 `smtp.qq.com`、`smtp.163.com`、`smtp.gmail.com` |
| `SMTP_USER` | 是 | SMTP 账号，通常是完整邮箱地址 |
| `SMTP_PASSWORD` | 是 | SMTP 授权码，**不是**登录密码 |
| `SMTP_FROM` | 否 | 发件人，默认等于 `SMTP_USER` |
| `MAIL_TO` | 是 | 收件人，多个用英文逗号分隔 |
| `SMTP_PORT` | 否 | 默认 `465` |

可选 **Variables**：`LLM_BASE_URL`、`LLM_MODEL`、`SMTP_USE_SSL`（`false` 时走 STARTTLS，常见于 587 端口）。

## 获取密钥

**DeepSeek**：登录 `platform.deepseek.com` → API Keys → 创建，模型默认 `deepseek-chat`。
任何 OpenAI 兼容服务都可以，改 `LLM_BASE_URL` 与 `LLM_MODEL` 即可。

**QQ 邮箱**：设置 → 账户 → 开启 POP3/SMTP → 生成授权码；`SMTP_HOST=smtp.qq.com`、`SMTP_PORT=465`、`SMTP_USE_SSL=true`。

**163 邮箱**：设置 → POP3/SMTP/IMAP → 开启并获取授权码；`smtp.163.com`、465。

**Gmail**：开启两步验证后创建“应用专用密码”；`smtp.gmail.com`、`587`、`SMTP_USE_SSL=false`。

## 本地测试

```bash
# 只生成报告，不发送（不需要 SMTP）
python scripts/valuation_report.py --dry-run

# 不调用 LLM，只看规则结论
python scripts/valuation_report.py --no-llm --dry-run

# 真实发送（先在本地导出环境变量）
export LLM_API_KEY=sk-xxx
export SMTP_HOST=smtp.qq.com
export SMTP_USER=you@qq.com
export SMTP_PASSWORD=授权码
export MAIL_TO=you@qq.com
python scripts/valuation_report.py
```

PowerShell 用 `$env:LLM_API_KEY="sk-xxx"` 的形式设置。

## 降级与失败

| 情况 | 行为 |
|---|---|
| 未设置 `LLM_API_KEY` | 打印警告，使用规则结论，邮件照发 |
| LLM 超时 / 401 / 返回非 JSON | 该公司回退规则结论，报告顶部标注“备注：LLM 失败” |
| 行情采集失败 | 该公司标记“数据错误”，仍参与邮件 |
| 缺少收件人或 SMTP 配置 | 退出码 1，工作流变红，便于发现配置问题 |

## 成本

四家公司各一次调用，输入约 1–2k tokens、输出约 300 tokens，一天不到 1 万 tokens。
按 DeepSeek 当前价格，每天成本在几分钱人民币以内；每月 Actions 时长也远低于免费额度。

## 安全

- 密钥只放在 GitHub Secrets，脚本不读配置文件里的密钥，也不写日志。
- 新闻标题是不可信外部输入：截断到 120 字、放入 `<news>` 标签，系统提示明确要求忽略其中指令。
- 邮件主题会去掉换行等控制字符，避免邮件头注入。
- 输出的是“仓位建议”而非交易指令，并在页面与邮件中标注“不构成投资建议”。

## 常见问题

**没收到邮件**
- 先看 Actions 日志最后一步是否成功；缺 Secret 时脚本会直接报错。
- 检查垃圾邮件目录，必要时把发件人加入白名单。

**SMTP 535 认证失败**
- 多数邮箱要求“授权码”而不是登录密码；确认已开启 SMTP 服务。

**LLM 401 / 402**
- 401 是 Key 无效；402 通常是余额不足。

**报告里全是“数据不足”**
- 说明行情采集失败，看日志里的 `数据错误`；也可能是 `yfinance` 被限流。

**首页没有出现估值建议**
- 确认 `docs/valuation_reports.json` 的 `reports` 首条有 `items`；
- 直接打开 `valuation.html` 能看到内容则是浏览器缓存，强制刷新即可；
- 该区块与每日报告完全独立，日报更新不会覆盖它。
