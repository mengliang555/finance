// 财务分析网站主JavaScript文件

document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    initCharts();
    
    // 初始化标签页
    initTabs();
    
    // 初始化平滑滚动
    initSmoothScroll();
    
    // 初始化导航栏高亮
    initNavHighlight();
    
    // 初始化公司卡片交互
    initCompanyCards();
});

// 初始化图表
function initCharts() {
    // 风险雷达图
    const riskCtx = document.getElementById('riskRadar');
    if (riskCtx) {
        const riskChart = new Chart(riskCtx, {
            type: 'radar',
            data: {
                labels: ['行业风险', '竞争风险', '技术风险', '监管风险', '财务风险'],
                datasets: [
                    {
                        label: '小米集团',
                        data: [7, 8, 6, 5, 3],
                        backgroundColor: 'rgba(255, 105, 0, 0.2)',
                        borderColor: 'rgba(255, 105, 0, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(255, 105, 0, 1)'
                    },
                    {
                        label: '美团',
                        data: [7, 8, 4, 9, 3],
                        backgroundColor: 'rgba(255, 195, 0, 0.2)',
                        borderColor: 'rgba(255, 195, 0, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(255, 195, 0, 1)'
                    },
                    {
                        label: '地平线机器人',
                        data: [9, 8, 9, 6, 5],
                        backgroundColor: 'rgba(0, 184, 148, 0.2)',
                        borderColor: 'rgba(0, 184, 148, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(0, 184, 148, 1)'
                    },
                    {
                        label: '三安光电',
                        data: [8, 7, 8, 5, 5],
                        backgroundColor: 'rgba(9, 132, 227, 0.2)',
                        borderColor: 'rgba(9, 132, 227, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(9, 132, 227, 1)'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        pointLabels: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            font: {
                                size: 12
                            }
                        },
                        ticks: {
                            backdropColor: 'transparent',
                            color: 'rgba(255, 255, 255, 0.6)',
                            font: {
                                size: 10
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                }
            }
        });
    }

    // 估值对比图
    const valuationCtx = document.getElementById('valuationChart');
    if (valuationCtx) {
        const valuationChart = new Chart(valuationCtx, {
            type: 'bar',
            data: {
                labels: ['小米集团', '美团', '地平线机器人', '三安光电'],
                datasets: [
                    {
                        label: 'P/E比率',
                        data: [16.5, 27.5, null, 27.5],
                        backgroundColor: [
                            'rgba(255, 105, 0, 0.8)',
                            'rgba(255, 195, 0, 0.8)',
                            'rgba(0, 184, 148, 0.3)',
                            'rgba(9, 132, 227, 0.8)'
                        ],
                        borderColor: [
                            'rgba(255, 105, 0, 1)',
                            'rgba(255, 195, 0, 1)',
                            'rgba(0, 184, 148, 0.5)',
                            'rgba(9, 132, 227, 1)'
                        ],
                        borderWidth: 1
                    },
                    {
                        label: 'P/S比率',
                        data: [1.1, 3.5, 18, 3.5],
                        backgroundColor: [
                            'rgba(255, 105, 0, 0.6)',
                            'rgba(255, 195, 0, 0.6)',
                            'rgba(0, 184, 148, 0.8)',
                            'rgba(9, 132, 227, 0.6)'
                        ],
                        borderColor: [
                            'rgba(255, 105, 0, 1)',
                            'rgba(255, 195, 0, 1)',
                            'rgba(0, 184, 148, 1)',
                            'rgba(9, 132, 227, 1)'
                        ],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'rgba(255, 255, 255, 0.8)'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: 'white',
                        bodyColor: 'white',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1
                    }
                }
            }
        });
    }

    // 营收趋势图（英雄区域）
    const revenueCtx = document.getElementById('revenue-chart');
    if (revenueCtx) {
        // 创建模拟的营收趋势图
        const revenueChart = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: ['2021', '2022', '2023', '2024', '2025'],
                datasets: [
                    {
                        label: '小米集团',
                        data: [3283, 2800, 2710, 3100, 3500],
                        borderColor: 'rgba(255, 105, 0, 1)',
                        backgroundColor: 'rgba(255, 105, 0, 0.1)',
                        borderWidth: 2,
                        tension: 0.4
                    },
                    {
                        label: '美团',
                        data: [1791, 2200, 2400, 2600, 3000],
                        borderColor: 'rgba(255, 195, 0, 1)',
                        backgroundColor: 'rgba(255, 195, 0, 0.1)',
                        borderWidth: 2,
                        tension: 0.4
                    },
                    {
                        label: '三安光电',
                        data: [125, 140, 155, 190, 235],
                        borderColor: 'rgba(9, 132, 227, 1)',
                        backgroundColor: 'rgba(9, 132, 227, 0.1)',
                        borderWidth: 2,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: '#374151',
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                if (value >= 1000) {
                                    return (value / 1000) + 'k';
                                }
                                return value;
                            }
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'nearest'
                }
            }
        });
    }
}

// 初始化标签页
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // 移除所有标签的active类
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // 添加当前标签的active类
            this.classList.add('active');
            
            // 显示对应的内容
            const targetContent = document.getElementById(`${tabId}-tab`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// 初始化平滑滚动
function initSmoothScroll() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                // 更新导航栏active状态
                updateNavActive(targetId);
                
                // 平滑滚动到目标位置
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// 更新导航栏active状态
function updateNavActive(targetId) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === targetId) {
            link.classList.add('active');
        }
    });
}

// 初始化导航栏高亮
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollY >= (sectionTop - 150)) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// 初始化公司卡片交互
function initCompanyCards() {
    const companyCards = document.querySelectorAll('.company-card');
    
    companyCards.forEach(card => {
        // 鼠标悬停效果
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
        });
        
        // 点击效果
        card.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                const reportLink = this.querySelector('a[href$=".md"]');
                if (reportLink) {
                    reportLink.click();
                }
            }
        });
    });
}

// 添加加载动画
function showLoading() {
    const loading = document.createElement('div');
    loading.id = 'loading';
    loading.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-chart-line"></i>
            <p>加载分析数据...</p>
        </div>
    `;
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    
    const spinner = loading.querySelector('.loading-spinner');
    spinner.style.cssText = `
        text-align: center;
        color: #2563eb;
    `;
    
    spinner.querySelector('i').style.cssText = `
        font-size: 3rem;
        margin-bottom: 1rem;
        animation: spin 1s linear infinite;
    `;
    
    document.body.appendChild(loading);
    
    // 添加旋转动画
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
    
    return loading;
}

function hideLoading(loading) {
    if (loading) {
        loading.style.opacity = '0';
        loading.style.transition = 'opacity 0.3s';
        setTimeout(() => {
            loading.remove();
        }, 300);
    }
}

// 模拟数据加载
window.addEventListener('load', function() {
    const loading = showLoading();
    
    // 模拟数据加载延迟
    setTimeout(() => {
        hideLoading(loading);
    }, 1000);
});

// 添加复制功能
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> 已复制';
                    this.classList.add('copied');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('copied');
                    }, 2000);
                });
            }
        });
    });
}

// 添加打印功能
function initPrintButton() {
    const printBtn = document.getElementById('print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
}

// 添加主题切换功能
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            const icon = this.querySelector('i');
            if (document.body.classList.contains('dark-theme')) {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
                localStorage.setItem('theme', 'dark');
            } else {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
                localStorage.setItem('theme', 'light');
            }
        });
        
        // 检查本地存储的主题设置
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            const icon = themeToggle.querySelector('i');
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        }
    }
}

// 初始化所有功能
function initAll() {
    initCharts();
    initTabs();
    initSmoothScroll();
    initNavHighlight();
    initCompanyCards();
    initCopyButtons();
    initPrintButton();
    initThemeToggle();
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
} else {
    initAll();
}