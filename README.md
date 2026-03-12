# Finance Analysis Project

专业的财务分析项目，包含公司分析、行业研究、每日报告和AI分析。

## 📁 项目结构

```
finance/
├── README.md                    # 项目说明
├── docs/                        # 网站文件
│   ├── index.html              # 主页面
│   ├── css/                    # 样式文件
│   ├── js/                     # JavaScript文件
│   ├── reports/                # 报告页面
│   └── archive/                # 归档文件
├── reports/                     # 分析报告
│   ├── company_analysis/       # 公司分析
│   │   ├── xiaomi_financial_analysis.md
│   │   ├── meituan_financial_analysis.md
│   │   ├── horizon_robotics_financial_analysis.md
│   │   └── sanan_opto_financial_analysis.md
│   ├── industry_analysis/      # 行业分析
│   │   ├── comparative_analysis.md
│   │   └── power_equipment_grid.md
│   ├── daily_reports/          # 每日报告
│   │   └── daily_stock_performance_20260312.md
│   └── ai_analysis/            # AI分析
│       ├── deepseek_v4_open_source_analysis.md
│       └── deepseek_v4_huawei_ascend_analysis.md
├── data/                       # 数据文件
│   ├── raw/                    # 原始数据
│   └── processed/              # 处理后的数据
├── scripts/                    # 脚本文件
│   ├── data_collection/        # 数据收集脚本
│   └── analysis/               # 分析脚本
├── guides/                     # 指南文档
│   ├── company_analysis_framework.md
│   ├── ACCESS_GUIDE.md
│   ├── GITHUB_PAGES_SETUP.md
│   └── GIT_VERSION_CONTROL_GUIDE.md
├── archive/                    # 归档文件
│   └── 20260311/               # 2026年3月11日归档
└── .gitignore                  # Git忽略配置
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

### 4. AI技术分析
- DeepSeek V4开源影响分析
- 华为升腾芯片训练影响分析
- AI产业链投资机会

### 5. 自动化工具
- 数据收集脚本
- 网站报告更新脚本
- 分析工具

## 🚀 快速开始

### 访问网站
```
https://mengliang555.github.io/finance/
```

### 本地开发
```bash
# 克隆项目
git clone https://github.com/mengliang555/finance.git
cd finance

# 安装依赖
pip install -r requirements.txt

# 运行数据收集脚本
python scripts/data_collection/get_horizon_data.py

# 更新网站报告
python scripts/analysis/update_website_reports.py
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
- **部署**: GitHub Pages
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

**最后更新**: 2026年3月12日  
**项目状态**: 活跃开发中  
**数据更新频率**: 每日
