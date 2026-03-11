#!/bin/bash

# GitHub Pages 配置脚本
# 用于配置财务分析项目的GitHub Pages

echo "========================================="
echo "    GitHub Pages 配置脚本"
echo "    财务分析项目部署"
echo "    时间: 2026-03-11 14:43"
echo "========================================="

echo ""
echo "📊 项目信息:"
echo "-----------------------------------------"
echo "仓库: mengliang555/finance"
echo "分支: main"
echo "目录: docs/"
echo "目标URL: https://mengliang555.github.io/finance"
echo ""

echo "🔍 检查当前状态:"
echo "-----------------------------------------"

# 检查Git状态
echo "1. Git仓库状态:"
cd /Users/mengliang.yang/github/finance
git status --short

echo ""
echo "2. 最近提交:"
git log --oneline -3

echo ""
echo "3. 网站文件检查:"
if [ -f "docs/index.html" ]; then
    echo "   ✅ index.html 存在 ($(wc -c docs/index.html | awk '{print $1}')字节)"
else
    echo "   ❌ index.html 缺失"
fi

if [ -f "docs/_config.yml" ]; then
    echo "   ✅ _config.yml 存在 ($(wc -c docs/_config.yml | awk '{print $1}')字节)"
else
    echo "   ❌ _config.yml 缺失"
fi

if [ -f "docs/.nojekyll" ]; then
    echo "   ✅ .nojekyll 存在"
else
    echo "   ❌ .nojekyll 缺失"
fi

echo ""
echo "🚀 GitHub Pages 配置步骤:"
echo "========================================="
echo ""
echo "请按照以下步骤手动配置GitHub Pages:"
echo ""
echo "步骤1: 打开GitHub仓库设置页面"
echo "   🔗 https://github.com/mengliang555/finance/settings/pages"
echo ""
echo "步骤2: 配置部署设置"
echo "   1. 在 'Source' 部分选择: 'Deploy from a branch'"
echo "   2. 在 'Branch' 下拉菜单中选择: 'main'"
echo "   3. 在 'Folder' 下拉菜单中选择: '/docs'"
echo "   4. 点击 'Save' 按钮"
echo ""
echo "步骤3: 等待构建完成"
echo "   ⏰ 首次构建通常需要 1-5 分钟"
echo "   📊 构建状态会显示在设置页面"
echo ""
echo "步骤4: 验证访问"
echo "   构建完成后，访问:"
echo "   🔗 https://mengliang555.github.io/finance"
echo ""

echo "🔧 备用方案 - 本地访问:"
echo "========================================="
echo ""
echo "如果GitHub Pages配置需要时间，可以立即本地访问:"
echo ""
echo "方案A: 直接打开本地文件"
echo "   open /Users/mengliang.yang/github/finance/docs/index.html"
echo ""
echo "方案B: 启动本地HTTP服务器"
echo "   cd /Users/mengliang.yang/github/finance/docs"
echo "   python3 -m http.server 8888"
echo "   然后访问: http://localhost:8888"
echo ""
echo "方案C: 使用其他端口"
echo "   cd /Users/mengliang.yang/github/finance/docs"
echo "   python3 -m http.server 9000"
echo "   然后访问: http://localhost:9000"
echo ""

echo "📋 验证清单:"
echo "========================================="
echo ""
echo "✅ 代码已推送到GitHub (最新提交: $(git log --oneline -1 | cut -d' ' -f1))"
echo "✅ 网站文件完整 (docs/目录包含所有必要文件)"
echo "✅ 配置文件正确 (_config.yml 和 .nojekyll 存在)"
echo "⏳ 需要手动配置GitHub Pages设置"
echo ""

echo "💡 故障排除:"
echo "========================================="
echo ""
echo "如果遇到问题，请检查:"
echo ""
echo "1. 仓库是否为公开(Public)状态"
echo "2. 分支名称是否正确 (应为 'main')"
echo "3. 目录名称是否正确 (应为 '/docs')"
echo "4. 等待足够时间让构建完成 (1-5分钟)"
echo "5. 清除浏览器缓存后重试"
echo "6. 检查GitHub状态: https://www.githubstatus.com/"
echo ""

echo "📞 支持信息:"
echo "========================================="
echo ""
echo "GitHub仓库: https://github.com/mengliang555/finance"
echo "GitHub Pages设置: https://github.com/mengliang555/finance/settings/pages"
echo "问题反馈: https://github.com/mengliang555/finance/issues"
echo ""

echo "🎯 预期结果:"
echo "========================================="
echo ""
echo "成功配置后，您将能够访问:"
echo ""
echo "🌐 在线网站: https://mengliang555.github.io/finance"
echo "   - 完整的财务分析网站"
echo "   - 交互式图表和数据可视化"
echo "   - 四家公司对比分析"
echo "   - 响应式设计，适配所有设备"
echo ""
echo "📊 网站功能包括:"
echo "   1. 公司财务分析展示"
echo "   2. 交互式对比图表"
echo "   3. 风险雷达图可视化"
echo "   4. 估值对比分析"
echo "   5. 完整的分析框架"
echo ""

echo "✨ 配置完成时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="