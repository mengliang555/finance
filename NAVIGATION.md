# 项目导航索引

## 📋 快速导航

### 公司分析报告
- [小米集团财务分析](reports/company_analysis/xiaomi_financial_analysis.md)
- [美团财务分析](reports/company_analysis/meituan_financial_analysis.md)
- [地平线机器人财务分析](reports/company_analysis/horizon_robotics_financial_analysis.md)
- [三安光电财务分析](reports/company_analysis/sanan_opto_financial_analysis.md)
- [中宠股份深度分析](reports/zhongchong_analysis_20260319.md)

### 行业分析报告
- [四家公司对比分析](reports/industry_analysis/comparative_analysis.md)
- [电力设备和电网领域分析](reports/industry_analysis/power_equipment_grid.md)

### 每日报告
- [2026年3月12日股票表现](reports/daily_reports/daily_stock_performance_20260312.md)
- [2026年3月12日公司分析](reports/daily_analysis/daily_company_analysis_20260312.md)
- [2026年3月13日公司分析](reports/daily_analysis/daily_company_analysis_20260313.md)
- [2026年3月14日公司分析（周末特别版）](reports/daily_analysis/daily_company_analysis_20260314.md)
- [2026年3月15日公司分析（周日准备版）](reports/daily_analysis/daily_company_analysis_20260315.md)
- [2026年3月16日公司分析（周一复盘版）](reports/daily_analysis/daily_company_analysis_20260316.md)
- [2026年3月17日公司分析（周二复盘版）](reports/daily_analysis/daily_company_analysis_20260317.md)
- [2026年3月18日公司分析（周三复盘版）](reports/daily_analysis/daily_company_analysis_20260318.md)

### AI分析报告
- [DeepSeek V4开源影响分析](reports/ai_analysis/deepseek_v4_open_source_analysis.md)
- [DeepSeek V4华为升腾芯片训练影响分析](reports/ai_analysis/deepseek_v4_huawei_ascend_analysis.md)

### 指南文档
- [公司分析框架](guides/company_analysis_framework.md)
- [访问指南](guides/ACCESS_GUIDE.md)
- [GitHub Pages设置指南](guides/GITHUB_PAGES_SETUP.md)
- [Git版本控制指南](guides/GIT_VERSION_CONTROL_GUIDE.md)

### 网站页面
- [主页面](docs/index.html)
- [小米报告页面](docs/reports/xiaomi_report.html)
- [美团报告页面](docs/reports/meituan_report.html)
- [地平线机器人报告页面](docs/reports/horizon_report.html)
- [三安光电报告页面](docs/reports/sanan_report.html)
- [对比分析报告页面](docs/reports/comparative_report.html)

## 🔄 更新流程

### 每日更新
1. 运行数据收集脚本
2. 生成每日报告
3. 更新网站数据
4. 提交到GitHub

### 公司分析更新
1. 收集最新财务数据
2. 更新分析报告
3. 更新网站报告页面
4. 提交到GitHub

### 行业分析更新
1. 收集行业最新动态
2. 更新行业分析报告
3. 更新网站相关内容
4. 提交到GitHub

## 📊 数据流程

```
数据收集 → 数据处理 → 分析报告 → 网站更新 → GitHub发布
    ↓           ↓           ↓           ↓           ↓
新浪财经API  数据清洗    Markdown报告  HTML页面   GitHub Pages
腾讯财经API  数据转换    投资建议      CSS样式    自动部署
公司财报     数据验证    风险提示      JavaScript 实时访问
```

## 🛠️ 工具脚本

### 数据收集
- `scripts/data_collection/get_horizon_data.py` - 获取地平线机器人数据

### 分析处理
- `scripts/analysis/update_website_reports.py` - 更新网站报告

### 网站部署
- `SETUP_GITHUB_PAGES.sh` - 设置GitHub Pages

## 📅 维护计划

### 每日维护
- [ ] 更新股票数据
- [ ] 生成每日报告
- [ ] 检查网站运行状态

### 每周维护
- [ ] 更新公司分析报告
- [ ] 检查数据质量
- [ ] 备份重要数据

### 每月维护
- [ ] 整理归档文件
- [ ] 更新项目文档
- [ ] 优化代码结构

## 🔍 搜索指南

### 按公司搜索
- 小米: `grep -r "小米" reports/`
- 美团: `grep -r "美团" reports/`
- 地平线: `grep -r "地平线" reports/`
- 三安光电: `grep -r "三安光电" reports/`

### 按主题搜索
- 财务分析: `grep -r "财务分析" reports/`
- 投资建议: `grep -r "投资建议" reports/`
- 风险提示: `grep -r "风险提示" reports/`

### 按日期搜索
- 2026年3月: `find . -name "*202603*" -type f`
- 每日报告: `find reports/daily_reports -name "*.md"`

## 📞 问题反馈

### 常见问题
1. **网站无法访问**: 检查GitHub Pages设置
2. **数据更新失败**: 检查API密钥和网络连接
3. **报告格式错误**: 检查Markdown语法

### 反馈渠道
- GitHub Issues: 报告bug和功能请求
- 邮件联系: 项目维护者
- 文档更新: 提交Pull Request

---

**导航索引最后更新**: 2026年3月19日  
**维护状态**: 活跃  
**下次全面检查**: 2026年3月26日
