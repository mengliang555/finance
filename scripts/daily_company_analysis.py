#!/usr/bin/env python3
"""
每日公司分析脚本
每天6点自动分析小米、美团、地平线机器人、三安光电四家公司
生成分析报告并存储到指定目录
"""

import os
import sys
import json
import datetime
import yfinance as yf
from pathlib import Path
import pandas as pd
import numpy as np

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 配置
COMPANIES = {
    'xiaomi': {
        'name': '小米集团',
        'ticker': '1810.HK',
        'market': '港股',
        'industry': '消费电子/智能硬件'
    },
    'meituan': {
        'name': '美团',
        'ticker': '3690.HK',
        'market': '港股',
        'industry': '本地生活服务'
    },
    'horizon': {
        'name': '地平线机器人',
        'ticker': '09660.HK',
        'market': '港股',
        'industry': '自动驾驶/AI芯片'
    },
    'sanan': {
        'name': '三安光电',
        'ticker': '600703.SS',
        'market': 'A股',
        'industry': 'LED芯片/化合物半导体'
    }
}

# 输出目录
OUTPUT_DIR = project_root / 'data' / 'daily_analysis'
REPORTS_DIR = project_root / 'reports' / 'daily_analysis'
LOG_DIR = project_root / 'logs'

def setup_directories():
    """创建必要的目录"""
    for directory in [OUTPUT_DIR, REPORTS_DIR, LOG_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    print(f"✅ 目录已创建: {OUTPUT_DIR}, {REPORTS_DIR}, {LOG_DIR}")

def get_stock_data(ticker, period='1d'):
    """获取股票数据"""
    try:
        stock = yf.Ticker(ticker)
        
        # 获取历史数据
        hist = stock.history(period=period)
        
        # 获取基本信息
        info = stock.info
        
        # 获取新闻
        news = stock.news if hasattr(stock, 'news') else []
        
        return {
            'history': hist.to_dict() if not hist.empty else {},
            'info': info,
            'news': news[:5] if news else [],  # 只取最近5条新闻
            'success': True
        }
    except Exception as e:
        print(f"❌ 获取 {ticker} 数据失败: {str(e)}")
        return {
            'history': {},
            'info': {},
            'news': [],
            'success': False,
            'error': str(e)
        }

def analyze_company(company_id, company_info):
    """分析单个公司"""
    print(f"📊 开始分析 {company_info['name']} ({company_info['ticker']})...")
    
    ticker = company_info['ticker']
    analysis_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 获取数据
    data = get_stock_data(ticker, period='5d')  # 获取5天数据
    
    if not data['success']:
        return {
            'company_id': company_id,
            'company_name': company_info['name'],
            'ticker': ticker,
            'analysis_date': analysis_date,
            'success': False,
            'error': data.get('error', '未知错误')
        }
    
    # 分析历史数据
    hist_data = data['history']
    info = data['info']
    
    # 提取关键指标
    analysis = {
        'company_id': company_id,
        'company_name': company_info['name'],
        'ticker': ticker,
        'market': company_info['market'],
        'industry': company_info['industry'],
        'analysis_date': analysis_date,
        'analysis_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'success': True
    }
    
    # 价格分析
    if hist_data and 'Close' in hist_data and hist_data['Close']:
        closes = list(hist_data['Close'].values())
        if closes:
            current_price = closes[-1]
            prev_price = closes[0] if len(closes) > 1 else current_price
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price * 100) if prev_price != 0 else 0
            
            analysis['price'] = {
                'current': round(current_price, 2),
                'previous': round(prev_price, 2),
                'change': round(price_change, 2),
                'change_pct': round(price_change_pct, 2),
                'trend': '上涨' if price_change > 0 else '下跌' if price_change < 0 else '持平'
            }
    
    # 基本信息分析
    if info:
        analysis['fundamentals'] = {
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'pb_ratio': info.get('priceToBook'),
            'dividend_yield': info.get('dividendYield'),
            'beta': info.get('beta'),
            'volume': info.get('volume'),
            'avg_volume': info.get('averageVolume')
        }
    
    # 新闻分析
    if data['news']:
        analysis['recent_news'] = []
        for news_item in data['news']:
            analysis['recent_news'].append({
                'title': news_item.get('title', ''),
                'publisher': news_item.get('publisher', ''),
                'link': news_item.get('link', ''),
                'published': news_item.get('providerPublishTime', '')
            })
    
    # 生成分析结论
    analysis['conclusion'] = generate_conclusion(analysis)
    
    print(f"✅ {company_info['name']} 分析完成")
    return analysis

def generate_conclusion(analysis):
    """生成分析结论"""
    conclusions = []
    
    # 价格趋势分析
    if 'price' in analysis:
        price_info = analysis['price']
        if price_info['change_pct'] > 2:
            conclusions.append(f"股价表现强劲，今日上涨{price_info['change_pct']}%")
        elif price_info['change_pct'] < -2:
            conclusions.append(f"股价承压，今日下跌{abs(price_info['change_pct'])}%")
        else:
            conclusions.append(f"股价相对稳定，波动{abs(price_info['change_pct'])}%")
    
    # 基本面分析
    if 'fundamentals' in analysis:
        fundamentals = analysis['fundamentals']
        
        # PE比率分析
        pe = fundamentals.get('pe_ratio')
        if pe:
            if pe < 15:
                conclusions.append("估值较低，PE比率处于合理区间")
            elif pe > 30:
                conclusions.append("估值较高，需关注盈利增长")
        
        # 市值分析
        market_cap = fundamentals.get('market_cap')
        if market_cap:
            if market_cap > 100e9:  # 1000亿以上
                conclusions.append("大盘股，流动性好")
            elif market_cap < 10e9:  # 100亿以下
                conclusions.append("中小盘股，成长空间大")
    
    # 新闻影响分析
    if 'recent_news' in analysis and analysis['recent_news']:
        news_count = len(analysis['recent_news'])
        conclusions.append(f"近期有{news_count}条相关新闻，关注市场情绪")
    
    # 行业分析
    industry = analysis.get('industry', '')
    if 'AI' in industry or '芯片' in industry:
        conclusions.append("属于AI/半导体赛道，长期成长性看好")
    elif '消费' in industry:
        conclusions.append("消费类公司，关注宏观经济影响")
    
    if not conclusions:
        conclusions.append("数据有限，建议进一步分析")
    
    return conclusions

def save_analysis_results(analysis_results):
    """保存分析结果"""
    analysis_date = datetime.datetime.now().strftime('%Y%m%d')
    
    # 保存JSON数据
    json_file = OUTPUT_DIR / f'daily_analysis_{analysis_date}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    print(f"✅ 分析数据已保存: {json_file}")
    
    # 生成Markdown报告
    md_file = REPORTS_DIR / f'daily_analysis_report_{analysis_date}.md'
    generate_markdown_report(analysis_results, md_file)
    print(f"✅ Markdown报告已生成: {md_file}")
    
    # 生成摘要报告
    summary_file = REPORTS_DIR / f'daily_summary_{analysis_date}.md'
    generate_summary_report(analysis_results, summary_file)
    print(f"✅ 摘要报告已生成: {summary_file}")
    
    return {
        'json_file': str(json_file),
        'md_file': str(md_file),
        'summary_file': str(summary_file)
    }

def generate_markdown_report(analysis_results, output_file):
    """生成详细的Markdown报告"""
    analysis_date = datetime.datetime.now().strftime('%Y年%m月%d日')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 每日公司分析报告\n\n")
        f.write(f"**分析日期**: {analysis_date}\n")
        f.write(f"**生成时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**分析公司数量**: {len(analysis_results)}\n\n")
        
        f.write("---\n\n")
        
        # 总体概览
        f.write("## 📊 总体概览\n\n")
        successful = sum(1 for r in analysis_results if r.get('success', False))
        f.write(f"- **成功分析**: {successful} 家公司\n")
        f.write(f"- **失败分析**: {len(analysis_results) - successful} 家公司\n")
        f.write(f"- **分析时段**: 每日18:00自动执行\n\n")
        
        f.write("---\n\n")
        
        # 各公司详细分析
        f.write("## 🏢 各公司详细分析\n\n")
        
        for result in analysis_results:
            if not result.get('success', False):
                continue
                
            f.write(f"### {result['company_name']} ({result['ticker']})\n\n")
            
            # 基本信息
            f.write(f"**市场**: {result['market']} | **行业**: {result['industry']}\n")
            f.write(f"**分析时间**: {result['analysis_time']}\n\n")
            
            # 价格信息
            if 'price' in result:
                price = result['price']
                trend_emoji = '📈' if price['trend'] == '上涨' else '📉' if price['trend'] == '下跌' else '➡️'
                f.write(f"#### 价格表现 {trend_emoji}\n\n")
                f.write(f"- **当前价格**: {price['current']}\n")
                f.write(f"- **价格变化**: {price['change']} ({price['change_pct']}%)\n")
                f.write(f"- **趋势**: {price['trend']}\n\n")
            
            # 基本面信息
            if 'fundamentals' in result:
                fund = result['fundamentals']
                f.write("#### 基本面指标\n\n")
                
                if fund.get('market_cap'):
                    market_cap_b = fund['market_cap'] / 1e9
                    f.write(f"- **市值**: {market_cap_b:.2f}B\n")
                
                if fund.get('pe_ratio'):
                    f.write(f"- **PE比率**: {fund['pe_ratio']:.2f}\n")
                
                if fund.get('pb_ratio'):
                    f.write(f"- **PB比率**: {fund['pb_ratio']:.2f}\n")
                
                if fund.get('dividend_yield'):
                    f.write(f"- **股息率**: {fund['dividend_yield']:.2%}\n")
                
                if fund.get('volume') and fund.get('avg_volume'):
                    volume_ratio = fund['volume'] / fund['avg_volume'] if fund['avg_volume'] > 0 else 1
                    f.write(f"- **成交量比率**: {volume_ratio:.2f}\n")
                
                f.write("\n")
            
            # 分析结论
            if 'conclusion' in result:
                f.write("#### 分析结论\n\n")
                for conclusion in result['conclusion']:
                    f.write(f"- {conclusion}\n")
                f.write("\n")
            
            # 近期新闻
            if 'recent_news' in result and result['recent_news']:
                f.write("#### 近期新闻\n\n")
                for news in result['recent_news'][:3]:  # 只显示最近3条
                    f.write(f"- **{news['title']}**\n")
                    if news.get('publisher'):
                        f.write(f"  *来源: {news['publisher']}*\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        # 失败分析的公司
        failed_companies = [r for r in analysis_results if not r.get('success', False)]
        if failed_companies:
            f.write("## ⚠️ 分析失败的公司\n\n")
            for result in failed_companies:
                f.write(f"- **{result['company_name']}** ({result['ticker']})\n")
                f.write(f"  *错误: {result.get('error', '未知错误')}*\n")
            f.write("\n")
        
        # 投资建议
        f.write("## 💡 投资建议\n\n")
        f.write("### 短期关注 (1-3天)\n\n")
        f.write("1. **价格趋势**: 关注今日涨跌幅较大的公司\n")
        f.write("2. **成交量**: 关注异常成交量的公司\n")
        f.write("3. **新闻影响**: 关注有重大新闻的公司\n\n")
        
        f.write("### 中期关注 (1-4周)\n\n")
        f.write("1. **基本面变化**: 关注财报季和业绩预告\n")
        f.write("2. **行业动态**: 关注行业政策和竞争格局变化\n")
        f.write("3. **市场情绪**: 关注整体市场风险偏好\n\n")
        
        f.write("### 风险提示\n\n")
        f.write("1. **市场风险**: 股市有风险，投资需谨慎\n")
        f.write("2. **数据延迟**: 部分数据可能有15分钟延迟\n")
        f.write("3. **分析局限**: 本分析基于公开数据，仅供参考\n\n")
        
        # 数据来源和说明
        f.write("## 📋 数据来源和说明\n\n")
        f.write("1. **数据来源**: Yahoo Finance API\n")
        f.write("2. **更新频率**: 每日18:00自动更新\n")
        f.write("3. **数据延迟**: 实时数据，部分数据可能有延迟\n")
        f.write("4. **分析工具**: Python + yfinance库\n")
        f.write("5. **报告生成**: 自动生成，人工审核建议\n\n")
        
        # 联系方式
        f.write("## 📞 联系方式\n\n")
        f.write("如有问题或建议，请通过以下方式联系：\n\n")
        f.write("- **GitHub**: https://github.com/mengliang555/finance\n")
        f.write("- **项目主页**: https://mengliang555.github.io/finance/\n")
        f.write("- **报告目录**: https://mengliang555.github.io/finance/reports_index.html\n")

def generate_summary_report(analysis_results, output_file):
    """生成摘要报告"""
    analysis_date = datetime.datetime.now().strftime('%Y年%m月%d日')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 每日分析摘要\n\n")
        f.write(f"**日期**: {analysis_date}\n")
        f.write(f"**时间**: {datetime.datetime.now().strftime('%H:%M')}\n\n")
        
        f.write("## 📈 今日表现概览\n\n")
        
        successful_results = [r for r in analysis_results if r.get('success', False)]
        
        if successful_results:
            # 计算总体表现
            price_changes = []
            for result in successful_results:
                if 'price' in result:
                    price_changes.append(result['price']['change_pct'])
            
            if price_changes:
                avg_change = sum(price_changes) / len(price_changes)
                up_count = sum(1 for p in price_changes if p > 0)
                down_count = sum(1 for p in price_changes if p < 0)
                
                f.write(f"- **平均涨跌幅**: {avg_change:.2f}%\n")
                f.write(f"- **上涨公司**: {up_count}家\n")
                f.write(f"- **下跌公司**: {down_count}家\n")
                f.write(f"- **持平公司**: {len(price_changes) - up_count - down_count}家\n\n")
            
            # 各公司简要信息
            f.write("## 🏢 各公司简要\n\n")
            
            for result in successful_results:
                company_emoji = '📱' if '小米' in result['company_name'] else \
                               '🛵' if '美团' in result['company_name'] else \
                               '🤖' if '地平线' in result['company_name'] else \
                               '💡' if '三安' in result['company_name'] else '🏢'
                
                f.write(f"### {company_emoji} {result['company_name']}\n\n")
                
                if 'price' in result:
                    price = result['price']
                    trend_emoji = '📈' if price['trend'] == '上涨' else '📉' if price['trend'] == '下跌' else '➡️'
                    f.write(f"- **价格**: {price['current']} ({trend_emoji} {price['change_pct']}%)\n")
                
                if 'conclusion' in result and result['conclusion']:
                    f.write(f"- **要点**: {result['conclusion'][0]}\n")
                
                f.write("\n")
        
        # 今日重点关注
        f.write("## 🔍 今日重点关注\n\n")
        
        if successful_results:
            # 找出涨跌幅最大的公司
            max_up = max(successful_results, 
                        key=lambda x: x.get('price', {}).get('change_pct', -100) 
                        if 'price' in x else -100)
            max_down = min(successful_results, 
                          key=lambda x: x.get('price', {}).get('change_pct', 100) 
                          if 'price' in x else 100)
            
            if 'price' in max_up:
                f.write(f"1. **涨幅最大**: {max_up['company_name']} (+{max_up['price']['change_pct']}%)\n")
            
            if 'price' in max_down:
                f.write(f"2. **跌幅最大**: {max_down['company_name']} ({max_down['price']['change_pct']}%)\n")
        
        f.write("3. **行业动态**: 关注AI芯片和消费电子板块\n")
        f.write("4. **市场情绪**: 关注港股通资金流向\n\n")
        
        # 操作建议
        f.write("## 🎯 操作建议\n\n")
        f.write("### 建议关注\n\n")
        f.write("1. **趋势跟踪**: 关注连续上涨/下跌的公司\n")
        f.write("2. **价值发现**: 关注估值合理的公司\n")
        f.write("3. **事件驱动**: 关注有重大新闻的公司\n\n")
        
        f.write("### 风险控制\n\n")
        f.write("1. **仓位管理**: 建议分散投资\n")
        f.write("2. **止损设置**: 设置合理的止损位\n")
        f.write("3. **持续跟踪**: 每日关注分析报告\n\n")
        
        # 下次分析时间
        next_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y年%m月%d日')
        f.write(f"## ⏰ 下次分析时间\n\n")
        f.write(f"**计划时间**: {next_date} 06:00\n")
        f.write(f"**分析公司**: 小米、美团、地平线机器人、三安光电\n")

def log_analysis(analysis_results, file_paths):
    """记录分析日志"""
    log_date = datetime.datetime.now().strftime('%Y%m%d')
    log_file = LOG_DIR / f'analysis_log_{log_date}.json'
    
    log_entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'companies_analyzed': len(analysis_results),
        'successful_analysis': sum(1 for r in analysis_results if r.get('success', False)),
        'failed_analysis': sum(1 for r in analysis_results if not r.get('success', False)),
        'output_files': file_paths,
        'results_summary': []
    }
    
    # 添加简要结果
    for result in analysis_results:
        if result.get('success', False):
            summary = {
                'company': result['company_name'],
                'ticker': result['ticker'],
                'price_change': result.get('price', {}).get('change_pct', 0)
            }
            log_entry['results_summary'].append(summary)
    
    # 保存日志
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_entry, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 分析日志已保存: {log_file}")
    return str(log_file)

def main():
    """主函数"""
    print("=" * 60)
    print("📊 每日公司分析脚本")
    print(f"📅 分析时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 1. 设置目录
        setup_directories()
        
        # 2. 分析各公司
        analysis_results = []
        for company_id, company_info in COMPANIES.items():
            result = analyze_company(company_id, company_info)
            analysis_results.append(result)
        
        # 3. 保存分析结果
        file_paths = save_analysis_results(analysis_results)
        
        # 4. 记录日志
        log_file = log_analysis(analysis_results, file_paths)
        
        # 5. 输出总结
        successful = sum(1 for r in analysis_results if r.get('success', False))
        print("\n" + "=" * 60)
        print("🎉 分析完成总结")
        print("=" * 60)
        print(f"✅ 分析公司: {len(COMPANIES)}家")
        print(f"✅ 成功分析: {successful}家")
        print(f"✅ 失败分析: {len(COMPANIES) - successful}家")
        print(f"✅ 数据文件: {file_paths['json_file']}")
        print(f"✅ 详细报告: {file_paths['md_file']}")
        print(f"✅ 摘要报告: {file_paths['summary_file']}")
        print(f"✅ 分析日志: {log_file}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ 分析过程出错: {str(e)}")
        
        # 记录错误日志
        error_log = LOG_DIR / f'error_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        with open(error_log, 'w', encoding='utf-8') as f:
            f.write(f"错误时间: {datetime.datetime.now().isoformat()}\n")
            f.write(f"错误信息: {str(e)}\n")
            import traceback
            f.write(f"堆栈跟踪:\n{traceback.format_exc()}\n")
        
        print(f"📝 错误日志: {error_log}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)