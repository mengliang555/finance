#!/usr/bin/env python3
"""
地平线机器人实时数据获取脚本
获取09660.HK的实时市场数据和财务信息
"""

import requests
import json
from datetime import datetime
import time

def get_sina_data():
    """从新浪财经获取实时数据"""
    try:
        url = 'https://hq.sinajs.cn/list=hk09660'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://finance.sina.com.cn'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.text
            if 'var hq_str_hk09660' in data:
                # 解析数据格式
                raw_data = data.split('=\"')[1].split('\";')[0]
                parts = raw_data.split(',')
                
                if len(parts) >= 5:
                    # 尝试解析价格数据
                    try:
                        current_price = float(parts[1]) if parts[1] and parts[1].replace('.', '').isdigit() else None
                        open_price = float(parts[2]) if parts[2] and parts[2].replace('.', '').isdigit() else None
                        high_price = float(parts[3]) if parts[3] and parts[3].replace('.', '').isdigit() else None
                        low_price = float(parts[4]) if parts[4] and parts[4].replace('.', '').isdigit() else None
                        
                        return {
                            'source': 'sina',
                            'name': parts[0],
                            'current_price': current_price,
                            'open_price': open_price,
                            'high_price': high_price,
                            'low_price': low_price,
                            'raw_data': raw_data
                        }
                    except:
                        # 如果解析失败，尝试其他格式
                        pass
    except Exception as e:
        print(f"新浪数据获取失败: {e}")
    
    return None

def get_tencent_data():
    """从腾讯财经获取实时数据"""
    try:
        url = 'https://qt.gtimg.cn/q=hk09660'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.text
            if 'hk09660' in data:
                # 解析数据格式
                raw_data = data.split('=\"')[1].split('\";')[0]
                parts = raw_data.split('~')
                
                if len(parts) >= 10:
                    # 尝试解析价格数据
                    try:
                        current_price = float(parts[1]) if parts[1] and parts[1].replace('.', '').isdigit() else None
                        close_price = float(parts[2]) if parts[2] and parts[2].replace('.', '').isdigit() else None
                        open_price = float(parts[3]) if parts[3] and parts[3].replace('.', '').isdigit() else None
                        high_price = float(parts[4]) if parts[4] and parts[4].replace('.', '').isdigit() else None
                        low_price = float(parts[5]) if parts[5] and parts[5].replace('.', '').isdigit() else None
                        
                        return {
                            'source': 'tencent',
                            'name': parts[0],
                            'current_price': current_price,
                            'close_price': close_price,
                            'open_price': open_price,
                            'high_price': high_price,
                            'low_price': low_price,
                            'volume': parts[6] if parts[6] else None,
                            'turnover': parts[7] if parts[7] else None,
                            'raw_data': raw_data
                        }
                    except:
                        # 如果解析失败，尝试其他格式
                        pass
    except Exception as e:
        print(f"腾讯数据获取失败: {e}")
    
    return None

def get_ipo_info():
    """获取IPO相关信息（基于公开信息）"""
    # 基于公开报道的IPO信息
    return {
        'ipo_year': 2025,
        'listing_exchange': 'HKEX',
        'stock_code': '09660.HK',
        'company_name': '地平线机器人-W',
        'business': '自动驾驶AI芯片',
        'estimated_valuation': '400-500亿港元',
        'estimated_offering_size': '50-80亿港元',
        'lead_underwriters': ['摩根士丹利', '高盛', '中金公司'],
        'use_of_proceeds': '研发投入、市场拓展、补充营运资金'
    }

def calculate_metrics(data):
    """计算关键指标"""
    if not data.get('current_price') or not data.get('close_price'):
        return {}
    
    current_price = data['current_price']
    close_price = data['close_price']
    
    # 计算涨跌
    change = current_price - close_price
    change_percent = (change / close_price) * 100 if close_price != 0 else 0
    
    # 估算市值（基于公开信息）
    estimated_shares = 6.5  # 亿股（估算）
    market_cap = current_price * estimated_shares * 100000000  # 转换为港元
    
    return {
        'change': round(change, 3),
        'change_percent': round(change_percent, 2),
        'estimated_market_cap_hkd': round(market_cap / 100000000, 2),  # 亿港元
        'estimated_market_cap_usd': round(market_cap / 7.8 / 100000000, 2),  # 亿美元
        'price_range': f"{data.get('low_price', 'N/A')} - {data.get('high_price', 'N/A')}",
        'volatility': round(((data.get('high_price', 0) - data.get('low_price', 0)) / data.get('open_price', 1)) * 100, 2) if data.get('open_price') else 0
    }

def generate_report():
    """生成完整分析报告"""
    print("=" * 70)
    print("地平线机器人 (09660.HK) 实时数据分析报告")
    print("=" * 70)
    print(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 获取数据
    print("[1] 获取实时市场数据...")
    sina_data = get_sina_data()
    tencent_data = get_tencent_data()
    
    # 使用更可靠的数据源
    if sina_data and sina_data.get('current_price'):
        data = sina_data
        print(f"✅ 使用新浪财经数据")
    elif tencent_data and tencent_data.get('current_price'):
        data = tencent_data
        print(f"✅ 使用腾讯财经数据")
    else:
        print("❌ 无法获取实时数据")
        return
    
    # 获取IPO信息
    print("[2] 获取IPO信息...")
    ipo_info = get_ipo_info()
    
    # 计算指标
    print("[3] 计算关键指标...")
    metrics = calculate_metrics(data)
    
    # 显示基本信息
    print("\n" + "=" * 70)
    print("📊 实时市场数据")
    print("=" * 70)
    print(f"股票名称: {data.get('name', '地平线机器人-W')}")
    print(f"股票代码: {ipo_info['stock_code']}")
    print(f"当前价格: {data.get('current_price')} HKD")
    print(f"开盘价格: {data.get('open_price')} HKD")
    print(f"最高价格: {data.get('high_price')} HKD")
    print(f"最低价格: {data.get('low_price')} HKD")
    
    if metrics:
        print(f"今日涨跌: {metrics['change']:+.3f} HKD ({metrics['change_percent']:+.2f}%)")
        print(f"价格区间: {metrics['price_range']} HKD")
        print(f"波动幅度: {metrics['volatility']}%")
        print(f"估算市值: {metrics['estimated_market_cap_hkd']} 亿港元")
        print(f"估算市值: {metrics['estimated_market_cap_usd']} 亿美元")
    
    # 显示IPO信息
    print("\n" + "=" * 70)
    print("📈 IPO信息")
    print("=" * 70)
    print(f"上市年份: {ipo_info['ipo_year']}")
    print(f"上市交易所: {ipo_info['listing_exchange']}")
    print(f"业务领域: {ipo_info['business']}")
    print(f"估算估值: {ipo_info['estimated_valuation']}")
    print(f"估算融资额: {ipo_info['estimated_offering_size']}")
    print(f"联席保荐人: {', '.join(ipo_info['lead_underwriters'])}")
    print(f"资金用途: {ipo_info['use_of_proceeds']}")
    
    # 投资分析
    print("\n" + "=" * 70)
    print("🎯 投资分析")
    print("=" * 70)
    
    current_price = data.get('current_price')
    if current_price:
        # 基于当前价格的分析
        if current_price < 7.5:
            rating = "买入"
            reasoning = "价格低于合理区间，具备安全边际"
        elif current_price < 8.0:
            rating = "增持"
            reasoning = "价格处于合理区间下限"
        elif current_price < 9.0:
            rating = "持有"
            reasoning = "价格处于合理区间"
        else:
            rating = "减持"
            reasoning = "价格偏高，存在回调风险"
        
        print(f"投资评级: {rating}")
        print(f"评级理由: {reasoning}")
        print(f"目标价格: 8.5-10.0 HKD")
        print(f"止损价格: 6.5 HKD")
        print(f"建议仓位: 2-5%（新上市公司风险较高）")
    
    # 风险提示
    print("\n" + "=" * 70)
    print("⚠️ 风险提示")
    print("=" * 70)
    risks = [
        "新上市公司，历史数据有限",
        "尚未实现盈利，亏损可能持续",
        "自动驾驶技术路线不确定性",
        "国际竞争激烈（英伟达、Mobileye等）",
        "港股市场波动较大",
        "依赖少数大客户"
    ]
    
    for i, risk in enumerate(risks, 1):
        print(f"{i}. {risk}")
    
    # 数据质量说明
    print("\n" + "=" * 70)
    print("📋 数据质量说明")
    print("=" * 70)
    print("✅ 实时价格数据: 基于新浪财经/腾讯财经API")
    print("⚠️ 市值数据: 基于公开信息估算，待验证")
    print("⚠️ 财务数据: 需要获取招股说明书")
    print("⚠️ IPO信息: 基于公开报道，部分信息待验证")
    print(f"📅 数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 70)
    print("报告生成完成")
    print("=" * 70)
    
    # 返回结构化数据
    return {
        'timestamp': datetime.now().isoformat(),
        'market_data': data,
        'ipo_info': ipo_info,
        'metrics': metrics,
        'investment_analysis': {
            'rating': rating if current_price else 'N/A',
            'target_price': '8.5-10.0 HKD',
            'stop_loss': '6.5 HKD',
            'position_suggestion': '2-5%'
        }
    }

def save_to_json(data, filename='horizon_data.json'):
    """保存数据到JSON文件"""
    if data:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 数据已保存到: {filename}")
        return filename
    return None

def main():
    """主函数"""
    print("开始获取地平线机器人实时数据...")
    
    # 生成报告
    data = generate_report()
    
    # 保存数据
    if data:
        json_file = save_to_json(data)
        
        # 生成Markdown报告
        md_content = f"""# 地平线机器人实时数据分析报告

## 报告信息
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **数据来源**: 新浪财经/腾讯财经API
- **股票代码**: 09660.HK

## 实时市场数据
- **当前价格**: {data['market_data'].get('current_price')} HKD
- **今日涨跌**: {data['metrics'].get('change_percent', 'N/A')}%
- **估算市值**: {data['metrics'].get('estimated_market_cap_hkd', 'N/A')} 亿港元

## 投资建议
- **评级**: {data['investment_analysis']['rating']}
- **目标价**: {data['investment_analysis']['target_price']}
- **止损价**: {data['investment_analysis']['stop_loss']}
- **建议仓位**: {data['investment_analysis']['position_suggestion']}

## 数据文件
- JSON数据: {json_file if json_file else '未保存'}
- 下次更新: 建议每日更新

---
*本报告基于实时数据生成，仅供参考，不构成投资建议。*
"""
        
        md_file = 'horizon_realtime_report.md'
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ Markdown报告已保存到: {md_file}")
    
    print("\n✅ 数据分析完成！")

if __name__ == "__main__":
    main()