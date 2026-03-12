# 每日公司分析定时任务设置指南

## 📋 概述

本指南介绍如何设置每日公司分析定时任务，该任务会在每天下午6点（18:00）自动分析小米、美团、地平线机器人、三安光电四家公司，生成分析报告并存储。

## 🎯 功能特性

### 核心功能
1. **定时执行**: 每天6点自动运行
2. **多公司分析**: 同时分析4家公司
3. **数据获取**: 从Yahoo Finance获取实时数据
4. **报告生成**: 生成JSON、Markdown、摘要三种格式报告
5. **日志记录**: 完整的执行日志和错误处理

### 分析内容
- 股价表现和趋势分析
- 基本面指标分析
- 近期新闻影响分析
- 投资建议和风险提示

## 🚀 快速开始

### 1. 环境要求
```bash
# 检查Python版本
python3 --version  # 需要Python 3.7+

# 检查必要工具
which bash
which cron
```

### 2. 安装依赖
```bash
# 进入项目目录
cd /Users/mengliang.yang/github/finance

# 安装Python依赖
pip3 install yfinance pandas numpy

# 或者使用requirements.txt
pip3 install -r requirements.txt
```

### 3. 测试运行
```bash
# 给脚本添加执行权限
chmod +x scripts/run_daily_analysis.sh
chmod +x scripts/daily_company_analysis.py

# 手动运行测试
./scripts/run_daily_analysis.sh

# 或者直接运行Python脚本
python3 scripts/daily_company_analysis.py
```

### 4. 设置定时任务

#### 方法一：使用crontab（推荐）
```bash
# 编辑当前用户的crontab
crontab -e

# 添加以下行（每天下午6点执行）
0 18 * * * /Users/mengliang.yang/github/finance/scripts/run_daily_analysis.sh

# 保存并退出
```

#### 方法二：使用系统cron
```bash
# 编辑系统cron
sudo nano /etc/crontab

# 添加以下行
0 18 * * * mengliang.yang /Users/mengliang.yang/github/finance/scripts/run_daily_analysis.sh
```

#### 方法三：使用launchd（macOS）
```bash
# 创建plist文件
nano ~/Library/LaunchAgents/com.finance.dailyanalysis.plist

# 添加以下内容
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.finance.dailyanalysis</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/mengliang.yang/github/finance/scripts/run_daily_analysis.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>18</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/mengliang.yang/github/finance/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/mengliang.yang/github/finance/logs/launchd_error.log</string>
</dict>
</plist>

# 加载任务
launchctl load ~/Library/LaunchAgents/com.finance.dailyanalysis.plist
```

## 📁 文件结构

### 脚本文件
```
scripts/
├── daily_company_analysis.py      # 主分析脚本
├── run_daily_analysis.sh          # 包装脚本（定时任务调用）
└── daily_analysis_config.json     # 配置文件
```

### 输出目录
```
data/
└── daily_analysis/                # JSON数据文件
    ├── daily_analysis_20260312.json
    └── ...

reports/
└── daily_analysis/                # 分析报告
    ├── daily_analysis_report_20260312.md    # 详细报告
    └── daily_summary_20260312.md            # 摘要报告

logs/                              # 日志文件
├── daily_analysis_20260312_060000.log
├── analysis_log_20260312.json
└── ...
```

### 配置文件
```
guides/
└── DAILY_ANALYSIS_SETUP.md        # 本指南
```

## ⚙️ 配置说明

### 定时任务配置
```json
{
  "schedule": {
    "cron_expression": "0 18 * * *",     // 每天18点（下午6点）
    "timezone": "Asia/Shanghai",         // 上海时区
    "description": "每天下午6点执行"
  }
}
```

### 公司配置
```json
{
  "companies": [
    {
      "id": "xiaomi",
      "name": "小米集团",
      "ticker": "1810.HK",               // 股票代码
      "market": "港股",
      "industry": "消费电子/智能硬件"
    }
    // ... 其他公司
  ]
}
```

### 分析参数
```json
{
  "analysis_parameters": {
    "data_period": "5d",                 // 获取5天数据
    "include_news": true,                // 包含新闻
    "news_count": 5,                     // 最多5条新闻
    "generate_json": true,               // 生成JSON
    "generate_markdown": true,           // 生成Markdown
    "generate_summary": true,            // 生成摘要
    "log_analysis": true                 // 记录日志
  }
}
```

## 🔧 自定义配置

### 修改分析公司
编辑 `scripts/daily_company_analysis.py` 中的 `COMPANIES` 字典：
```python
COMPANIES = {
    'new_company': {
        'name': '新公司名称',
        'ticker': '股票代码',
        'market': '市场',
        'industry': '行业'
    }
    # ... 添加或修改公司
}
```

### 修改分析时间
编辑crontab配置：
```bash
# 每天下午6点执行（默认）
0 18 * * * /path/to/run_daily_analysis.sh

# 每天上午9点执行
0 9 * * * /path/to/run_daily_analysis.sh

# 工作日每天下午6点执行
0 18 * * 1-5 /path/to/run_daily_analysis.sh

# 每小时执行一次
0 * * * * /path/to/run_daily_analysis.sh
```

### 修改输出目录
编辑 `scripts/daily_company_analysis.py` 中的输出目录配置：
```python
OUTPUT_DIR = project_root / 'custom_data' / 'daily'
REPORTS_DIR = project_root / 'custom_reports' / 'daily'
LOG_DIR = project_root / 'custom_logs'
```

## 📊 报告格式

### JSON数据文件
```json
{
  "company_id": "xiaomi",
  "company_name": "小米集团",
  "ticker": "1810.HK",
  "analysis_date": "2026-03-12",
  "price": {
    "current": 18.5,
    "change": 0.5,
    "change_pct": 2.78,
    "trend": "上涨"
  },
  "fundamentals": {
    "market_cap": 500000000000,
    "pe_ratio": 25.5
  },
  "conclusion": ["股价表现强劲，今日上涨2.78%"]
}
```

### Markdown详细报告
```markdown
# 每日公司分析报告

**分析日期**: 2026年3月12日
**生成时间**: 2026-03-12 06:05:23

## 📊 总体概览
- **成功分析**: 4家公司
- **失败分析**: 0家公司

## 🏢 各公司详细分析
### 小米集团 (1810.HK)
**市场**: 港股 | **行业**: 消费电子/智能硬件

#### 价格表现 📈
- **当前价格**: 18.5
- **价格变化**: 0.5 (2.78%)
- **趋势**: 上涨
```

### 摘要报告
```markdown
# 每日分析摘要

**日期**: 2026年3月12日
**时间**: 06:05

## 📈 今日表现概览
- **平均涨跌幅**: 1.25%
- **上涨公司**: 3家
- **下跌公司**: 1家

## 🎯 操作建议
### 建议关注
1. **趋势跟踪**: 关注连续上涨的公司
2. **价值发现**: 关注估值合理的公司
```

## 🐛 故障排除

### 常见问题

#### 1. Python依赖问题
```bash
# 检查Python版本
python3 --version

# 安装依赖
pip3 install yfinance pandas numpy --upgrade

# 如果遇到权限问题
pip3 install --user yfinance pandas numpy
```

#### 2. 定时任务不执行
```bash
# 检查cron服务状态
sudo systemctl status cron      # Linux
sudo systemctl status crond     # CentOS

# 检查cron日志
sudo tail -f /var/log/cron      # Linux
sudo tail -f /var/log/syslog    # Ubuntu

# 手动测试脚本
./scripts/run_daily_analysis.sh
```

#### 3. 数据获取失败
```bash
# 检查网络连接
ping finance.yahoo.com

# 检查API限制
# Yahoo Finance有请求频率限制，避免频繁请求

# 使用代理（如果需要）
export https_proxy=http://proxy.example.com:8080
```

#### 4. 磁盘空间不足
```bash
# 检查磁盘空间
df -h

# 清理旧日志和报告
# 脚本会自动保留最近30天的报告
```

### 日志检查
```bash
# 查看最新日志
ls -la logs/daily_analysis_*.log | tail -5

# 查看具体日志内容
tail -100 logs/daily_analysis_20260312_060000.log

# 查看错误日志
grep -i error logs/*.log
```

## 🔄 维护和更新

### 定期维护
1. **检查磁盘空间**: 每月检查一次
2. **更新依赖**: 每季度更新Python包
3. **备份数据**: 每周备份重要数据
4. **检查日志**: 每天检查执行日志

### 数据清理
脚本会自动管理数据保留：
- 每日报告: 保留30天
- 每周摘要: 保留12周
- 月度报告: 保留24个月

手动清理命令：
```bash
# 清理30天前的数据
find data/daily_analysis -name "*.json" -mtime +30 -delete
find reports/daily_analysis -name "*.md" -mtime +30 -delete
find logs -name "*.log" -mtime +30 -delete
```

### 版本更新
```bash
# 拉取最新代码
cd /Users/mengliang.yang/github/finance
git pull origin main

# 更新依赖
pip3 install -r requirements.txt --upgrade

# 重启定时任务
# 如果使用crontab，修改后会自动生效
# 如果使用launchd，需要重新加载
launchctl unload ~/Library/LaunchAgents/com.finance.dailyanalysis.plist
launchctl load ~/Library/LaunchAgents/com.finance.dailyanalysis.plist
```

## 📞 支持与反馈

### 问题报告
1. **检查日志**: 首先查看相关日志文件
2. **重现问题**: 尝试手动运行脚本
3. **收集信息**: 收集错误信息和环境信息
4. **提交问题**: 在GitHub Issues中报告

### 联系方式
- **GitHub仓库**: https://github.com/mengliang555/finance
- **项目主页**: https://mengliang555.github.io/finance/
- **报告目录**: https://mengliang555.github.io/finance/reports_index.html

### 贡献指南
1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📝 更新日志

### v1.0.1 (2026-03-12)
- 修正定时任务时间为下午6点（18:00）
- 更新所有文档中的时间说明

### v1.0.0 (2026-03-12)
- 初始版本发布
- 支持4家公司每日分析
- 生成JSON、Markdown、摘要三种报告
- 完整的日志和错误处理
- 定时任务配置

### 未来计划
- 添加更多分析指标
- 支持更多数据源
- 添加邮件通知功能
- 开发Web管理界面

---

**最后更新**: 2026年3月12日  
**维护状态**: 活跃  
**下次检查**: 2026年4月12日