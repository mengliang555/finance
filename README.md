# Finance Analysis Project

专业的财务分析项目，包含公司分析、行业研究、每日报告和自动化发布。

## 📁 项目结构

```
finance/
├── README.md                    # 项目说明
├── NAVIGATION.md                # 导航索引
├── UPDATE_LOG.md                # 更新日志
├── requirements.txt             # Python 依赖
├── LICENSE                      # MIT 许可证
├── wrangler.toml                # Cloudflare Workers 配置
├── .github/workflows/           # 自动化
│   ├── ci.yml                   # 推送/PR 一致性校验
│   └── daily-analysis.yml       # 每天 09:00 生成并发布日报
├── docs/                        # 网站文件（GitHub Pages 发布根目录）
│   ├── index.html               # 主页面
│   ├── reports_index.html       # 报告中心
│   ├── css/                     # 样式文件
│   ├── js/                      # 交互与报告索引
│   └── reports/                 # 报告页面与索引 JSON
├── reports/                     # 分析报告（Markdown）
│   ├── company_analysis/        # 公司分析
│   ├── industry_analysis/       # 行业分析
│   └── daily_analysis/          # 每日报告与摘要
├── data/                        # 数据文件
│   └── daily_analysis/          # 每日行情与分析 JSON
├── scripts/                     # 脚本
│   ├── daily_company_analysis.py    # 每日分析主脚本
│   ├── check_consistency.py         # 仓库一致性校验
│   ├── build_site.py                # 组装部署产物 dist/
│   ├── daily_analysis_config.json   # 公司与调度配置
│   ├── analysis/                    # 站点维护脚本
│   └── data_collection/             # 数据采集脚本
├── tests/                       # 单元测试
├── guides/                      # 指南文档
└── archive/                     # 历史归档
```

## 🎯 核心功能

### 1. 公司财务分析
- 小米集团 (1810.HK) 财务分析
- 美团 (3690.HK) 财务分析
- 地平线机器人 (09660.HK) 财务分析
- 三安光电 (600703.SS) 财务分析

### 2. 行业对比分析
- 四家公司对比分析报告
- 电力设备和电网领域分析
- 投资组合建议

### 3. 每日市场报告
- 关注股票每日涨幅情况
- 市场表现总结
- 操作建议
- 新闻主源 yfinance，无结果时自动回退 Google 新闻 RSS

### 4. 自动化与校验
- GitHub Actions 每天 09:00（Asia/Shanghai）自动生成并发布日报
- `scripts/check_consistency.py` 检查链接、报告索引、股票代码与调度配置的一致性
- 单元测试覆盖校验逻辑，推送与 PR 时自动运行

### 5. LLM 估值邮件（分支功能）
- 每天 10:00 用大模型基于行情、基本面与新闻生成估值判断
- 通过 SMTP 发送 HTML 邮件，失败时回退规则结论
- 配置见 [guides/VALUATION_LLM_EMAIL.md](guides/VALUATION_LLM_EMAIL.md)

## 🚀 快速开始

### 访问网站
```
https://mengliang555.github.io/finance/
```

### 部署到 Cloudflare Workers
```bash
# 组装 dist/（docs/ + 报告 Markdown）
python scripts/build_site.py

# 发布（需要先 npx wrangler login）
npx wrangler deploy
```
Workers Builds 的 Git 集成与自定义域名步骤见 [guides/CLOUDFLARE_DEPLOY.md](guides/CLOUDFLARE_DEPLOY.md)。

### 本地开发
```bash
# 克隆项目
git clone https://github.com/mengliang555/finance.git
cd finance

# 安装依赖
pip install -r requirements.txt

# 运行每日分析（生成 Markdown / JSON / 站点页面）
python scripts/daily_company_analysis.py

# 校验文档、站点与配置是否一致
python scripts/check_consistency.py

# 运行单元测试
python -m unittest discover -s tests -v
```

### 查看报告
- 公司分析报告: `reports/company_analysis/`
- 行业分析报告: `reports/industry_analysis/`
- 每日报告: `reports/daily_reports/`
- AI分析报告: `reports/ai_analysis/`

## 📊 数据来源

1. **股票数据**: 新浪财经API、腾讯财经API
2. **财务数据**: 公司财报、公开信息
3. **行业数据**: 行业研究报告、政策文件
4. **AI数据**: 技术文档、行业分析

## 🔧 技术栈

- **前端**: HTML5、CSS3、JavaScript
- **后端**: Python、Shell脚本
- **数据**: JSON、Markdown
- **部署**: GitHub Pages、Cloudflare Workers
- **版本控制**: Git

## 📈 更新日志

详细更新记录请查看: [UPDATE_LOG.md](UPDATE_LOG.md)

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过GitHub Issues提交。

---

**最后更新**: 2026年11月15日  
**项目状态**: 活跃开发中  
**数据更新频率**: 每日
