#!/bin/bash
# 每日公司分析包装脚本
# 用于定时任务调用

# 设置环境
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# 配置
LOG_DIR="$PROJECT_ROOT/logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$LOG_DIR/daily_analysis_${TIMESTAMP}.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 输出开始信息
echo "==========================================" >> "$LOG_FILE"
echo "🚀 开始每日公司分析" >> "$LOG_FILE"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "项目目录: $PROJECT_ROOT" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 检查Python环境
echo "🔍 检查Python环境..." >> "$LOG_FILE"
python3 --version >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python3 未安装或不可用" >> "$LOG_FILE"
    exit 1
fi

# 检查yfinance库
echo "🔍 检查yfinance库..." >> "$LOG_FILE"
python3 -c "import yfinance" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️ yfinance库未安装，尝试安装..." >> "$LOG_FILE"
    pip3 install yfinance pandas >> "$LOG_FILE" 2>&1
    if [ $? -ne 0 ]; then
        echo "❌ 安装yfinance失败" >> "$LOG_FILE"
        exit 1
    fi
    echo "✅ yfinance库安装成功" >> "$LOG_FILE"
else
    echo "✅ yfinance库已安装" >> "$LOG_FILE"
fi

# 运行分析脚本
echo "📊 运行分析脚本..." >> "$LOG_FILE"
python3 scripts/daily_company_analysis.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# 输出结果
echo "" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 分析完成成功" >> "$LOG_FILE"
    
    # 获取生成的文件
    TODAY=$(date '+%Y%m%d')
    JSON_FILE="$PROJECT_ROOT/data/daily_analysis/daily_analysis_${TODAY}.json"
    MD_FILE="$PROJECT_ROOT/reports/daily_analysis/daily_analysis_report_${TODAY}.md"
    SUMMARY_FILE="$PROJECT_ROOT/reports/daily_analysis/daily_summary_${TODAY}.md"
    
    if [ -f "$JSON_FILE" ]; then
        echo "📁 数据文件: $JSON_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$MD_FILE" ]; then
        echo "📄 详细报告: $MD_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$SUMMARY_FILE" ]; then
        echo "📋 摘要报告: $SUMMARY_FILE" >> "$LOG_FILE"
    fi
else
    echo "❌ 分析完成失败 (退出码: $EXIT_CODE)" >> "$LOG_FILE"
fi

echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "日志文件: $LOG_FILE" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 输出日志文件路径
echo "分析完成，日志文件: $LOG_FILE"

# 返回退出码
exit $EXIT_CODE