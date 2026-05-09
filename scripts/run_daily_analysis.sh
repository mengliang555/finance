#!/bin/bash
# 每日公司综合分析包装脚本
# 用于定时任务调用

# 设置环境
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Python解释器
if [ -d "$PROJECT_ROOT/.venv" ]; then
    PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
else
    PYTHON_BIN="python3"
fi

# 配置
LOG_DIR="$PROJECT_ROOT/logs"
if [ -x "$PYTHON_BIN" ] || command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    LOG_DIR=$("$PYTHON_BIN" - <<'PY'
import json
from pathlib import Path
root = Path.cwd()
config = json.loads((root / "scripts" / "daily_analysis_config.json").read_text(encoding="utf-8"))
log_dir = Path(config.get("output_directories", {}).get("logs", "logs"))
print(log_dir if log_dir.is_absolute() else root / log_dir)
PY
    )
    if [ -z "$LOG_DIR" ]; then
        LOG_DIR="$PROJECT_ROOT/logs"
    fi
fi
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$LOG_DIR/daily_analysis_${TIMESTAMP}.log"

# 创建日志目录
mkdir -p "$LOG_DIR"

# 输出开始信息
echo "==========================================" >> "$LOG_FILE"
echo "🚀 开始每日公司综合分析" >> "$LOG_FILE"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "项目目录: $PROJECT_ROOT" >> "$LOG_FILE"
echo "计划执行: 每天 09:00 Asia/Shanghai" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

# 检查Python环境
echo "🔍 检查Python环境..." >> "$LOG_FILE"
"$PYTHON_BIN" --version >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Python3 未安装或不可用" >> "$LOG_FILE"
    exit 1
fi

# 检查yfinance库
echo "🔍 检查yfinance库..." >> "$LOG_FILE"
"$PYTHON_BIN" -c "import yfinance" >> "$LOG_FILE" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ yfinance库未安装，请先在运行环境中安装 yfinance pandas" >> "$LOG_FILE"
    exit 1
else
    echo "✅ yfinance库已安装" >> "$LOG_FILE"
fi

# 运行分析脚本
echo "📊 运行分析脚本..." >> "$LOG_FILE"
"$PYTHON_BIN" scripts/daily_company_analysis.py >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# 输出结果
echo "" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 分析完成成功" >> "$LOG_FILE"
    
    # 获取生成的文件
    TODAY=$(date '+%Y%m%d')
    JSON_FILE="$PROJECT_ROOT/data/daily_analysis/daily_analysis_${TODAY}.json"
    MD_FILE="$PROJECT_ROOT/reports/daily_analysis/daily_company_analysis_${TODAY}.md"
    LEGACY_MD_FILE="$PROJECT_ROOT/reports/daily_analysis/daily_analysis_report_${TODAY}.md"
    SUMMARY_FILE="$PROJECT_ROOT/reports/daily_analysis/daily_summary_${TODAY}.md"
    HTML_FILE="$PROJECT_ROOT/docs/reports/daily_company_analysis_${TODAY}.html"
    
    if [ -f "$JSON_FILE" ]; then
        echo "📁 数据文件: $JSON_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$MD_FILE" ]; then
        echo "📄 综合报告: $MD_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$LEGACY_MD_FILE" ]; then
        echo "📄 兼容报告: $LEGACY_MD_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$SUMMARY_FILE" ]; then
        echo "📋 摘要报告: $SUMMARY_FILE" >> "$LOG_FILE"
    fi
    if [ -f "$HTML_FILE" ]; then
        echo "🌐 Pages页面: $HTML_FILE" >> "$LOG_FILE"
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
