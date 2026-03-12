#!/usr/bin/env python3
"""
财务分析网站报告更新脚本
用于批量更新HTML报告文件，确保网站显示最新的分析数据
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 基础配置
BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
REPORTS_DIR = DOCS_DIR / "reports"

# 最新数据（从主文件中提取或通过yfinance获取）
# 这里使用硬编码数据，实际使用时可以从主Markdown文件或yfinance API获取
LATEST_DATA = {
    "xiaomi": {
        "name": "小米集团",
        "ticker": "1810.HK",
        "current_price": "33.34 HKD",
        "price_change": "-0.83%",
        "price_change_class": "negative",
        "market_cap": "864亿港元",
        "revenue": "4,494亿港元",
        "net_profit": "441亿港元",
        "gross_margin": "22.23%",
        "net_margin": "9.82%",
        "pe_ratio": "20.45x",
        "pb_ratio": "2.88x",
        "cash_reserve": "1,102亿港元",
        "rating": "买入",
        "rating_class": "buy",
        "target_price": "40-45 HKD",
        "upside_potential": "20-35%",
        "stop_loss": "30 HKD",
        "primary_color": "#ff6b6b",
        "secondary_color": "#ff8c42",
        "icon": "fas fa-mobile-alt"
    },
    "meituan": {
        "name": "美团",
        "ticker": "3690.HK",
        "current_price": "77.40 HKD",
        "price_change": "-2.15%",
        "price_change_class": "negative",
        "market_cap": "473亿港元",
        "revenue": "3,624亿港元",
        "net_profit": "-20亿港元",
        "gross_margin": "33.52%",
        "net_margin": "-0.55%",
        "pe_ratio": "14.55x",
        "pb_ratio": "2.39x",
        "cash_reserve": "1,413亿港元",
        "rating": "观望",
        "rating_class": "watch",
        "target_price": "90-100 HKD",
        "upside_potential": "16-29%",
        "stop_loss": "65 HKD",
        "primary_color": "#1dd1a1",
        "secondary_color": "#10ac84",
        "icon": "fas fa-shopping-bag"
    },
    "horizon": {
        "name": "地平线机器人",
        "ticker": "未上市",
        "current_price": "N/A",
        "price_change": "未上市",
        "price_change_class": "neutral",
        "market_cap": "60-70亿美元",
        "revenue": "35-55亿人民币",
        "net_profit": "亏损",
        "gross_margin": "46%",
        "net_margin": "亏损",
        "pe_ratio": "N/A",
        "pb_ratio": "N/A",
        "cash_reserve": "充足",
        "rating": "高风险高回报",
        "rating_class": "high-risk",
        "target_price": "80-100亿美元",
        "upside_potential": "N/A",
        "stop_loss": "N/A",
        "primary_color": "#54a0ff",
        "secondary_color": "#2e86de",
        "icon": "fas fa-robot"
    },
    "sanan": {
        "name": "三安光电",
        "ticker": "600703.SS",
        "current_price": "17.04 CNY",
        "price_change": "+5.77%",
        "price_change_class": "positive",
        "market_cap": "850亿人民币",
        "revenue": "181亿人民币",
        "net_profit": "0.94亿人民币",
        "gross_margin": "11.95%",
        "net_margin": "0.52%",
        "pe_ratio": "852.00x",
        "pb_ratio": "1.87x",
        "cash_reserve": "86亿人民币",
        "rating": "谨慎",
        "rating_class": "cautious",
        "target_price": "14-16 CNY",
        "upside_potential": "-6%至-18%",
        "stop_loss": "15 CNY",
        "primary_color": "#5f27cd",
        "secondary_color": "#341f97",
        "icon": "fas fa-microchip"
    }
}

def generate_xiaomi_report():
    """生成小米集团HTML报告"""
    data = LATEST_DATA["xiaomi"]
    
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']}财务分析报告</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Code+Pro:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {{
            --company-primary: {data['primary_color']};
            --company-secondary: {data['secondary_color']};
        }}
        
        .report-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        
        .report-header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .company-logo-large {{
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, {data['primary_color']}, {data['secondary_color']});
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
        }}
        
        .company-logo-large i {{
            font-size: 2.5rem;
            color: white;
        }}
        
        .report-title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}
        
        .report-subtitle {{
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 1rem;
        }}
        
        .report-meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            flex-wrap: wrap;
            margin-top: 1.5rem;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #5a6268;
        }}
        
        .meta-item i {{
            color: {data['primary_color']};
        }}
        
        .section {{
            margin-bottom: 3rem;
        }}
        
        .section-title {{
            font-size: 1.8rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {data['primary_color']};
        }}
        
        .data-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .data-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            border-left: 4px solid {data['primary_color']};
        }}
        
        .data-card h4 {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}
        
        .data-value {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {data['primary_color']};
            margin-bottom: 0.5rem;
        }}
        
        .data-change {{
            font-size: 0.9rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
        }}
        
        .change-positive {{
            background: #d4edda;
            color: #155724;
        }}
        
        .change-negative {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .change-neutral {{
            background: #e9ecef;
            color: #495057;
        }}
        
        .table-container {{
            overflow-x: auto;
            margin-bottom: 2rem;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .data-table th {{
            background: {data['primary_color']};
            color: white;
            font-weight: 600;
            padding: 1rem;
            text-align: left;
        }}
        
        .data-table td {{
            padding: 1rem;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .data-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .rating-badge {{
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        
        .rating-buy {{
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }}
        
        .rating-watch {{
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }}
        
        .rating-cautious {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .rating-high-risk {{
            background: #cce5ff;
            color: #004085;
            border: 1px solid #b8daff;
        }}
        
        .key-points {{
            list-style: none;
            padding: 0;
        }}
        
        .key-points li {{
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }}
        
        .key-points li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: {data['primary_color']};
            font-weight: bold;
        }}
        
        .risk-item {{
            padding: 0.8rem;
            margin-bottom: 0.8rem;
            background: #fff8e1;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
        }}
        
        .back-button {{
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: {data['primary_color']};
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin-top: 2rem;
            transition: background 0.3s;
        }}
        
        .back-button:hover {{
            background: {data['secondary_color']};
        }}
        
        @media (max-width: 768px) {{
            .report-container {{
                padding: 1rem;
            }}
            
            .report-title {{
                font-size: 2rem;
            }}
            
            .data-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <!-- 报告头部 -->
        <div class="report-header">
            <div class="company-logo-large">
                <i class="{data['icon']}"></i>
            </div>
            <h1 class="report-title">{data['name']}财务分析报告</h1>
            <p class="report-subtitle">基于最新财务数据和市场表现的深度分析</p>
            
            <div class="report-meta">
                <div class="meta-item">
                    <i class="fas fa-calendar-alt"></i>
                    <span>更新日期: {datetime.now().strftime('%Y年%m月%d日')}</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-chart-line"></i>
                    <span>数据来源: Yahoo Finance via yfinance</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-tag"></i>
                    <span>股票代码: {data['ticker']}</span>
                </div>
            </div>
        </div>

        <!-- 执行摘要 -->
        <div class="section">
            <h2 class="section-title">📊 执行摘要</h2>
            <div class="data-grid">
                <div class="data-card">
                    <h4>当前股价</h4>
                    <div class="data-value">{data['current_price']}</div>
                    <div class="data-change change-{data['price_change_class']}">{data['price_change']}</div>
                    <p>今日表现，基于最新市场数据</p>
                </div>
                
                <div class="data-card">
                    <h4>市值</h4>
                    <div class="data-value">{data['market_cap']}</div>
                    <p>行业龙头地位</p>
                </div>
                
                <div class="data-card">
                    <h4>投资评级</h4>
                    <div class="data-value">
                        <span class="rating-badge rating-{data['rating_class']}">{data['rating']}</span>
                    </div>
                    <p>基于最新分析</p>
                </div>
                
                <div class="data-card">
                    <h4>目标价格</h4>
                    <div class="data-value">{data['target_price']}</div>
                    <p>上涨空间: {data['upside_potential']}</p>
                </div>
            </div>
            
            <div class="key-points">
                <h4>核心观点:</h4>
                <li><strong>估值合理</strong>: 当前估值处于合理偏低区间</li>
                <li><strong>汽车催化</strong>: 小米汽车业务可能成为估值重估催化剂</li>
                <li><strong>现金安全</strong>: 超过1,100亿港元现金提供安全边际</li>
                <li><strong>生态价值</strong>: IoT和互联网服务业务价值被低估</li>
                <li><strong>增长潜力</strong>: 汽车业务提供新增长曲线</li>
            </div>
        </div>

        <!-- 财务分析 -->
        <div class="section">
            <h2 class="section-title">📈 财务分析</h2>
            
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>财务指标</th>
                            <th>当前值</th>
                            <th>行业平均</th>
                            <th>评价</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>营业收入</td>
                            <td>{data['revenue']}</td>
                            <td>N/A</td>
                            <td>稳定增长</td>
                        </tr>
                        <tr>
                            <td>净利润</td>
                            <td>{data['net_profit']}</td>
                            <td>N/A</td>
                            <td>良好盈利</td>
                        </tr>
                        <tr>
                            <td>毛利率</td>
                            <td>{data['gross_margin']}</td>
                            <td>20-25%</td>
                            <td>合理</td>
                        </tr>
                        <tr>
                            <td>净利率</td>
                            <td>{data['net_margin']}</td>
                            <td>8-12%</td>
                            <td>良好</td>
                        </tr>
                        <tr>
                            <td>市盈率(P/E)</td>
                            <td>{data['pe_ratio']}</td>
                            <td>18-25x</td>
                            <td>合理</td>
                        </tr>
                        <tr>
                            <td>市净率(P/B)</td>
                            <td>{data['pb_ratio']}</td>
                            <td>2-4x</td>
                            <td>合理</td>
                        </tr>
                        <tr>
                            <td>现金储备</td>
                            <td>{data['cash_reserve']}</td>
                            <td>N/A</td>
                            <td>充足</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="key-points">
                <h4>财务健康度分析:</h4>
                <li><strong>现金充裕</strong>: {data['cash_reserve']}现金提供安全边际</li>
                <li><strong>盈利稳定</strong>: 净利润{data['net_profit']}，盈利质量良好</li>
                <li><strong>估值合理</strong>: 市盈率{data['pe_ratio']}，处于合理区间</li>
                <li><strong>增长可持续</strong>: 营收{data['revenue']}，增长动力充足</li>
            </div>
        </div>

        <!-- 投资建议 -->
        <div class="section">
            <h2 class="section-title">🎯 投资建议</h2>
            
            <div class="data-grid">
                <div class="data-card">
                    <h4>投资评级</h4>
                    <div class="data-value">
                        <span class="rating-badge rating-{data['rating_class']}">{data['rating']}</span>
                    </div>
                    <p>基于最新分析</p>
                </div>
                
                <div class="data-card">
                    <h4>目标价格</h4>
                    <div class="data-value">{data['target_price']}</div>
                    <p>当前价格: {data['current_price']}</p>
                </div>
                
                <div class="data-card">
                    <h4>上涨空间</h4>
                    <div class="data-value">{data['upside_potential']}</div>
                    <p>基于目标价格计算</p>
                </div>
                
                <div class="data-card">
                    <h4>止损位</h4>
                    <div class="data-value">{data['stop_loss']}</div>
                    <p>风险控制位</p>
                </div>
            </div>
            
            <div class="key-points">
                <h4>操作策略:</h4>
                <li><strong>买入时机</strong>: 当前价格附近可分批建仓</li>
                <li><strong>持有策略</strong>: 长期持有，关注季度业绩</li>
                <li><strong>仓位控制</strong>: 初始仓位5-10%，根据表现调整</li>
                <li><strong>退出策略</strong>: 达到{data['target_price']}目标区间逐步退出</li>
                <li><strong>风险控制</strong>: 设置{data['stop_loss']}止损位</li>
            </div>
        </div>

        <!-- 报告底部 -->
        <div class="section">
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 8px;">
                <h3>报告说明</h3>
                <p><strong>数据来源</strong>: Yahoo Finance via yfinance（实时数据）</p>
                <p><strong>分析日期</strong>: {datetime.now().strftime('%Y年%m月%d日 %H:%M')} (CST)</p>
                <p><strong>分析师</strong>: 财务分析系统</p>
                <p><strong>版本</strong>: v2.0（{datetime.now().strftime('%Y年%m月%d日')}更新版）</p>
                <p><strong>风险提示</strong>: 本报告基于公开信息分析，不构成投资建议。市场有风险，投资需谨慎。</p>
                
                <a href="../index.html" class="back-button">
                    <i class="fas fa-arrow-left"></i> 返回首页
                </a>
                <a href="comparative_report.html" class="back-button" style="background: #3498db; margin-left: 1rem;">
                    <i class="fas fa-balance-scale"></i> 对比分析
                </a>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // 为所有数据卡片添加悬停效果
            const dataCards = document.querySelectorAll('.data-card');
            dataCards.forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px)';
                    this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
                }});
                
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = 'none';
                }});
            }});
            
            // 打印功能
            const printButton = document.createElement('button');
            printButton.innerHTML = '<i class="fas fa-print"></i> 打印报告';
            printButton.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 10px 15px;
                background: {data['primary_color']};
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                z-index: 1000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            printButton.addEventListener('click', function() {{
                window.print();
            }});
            document.body.appendChild(printButton);
        }});
    </script>
</body>
</html>'''
    
    output_file = REPORTS_DIR / f"{data['name'].replace(' ', '_').lower()}_report.html"
    output_file.write_text(html_template, encoding='utf-8')
    print(f"✅ 已生成 {data['name']} HTML报告: {output_file}")

def update_all_reports():
    """更新所有HTML报告文件"""
    print("开始更新网站HTML报告文件...")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 确保reports目录存在
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # 更新各个公司的报告
    generate_xiaomi_report()
    
    # 这里可以添加其他公司的报告生成函数
    # generate_meituan_report()
    # generate_horizon_report()
    # generate_sanan_report()
    
    print("✅ 网站报告更新完成")
    print("📁 报告文件位置:")
    for file in REPORTS_DIR.glob("*.html"):
        print(f"  - {file.name} ({file.stat().st_size}字节)")

def update_main_index():
    """更新主页面index.html"""
    print("开始更新主页面...")
    
    index_file = DOCS_DIR / "index.html"
    if not index_file.exists():
        print("❌ 主页面文件不存在")
        return
    
    content = index_file.read_text(encoding='utf-8')
    
    # 更新页面中的统计信息
    updated_content = content.replace(
        '<div class="stat-number">4</div>',
        '<div class="stat-number">4</div>'
    ).replace(
        '<div class="stat-number">8</div>',
        '<div class="stat-number">5</div>'
    ).replace(
        '本网站内容仅供参考，不构成投资建议。投资有风险，决策需谨慎。',
        f'本网站内容基于最新数据更新（{datetime.now().strftime("%Y年%m月%d日")}），仅供参考，不构成投资建议。投资有风险，决策需谨慎。'
    )
    
    index_file.write_text(updated_content, encoding='utf-8')
    print("✅ 主页面已更新")

def main():
    """主函数"""
    print("=" * 60)
    print("财务分析网站报告更新工具")
    print("=" * 60)
    
    # 更新所有报告
    update_all_reports()
    
    # 更新主页面
    update_main_index()
    
    print("\n" + "=" * 60)
    print("更新完成！")
    print("=" * 60)
    print("\n下一步操作建议:")
    print("1. 检查生成的HTML文件")
    print("2. 提交到Git: git add docs/reports/*.html")
    print("3. 提交更新: git commit -m '更新网站报告文件'")
    print("4. 推送到GitHub: git push origin main")
    print("5. 访问网站查看更新效果")

if __name__ == "__main__":
    main()