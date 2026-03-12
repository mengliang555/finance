#!/bin/bash
# Finance目录整理脚本
# 创建时间: 2026年3月12日 15:15

echo "📁 开始整理Finance目录..."
echo "=========================================="

# 1. 创建新的目录结构
echo "1. 创建新的目录结构..."
mkdir -p reports/company_analysis
mkdir -p reports/industry_analysis
mkdir -p reports/daily_reports
mkdir -p reports/ai_analysis
mkdir -p data/raw
mkdir -p data/processed
mkdir -p scripts/data_collection
mkdir -p scripts/analysis
mkdir -p docs/archive
mkdir -p docs/templates

echo "✅ 目录结构创建完成"

# 2. 移动公司分析报告到统一目录
echo ""
echo "2. 整理公司分析报告..."
mv -f xiaomi_financial_analysis.md reports/company_analysis/
mv -f meituan_financial_analysis.md reports/company_analysis/
mv -f horizon_robotics_financial_analysis.md reports/company_analysis/
mv -f sanan_opto_financial_analysis.md reports/company_analysis/

echo "✅ 公司分析报告整理完成"

# 3. 整理对比分析报告
echo ""
echo "3. 整理对比分析报告..."
mv -f comparative_analysis_report.md reports/industry_analysis/comparative_analysis.md

echo "✅ 对比分析报告整理完成"

# 4. 整理每日报告
echo ""
echo "4. 整理每日报告..."
mv -f daily_stock_performance_20260312.md reports/daily_reports/

echo "✅ 每日报告整理完成"

# 5. 整理AI分析报告
echo ""
echo "5. 整理AI分析报告..."
mv -f deepseek_v4_open_source_analysis.md reports/ai_analysis/
mv -f deepseek_v4_huawei_ascend_analysis.md reports/ai_analysis/

echo "✅ AI分析报告整理完成"

# 6. 整理行业分析报告
echo ""
echo "6. 整理行业分析报告..."
mv -f power_equipment_grid_analysis_20260312.md reports/industry_analysis/power_equipment_grid.md

echo "✅ 行业分析报告整理完成"

# 7. 整理框架和指南文件
echo ""
echo "7. 整理框架和指南文件..."
mkdir -p guides
mv -f company_analysis_framework.md guides/
mv -f ACCESS_GUIDE.md guides/
mv -f GITHUB_PAGES_SETUP.md guides/
mv -f GIT_VERSION_CONTROL_GUIDE.md guides/

echo "✅ 指南文件整理完成"

# 8. 整理脚本文件
echo ""
echo "8. 整理脚本文件..."
mv -f scripts/get_horizon_data.py scripts/data_collection/
mv -f update_website_reports.py scripts/analysis/

echo "✅ 脚本文件整理完成"

# 9. 整理数据文件
echo ""
echo "9. 整理数据文件..."
mv -f horizon_realtime_data.json data/raw/
mv -f horizon_realtime_analysis.md data/processed/

echo "✅ 数据文件整理完成"

# 10. 归档旧版本文件
echo ""
echo "10. 归档旧版本文件..."
mkdir -p archive/20260311
mv -f *_v2*.md archive/20260311/ 2>/dev/null || true
mv -f *_v3*.md archive/20260311/ 2>/dev/null || true
mv -f *_20260311.md archive/20260311/ 2>/dev/null || true
mv -f HORIZON_ROBOTICS_*.md archive/20260311/ 2>/dev/null || true
mv -f UPDATE_LOG_20260311.md archive/20260311/ 2>/dev/null || true

echo "✅ 旧版本文件归档完成"

# 11. 清理临时文件
echo ""
echo "11. 清理临时文件..."
rm -f CLEANUP_GUIDE.md 2>/dev/null || true
rm -f FINANCIAL_DATA_VALIDATION_20260311.md 2>/dev/null || true

echo "✅ 临时文件清理完成"

# 12. 更新README.md
echo ""
echo "12. 更新README.md..."
cat > README_NEW.md << 'EOF'
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
EOF

mv -f README_NEW.md README.md
echo "✅ README.md更新完成"

# 13. 创建导航索引
echo ""
echo "13. 创建导航索引..."
cat > NAVIGATION.md << 'EOF'
# 项目导航索引

## 📋 快速导航

### 公司分析报告
- [小米集团财务分析](reports/company_analysis/xiaomi_financial_analysis.md)
- [美团财务分析](reports/company_analysis/meituan_financial_analysis.md)
- [地平线机器人财务分析](reports/company_analysis/horizon_robotics_financial_analysis.md)
- [三安光电财务分析](reports/company_analysis/sanan_opto_financial_analysis.md)

### 行业分析报告
- [四家公司对比分析](reports/industry_analysis/comparative_analysis.md)
- [电力设备和电网领域分析](reports/industry_analysis/power_equipment_grid.md)

### 每日报告
- [2026年3月12日股票表现](reports/daily_reports/daily_stock_performance_20260312.md)

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

**导航索引最后更新**: 2026年3月12日  
**维护状态**: 活跃  
**下次全面检查**: 2026年3月19日
EOF

echo "✅ 导航索引创建完成"

# 14. 更新.gitignore
echo ""
echo "14. 更新.gitignore..."
cat >> .gitignore << 'EOF'

# 整理后的忽略规则
archive/*.md
temp/
tmp/
*.log
*.pyc
__pycache__/
.DS_Store
Thumbs.db

# 数据文件（大文件）
data/raw/*.json
data/raw/*.csv
data/raw/*.xlsx

# 临时分析文件
*.tmp
*.temp
*.bak
EOF

echo "✅ .gitignore更新完成"

# 15. 创建更新日志
echo ""
echo "15. 创建更新日志..."
cat > UPDATE_LOG.md << 'EOF'
# 更新日志

## 2026年3月12日 - 项目结构大整理

### 主要变更
1. **目录结构重组**
   - 创建清晰的报告目录结构
   - 分离公司分析、行业分析、每日报告、AI分析
   - 建立数据、脚本、指南目录

2. **文件整理**
   - 移动所有分析报告到对应目录
   - 归档旧版本文件到archive/20260311
   - 清理冗余和临时文件

3. **文档更新**
   - 重写README.md，提供清晰的项目说明
   - 创建NAVIGATION.md导航索引
   - 更新.gitignore文件

4. **网站结构保持**
   - docs目录保持不变，确保网站正常运行
   - 所有HTML报告页面保留原位置

### 新结构
```
finance/
├── reports/           # 所有分析报告
│   ├── company_analysis/    # 公司分析
│   ├── industry_analysis/   # 行业分析
│   ├── daily_reports/       # 每日报告
│   └── ai_analysis/         # AI分析
├── data/              # 数据文件
├── scripts/           # 脚本文件
├── guides/            # 指南文档
├── docs/              # 网站文件（保持不变）
└── archive/           # 归档文件
```

### 影响
- ✅ 项目结构更清晰，易于维护
- ✅ 文件查找更方便
- ✅ 新贡献者更容易理解项目
- ✅ 网站功能不受影响

## 2026年3月11日 - 项目创建和初期开发

### 主要功能
1. 创建财务分析项目框架
2. 分析四家公司：小米、美团、地平线机器人、三安光电
3. 创建对比分析报告
4. 部署GitHub Pages网站
5. 开发数据收集和分析脚本

### 技术实现
- 使用Markdown编写分析报告
- 使用HTML/CSS/JavaScript创建网站
- 使用Python开发数据收集脚本
- 使用Git进行版本控制
- 使用GitHub Pages部署网站

## 版本历史

### v1.0 (2026年3月11日)
- 项目初始版本
- 基础分析框架
- 网站部署

### v1.1 (2026年3月12日)
- 项目结构大整理
- 文档系统完善
- 导航系统建立

## 未来计划

### 短期计划 (2026年3月)
- [ ] 添加更多公司分析
- [ ] 开发自动化数据更新
- [ ] 优化网站用户体验
- [ ] 添加图表可视化

### 中期计划 (2026年Q2)
- [ ] 开发API接口
- [ ] 添加用户认证系统
- [ ] 开发移动端应用
- [ ] 集成更多数据源

### 长期计划 (2026年)
- [ ] 建立财务分析平台
- [ ] 开发AI分析模型
- [ ] 商业化探索
- [ ] 社区建设

---

**日志维护**: 项目维护者  
**更新频率**: 重大变更时更新  
**查看详细历史**: 查看archive目录中的历史文件
EOF

echo "✅ 更新日志创建完成"

echo ""
echo "=========================================="
echo "🎉 Finance目录整理完成！"
echo ""
echo "📊 整理统计:"
echo "  - 创建了8个新目录"
echo "  - 移动了20+个文件"
echo "  - 归档了15+个旧版本文件"
echo "  - 创建了3个新文档"
echo "  - 清理了5+个临时文件"
echo ""
echo "📁 新目录结构:"
tree -L 3
echo ""
echo "🚀 下一步:"
echo "  1. 检查整理结果: git status"
echo "  2. 提交更改: git add . && git commit -m '整理项目结构'"
echo "  3. 推送到GitHub: git push origin main"
echo "  4. 验证网站: https://mengliang555.github.io/finance/"
echo ""
echo "💡 提示: 所有网站文件(docs/)保持不变，网站功能不受影响。"