# 每日公司分析自动化指南

## 📋 概述

每日公司分析由 **GitHub Actions** 完成，不再依赖本机 crontab / launchd：

- 每天 **09:00（Asia/Shanghai，即 01:00 UTC）** 自动运行；
- 分析小米集团、美团、地平线机器人、三安光电四家公司；
- 生成 JSON、综合报告、摘要、站点页面和报告索引；
- 先做一致性校验，校验通过后由机器人账号提交并推送；
- 推送后 GitHub Pages 自动更新。

## 🧩 组成

| 文件 | 作用 |
|---|---|
| `.github/workflows/daily-analysis.yml` | 定时（或手动）生成并发布日报 |
| `.github/workflows/ci.yml` | push / PR 时运行编译、单元测试与一致性校验 |
| `scripts/daily_company_analysis.py` | 采集行情、生成报告 |
| `scripts/check_consistency.py` | 校验文档、站点、配置之间的一致性 |
| `scripts/daily_analysis_config.json` | 公司列表、输出目录、交易时段、调度时间 |
| `tests/test_check_consistency.py` | 校验逻辑的单元测试（仅标准库） |

## ⏰ 调度时间

调度时间的**唯一来源**是配置文件的 `schedule.cron_expression` 与 `schedule.timezone`：

```json
{
  "schedule": {
    "cron_expression": "0 9 * * *",
    "timezone": "Asia/Shanghai",
    "description": "每天09:00 Asia/Shanghai执行"
  }
}
```

GitHub Actions 的 cron 使用 **UTC**，因此工作流里写的是 `0 1 * * *`。两边不一致时，
`scripts/check_consistency.py` 会直接报错，避免“文档改了、任务没改”。

## 🚀 日常使用

### 自动执行

无需操作。每个交易日（含周末，脚本会自动回退到上一交易日数据）09:00 左右自动运行。

### 手动触发

1. 打开仓库 **Actions** → **每日分析发布**；
2. 点击 **Run workflow** → 选择 `main` 分支 → **Run workflow**。

### 本地运行

```bash
# 安装依赖
python -m pip install -r requirements.txt

# 生成报告（会写入 data/、reports/、docs/reports/）
python scripts/daily_company_analysis.py

# 只演练、不写文件
python scripts/daily_company_analysis.py --dry-run

# 校验一致性
python scripts/check_consistency.py

# 单元测试
python -m unittest discover -s tests -v
```

## 📁 产物

| 路径 | 内容 |
|---|---|
| `data/daily_analysis/daily_analysis_YYYYMMDD.json` | 结构化数据（行情、基本面、新闻、结论） |
| `reports/daily_analysis/daily_company_analysis_YYYYMMDD.md` | 综合报告 |
| `reports/daily_analysis/daily_analysis_report_YYYYMMDD.md` | 兼容旧路径的副本 |
| `reports/daily_analysis/daily_summary_YYYYMMDD.md` | 摘要 |
| `docs/reports/daily_company_analysis_YYYYMMDD.html` | 站点页面 |
| `docs/reports/daily_company_analysis_latest.html` | 最新一期 |
| `docs/reports/daily_reports.json` | 报告中心索引（脚本自动追加） |
| `logs/` | 运行日志（不入库，CI 中作为 artifact 上传） |

## 🔍 一致性校验覆盖范围

`scripts/check_consistency.py` 会在以下情况返回非零退出码：

1. JSON 文件无法解析；
2. `docs/reports/daily_reports.json` 中的 `rawPath` / `htmlPath` 不存在，或 `id` 重复；
3. `docs/js/reports.js` 中静态报告的 `rawPath` 不存在；
4. README、NAVIGATION、UPDATE_LOG、guides 中的相对链接失效（跳过代码块与外部链接）；
5. `docs/` 下 HTML 引用的本地资源缺失，或链接越出 `docs/` 发布根目录（Pages 会 404）；
6. 配置中的公司股票代码未出现在首页（`.SS` / `.SH`、港股前导零视为等价）；
7. 配置的 cron 换算成 UTC 后与工作流不一致；
8. 最新日报超过 7 天（仅警告，不阻断）。

## ⚙️ 新增分析公司

1. 在 `scripts/daily_analysis_config.json` 的 `companies` 中追加：

```json
{
  "id": "newco",
  "name": "新公司",
  "ticker": "000001.SZ",
  "market": "A股",
  "industry": "所属行业",
  "analysis_focus": ["关注点1", "关注点2"]
}
```

2. 如需新浪行情兜底，在 `market_data.sina_symbols` 中补一条映射；
3. 在 `docs/index.html` 中补充公司卡片（一致性校验要求首页出现该股票代码）；
4. 本地运行一次 `python scripts/check_consistency.py` 确认通过。

## 🐛 常见问题

**工作流没有按时运行**
- 仓库连续 60 天无提交时，GitHub 会暂停定时工作流；本项目每天由机器人提交，正常不会触发。
- 也可在 Actions 页面用 Run workflow 手动补跑。

**推送失败（403）**
- 检查仓库 `Settings → Actions → General → Workflow permissions` 是否为 *Read and write*；
- 工作流已声明 `permissions: contents: write`。

**推送被拒绝（protected branch）**
- 若 `main` 启用了分支保护，需要允许 `github-actions[bot]` 直接推送，或改为创建 PR；
- 使用 `GITHUB_TOKEN` 的推送不会再触发其他工作流，若将来新增独立的 Pages 部署工作流，需要改用 PAT 或 `workflow_run` 触发。

**报告里行情为 N/A**
- `yfinance` 偶发限流或字段缺失，脚本会自动回退新浪行情；
- 若两家都失败，该公司的 `success` 为 `false`，报告会在“失败项”中说明原因，不影响其他公司。

**站点上的报告打不开**
- 报告中心的 Markdown 通过 `raw.githubusercontent.com` 读取，需要仓库保持公开、分支名为 `main`；
- 动态日报使用本地 HTML（`htmlPath`），不依赖外网。

## 📝 变更记录

### v2.0 (2026-11-15)
- 迁移到 GitHub Actions，删除 crontab / launchd 说明；
- 新增一致性校验与单元测试；
- 修正调度时间口径（09:00 Asia/Shanghai = 01:00 UTC）。

### v1.0.1 (2026-03-12)
- 修正定时任务时间为下午 6 点（已废弃）。

### v1.0.0 (2026-03-12)
- 初始版本，支持 4 家公司每日分析。
