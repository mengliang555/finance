// 报告中心JavaScript文件

// 报告数据
const reports = [
    // 公司分析报告
    {
        id: 'xiaomi',
        title: '小米集团财务分析报告',
        category: 'company',
        description: '深度分析小米集团的财务表现、业务发展和投资价值，包括智能手机、IoT、汽车等业务分析。',
        icon: 'fas fa-mobile-alt',
        iconColor: 'linear-gradient(135deg, #ff6b6b, #ff8e8e)',
        date: '2026-03-11',
        size: '15.2KB',
        rawPath: 'reports/company_analysis/xiaomi_financial_analysis.md'
    },
    {
        id: 'meituan',
        title: '美团财务分析报告',
        category: 'company',
        description: '全面分析美团的本地生活服务平台业务，包括外卖、到店服务、酒店旅游等业务分析。',
        icon: 'fas fa-shopping-bag',
        iconColor: 'linear-gradient(135deg, #4ecdc4, #6de5dd)',
        date: '2026-03-11',
        size: '14.8KB',
        rawPath: 'reports/company_analysis/meituan_financial_analysis.md'
    },
    {
        id: 'horizon',
        title: '地平线机器人财务分析报告',
        category: 'company',
        description: '基于真实上市数据的自动驾驶AI芯片公司分析，包括技术优势、市场机会和投资建议。',
        icon: 'fas fa-robot',
        iconColor: 'linear-gradient(135deg, #45b7d1, #67c9e0)',
        date: '2026-03-11',
        size: '12.5KB',
        rawPath: 'reports/company_analysis/horizon_robotics_financial_analysis.md'
    },
    {
        id: 'sanan',
        title: '三安光电财务分析报告',
        category: 'company',
        description: 'LED芯片全球龙头和化合物半导体领先企业的财务分析和业务展望。',
        icon: 'fas fa-microchip',
        iconColor: 'linear-gradient(135deg, #96ceb4, #b4e6d2)',
        date: '2026-03-11',
        size: '11.9KB',
        rawPath: 'reports/company_analysis/sanan_opto_financial_analysis.md'
    },
    {
        id: 'zhongchong',
        title: '中宠股份深度分析报告',
        category: 'company',
        description: '宠物食品龙头企业深度分析，包括财务表现、行业前景、投资建议等全面分析。',
        icon: 'fas fa-paw',
        iconColor: 'linear-gradient(135deg, #ff9f43, #ffb872)',
        date: '2026-03-19',
        size: '9.3KB',
        rawPath: 'reports/zhongchong_analysis_20260319.md'
    },
    
    // 行业分析报告
    {
        id: 'comparative',
        title: '四家公司对比分析报告',
        category: 'industry',
        description: '小米、美团、地平线机器人、三安光电四家公司在财务指标、业务模式、风险特征等方面的全面对比。',
        icon: 'fas fa-balance-scale',
        iconColor: 'linear-gradient(135deg, #feca57, #ffd98c)',
        date: '2026-03-11',
        size: '18.3KB',
        rawPath: 'reports/industry_analysis/comparative_analysis.md'
    },
    {
        id: 'power-grid',
        title: '电力设备和电网领域分析',
        category: 'industry',
        description: '分析电力设备、电网建设、特高压、智能电网等领域的投资机会和上市公司推荐。',
        icon: 'fas fa-bolt',
        iconColor: 'linear-gradient(135deg, #ff9ff3, #ffc2f7)',
        date: '2026-03-12',
        size: '8.6KB',
        rawPath: 'reports/industry_analysis/power_equipment_grid.md'
    },
    
    // 每日报告
    {
        id: 'daily-20260312',
        title: '2026年3月12日股票表现报告',
        category: 'daily',
        description: '总结小米集团、美团、地平线机器人三只关注股票的今日涨幅情况和市场分析。',
        icon: 'fas fa-calendar-day',
        iconColor: 'linear-gradient(135deg, #54a0ff, #7bb9ff)',
        date: '2026-03-12',
        size: '4.6KB',
        rawPath: 'reports/daily_reports/daily_stock_performance_20260312.md'
    },
    
    // AI分析报告
    {
        id: 'deepseek-open',
        title: 'DeepSeek V4开源影响分析',
        category: 'ai',
        description: '分析DeepSeek V4如果开源对A股和港股上市公司的影响，重点关注AI算力和应用公司。',
        icon: 'fas fa-brain',
        iconColor: 'linear-gradient(135deg, #5f27cd, #7d4ce8)',
        date: '2026-03-12',
        size: '6.3KB',
        rawPath: 'reports/ai_analysis/deepseek_v4_open_source_analysis.md'
    },
    {
        id: 'deepseek-huawei',
        title: 'DeepSeek V4华为升腾芯片训练影响分析',
        category: 'ai',
        description: '分析如果DeepSeek V4使用华为升腾芯片训练，对华为昇腾产业链和国产AI芯片生态的影响。',
        icon: 'fas fa-microchip',
        iconColor: 'linear-gradient(135deg, #00d2d3, #2de9ea)',
        date: '2026-03-12',
        size: '6.5KB',
        rawPath: 'reports/ai_analysis/deepseek_v4_huawei_ascend_analysis.md'
    },
    
    // 指南文档
    {
        id: 'framework',
        title: '公司分析框架指南',
        category: 'guides',
        description: '系统化的公司财务分析方法论，适用于各种类型和规模的公司分析。',
        icon: 'fas fa-sitemap',
        iconColor: 'linear-gradient(135deg, #ff9f43, #ffb872)',
        date: '2026-03-11',
        size: '8.4KB',
        rawPath: 'guides/company_analysis_framework.md'
    },
    {
        id: 'access-guide',
        title: '项目访问指南',
        category: 'guides',
        description: '财务分析项目的使用指南，包括网站访问、报告查看、数据更新等说明。',
        icon: 'fas fa-book',
        iconColor: 'linear-gradient(135deg, #1dd1a1, #4be9c9)',
        date: '2026-03-11',
        size: '4.3KB',
        rawPath: 'guides/ACCESS_GUIDE.md'
    },
    {
        id: 'markdown-guide',
        title: 'Markdown报告在线查看指南',
        category: 'guides',
        description: '详细介绍如何在网站上查看和渲染Markdown格式的分析报告，包括使用方法和技术实现。',
        icon: 'fas fa-file-code',
        iconColor: 'linear-gradient(135deg, #9b59b6, #b57cc6)',
        date: '2026-03-12',
        size: '5.4KB',
        rawPath: 'guides/MARKDOWN_REPORTS_GUIDE.md'
    }
];

// DOM元素引用
let reportsGrid, emptyState, reportViewer, viewerTitle, viewerContent, viewerClose;
let filterButtons, navLinks;
let companyCount, industryCount, dailyCount, aiCount;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 获取DOM元素
    reportsGrid = document.getElementById('reportsGrid');
    emptyState = document.getElementById('emptyState');
    reportViewer = document.getElementById('reportViewer');
    viewerTitle = document.getElementById('viewerTitle');
    viewerContent = document.getElementById('viewerContent');
    viewerClose = document.getElementById('viewerClose');
    filterButtons = document.querySelectorAll('.filter-btn');
    navLinks = document.querySelectorAll('.nav-link[data-category]');
    
    // 统计元素
    companyCount = document.getElementById('companyCount');
    industryCount = document.getElementById('industryCount');
    dailyCount = document.getElementById('dailyCount');
    aiCount = document.getElementById('aiCount');
    
    // 初始化功能
    updateStats();
    renderReports('all');
    setupEventListeners();
    setupNavLinks();
});

// 更新统计信息
function updateStats() {
    const companyReports = reports.filter(r => r.category === 'company').length;
    const industryReports = reports.filter(r => r.category === 'industry').length;
    const dailyReports = reports.filter(r => r.category === 'daily').length;
    const aiReports = reports.filter(r => r.category === 'ai').length;
    
    companyCount.textContent = companyReports;
    industryCount.textContent = industryReports;
    dailyCount.textContent = dailyReports;
    aiCount.textContent = aiReports;
}

// 渲染报告卡片
function renderReports(category) {
    reportsGrid.innerHTML = '';
    emptyState.style.display = 'none';
    
    const filteredReports = category === 'all' 
        ? reports 
        : reports.filter(report => report.category === category);
    
    if (filteredReports.length === 0) {
        reportsGrid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    reportsGrid.style.display = 'grid';
    
    filteredReports.forEach((report, index) => {
        const card = document.createElement('div');
        card.className = 'report-card fade-in slide-up';
        card.style.animationDelay = `${index * 0.05}s`;
        card.dataset.id = report.id;
        card.dataset.category = report.category;
        
        card.innerHTML = `
            <div class="report-header">
                <div class="report-icon" style="background: ${report.iconColor}">
                    <i class="${report.icon}"></i>
                </div>
                <div class="report-info">
                    <h3 class="report-title">${report.title}</h3>
                    <span class="report-category">${getCategoryName(report.category)}</span>
                </div>
            </div>
            <p class="report-description">${report.description}</p>
            <div class="report-meta">
                <div class="meta-info">
                    <span class="meta-item">
                        <i class="far fa-calendar"></i>
                        ${report.date}
                    </span>
                    <span class="meta-item">
                        <i class="far fa-file"></i>
                        ${report.size}
                    </span>
                </div>
                <button class="report-action" onclick="viewReport('${report.id}')">
                    <i class="fas fa-eye"></i>
                    查看报告
                </button>
            </div>
        `;
        
        reportsGrid.appendChild(card);
    });
}

// 获取分类名称
function getCategoryName(category) {
    const names = {
        'company': '公司分析',
        'industry': '行业分析',
        'daily': '每日报告',
        'ai': 'AI分析',
        'guides': '指南文档'
    };
    return names[category] || category;
}

// 查看报告
async function viewReport(reportId) {
    const report = reports.find(r => r.id === reportId);
    if (!report) return;
    
    // 更新查看器标题
    viewerTitle.textContent = report.title;
    
    // 显示查看器
    reportViewer.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // 显示加载状态
    viewerContent.innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <span>正在加载报告内容...</span>
        </div>
    `;
    
    try {
        // 使用GitHub raw文件URL
        const rawUrl = `https://raw.githubusercontent.com/mengliang555/finance/main/${report.rawPath}`;
        
        // 获取Markdown内容
        const response = await fetch(rawUrl);
        if (!response.ok) {
            throw new Error(`HTTP错误: ${response.status}`);
        }
        
        const markdown = await response.text();
        
        // 使用marked.js渲染Markdown
        const html = marked.parse(markdown);
        
        // 使用DOMPurify清理HTML
        const cleanHtml = DOMPurify.sanitize(html);
        
        // 更新查看器内容
        viewerContent.innerHTML = cleanHtml;
        
        // 添加样式增强
        enhanceMarkdownStyles();
        
    } catch (error) {
        console.error('加载报告失败:', error);
        viewerContent.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <div style="font-size: 3rem; color: #ef4444; margin-bottom: 20px;">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3 style="color: #1e293b; margin-bottom: 10px;">加载失败</h3>
                <p style="color: #64748b; margin-bottom: 20px;">无法加载报告内容：${error.message}</p>
                <p style="font-size: 0.9em; color: #94a3b8; margin-bottom: 20px;">
                    请确保文件已提交到GitHub仓库，并且网络连接正常。
                </p>
                <button onclick="viewReport('${reportId}')" style="padding: 10px 20px; background: #4f46e5; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 500;">
                    <i class="fas fa-redo"></i> 重试加载
                </button>
            </div>
        `;
    }
}

// 增强Markdown样式
function enhanceMarkdownStyles() {
    // 为表格添加响应式包装
    const tables = viewerContent.querySelectorAll('table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        wrapper.style.overflowX = 'auto';
        wrapper.style.marginBottom = '1em';
        wrapper.style.borderRadius = '8px';
        wrapper.style.border = '1px solid var(--border-color)';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });
    
    // 为代码块添加语言标签
    const codeBlocks = viewerContent.querySelectorAll('pre code');
    codeBlocks.forEach(block => {
        const language = block.className.replace('language-', '') || 'text';
        const header = document.createElement('div');
        header.className = 'code-header';
        header.style.background = '#1e293b';
        header.style.color = '#e2e8f0';
        header.style.padding = '8px 16px';
        header.style.borderTopLeftRadius = '8px';
        header.style.borderTopRightRadius = '8px';
        header.style.fontFamily = "'Source Code Pro', monospace";
        header.style.fontSize = '0.9em';
        header.style.fontWeight = '500';
        header.style.display = 'flex';
        header.style.justifyContent = 'space-between';
        header.style.alignItems = 'center';
        header.innerHTML = `
            <span>${language}</span>
            <button onclick="copyCode(this)" style="background: rgba(255,255,255,0.1); border: none; color: #e2e8f0; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 0.8em;">
                <i class="fas fa-copy"></i> 复制
            </button>
        `;
        
        const pre = block.parentNode;
        pre.parentNode.insertBefore(header, pre);
        pre.style.marginTop = '0';
        pre.style.borderTopLeftRadius = '0';
        pre.style.borderTopRightRadius = '0';
    });
}

// 复制代码功能
function copyCode(button) {
    const codeBlock = button.closest('.code-header').nextElementSibling;
    const code = codeBlock.querySelector('code').textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> 已复制';
        button.style.background = '#10b981';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = 'rgba(255,255,255,0.1)';
        }, 2000);
    });
}

// 设置事件监听器
function setupEventListeners() {
    // 关闭查看器
    viewerClose.addEventListener('click', closeViewer);
    
    // 点击查看器背景关闭
    reportViewer.addEventListener('click', (e) => {
        if (e.target === reportViewer) {
            closeViewer();
        }
    });
    
    // ESC键关闭查看器
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && reportViewer.classList.contains('active')) {
            closeViewer();
        }
    });
    
    // 分类筛选
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // 更新按钮状态
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // 渲染对应分类的报告
            const category = button.dataset.category;
            renderReports(category);
        });
    });
    
    // 卡片点击事件
    reportsGrid.addEventListener('click', (e) => {
        const card = e.target.closest('.report-card');
        if (card && !e.target.closest('.report-action')) {
            const reportId = card.dataset.id;
            viewReport(reportId);
        }
    });
}

// 设置导航链接
function setupNavLinks() {
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // 更新导航链接状态
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            link.classList.add('active');
            
            // 更新筛选按钮状态
            const category = link.dataset.category;
            filterButtons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.category === category) {
                    btn.classList.add('active');
                }
            });
            
            // 渲染对应分类的报告
            renderReports(category);
        });
    });
}

// 关闭查看器
function closeViewer() {
    reportViewer.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// 暴露函数到全局作用域
window.viewReport = viewReport;
window.copyCode = copyCode;
window.closeViewer = closeViewer;