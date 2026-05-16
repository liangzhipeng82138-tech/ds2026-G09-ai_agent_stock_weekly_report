#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资金流向数据获取脚本
使用 akshare 获取真实市场数据
"""

import akshare as ak
import json
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def get_north_money_flow():
    """获取北向资金流向数据"""
    try:
        # 北向资金流向
        north_money = ak.stock_em_hsgt_north_net_flow_in(symbol="北向资金", indicator="今日")
        print(f"北向资金数据获取成功: {len(north_money)} 条记录")
        return north_money.to_dict(orient='records')
    except Exception as e:
        print(f"北向资金获取失败: {e}")
        return []

def get_main_force_flow():
    """获取主力资金流向"""
    try:
        # 主力资金流向
        main_force = ak.stock_individual_fund_flow(stock="北向资金")
        print(f"主力资金数据获取成功: {len(main_force)} 条记录")
        return main_force.to_dict(orient='records')
    except Exception as e:
        print(f"主力资金获取失败: {e}")
        return []

def get_sector_money_flow():
    """获取行业资金流向"""
    try:
        # 申万行业资金流向
        sector = ak.stock_sector_fund_flow_rank(indicator="今日", sector_type="行业资金流向")
        print(f"行业资金数据获取成功: {len(sector)} 条记录")
        return sector.to_dict(orient='records')
    except Exception as e:
        print(f"行业资金获取失败: {e}")
        return []

def get_market_capital():
    """获取市场成交额数据"""
    try:
        # A股市场成交额
        market = ak.stock_zh_a_spot_em()
        total_turnover = market['成交额'].sum() if '成交额' in market.columns else 0
        print(f"市场成交额获取成功: {total_turnover/1e8:.2f} 亿元")
        return float(total_turnover/1e8)
    except Exception as e:
        print(f"市场成交额获取失败: {e}")
        return 0

def get_ggt_stock():
    """获取沪深港通数据"""
    try:
        ggt = ak.stock_hsgt_north_hold_stock_em(symbol="北向", indicator="北向持股数", date=datetime.now().strftime("%Y%m%d"))
        print(f"沪深港通持股数据获取成功: {len(ggt)} 条记录")
        return ggt.to_dict(orient='records')
    except Exception as e:
        print(f"沪深港通获取失败: {e}")
        return []

def get_margin_trading():
    """获取融资融券数据"""
    try:
        margin = ak.stock_margin_detail_szse(date=datetime.now().strftime("%Y%m%d"))
        print(f"融资融券数据获取成功: {len(margin)} 条记录")
        return margin.to_dict(orient='records')
    except Exception as e:
        print(f"融资融券获取失败: {e}")
        return []

def main():
    print("=" * 50)
    print("开始获取资金流向数据...")
    print("=" * 50)
    
    data = {
        "更新时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "北向资金": get_north_money_flow(),
        "主力资金": get_main_force_flow(),
        "行业资金": get_sector_money_flow(),
        "市场成交额": get_market_capital(),
        "沪深港通持股": get_ggt_stock(),
        "融资融券": get_margin_trading()
    }
    
    # 保存数据
    output_file = "../data/fund_flow_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, ensure_ascii=False, indent=2, default=str)
    
    print("=" * 50)
    print(f"数据已保存到 {output_file}")
    print("=" * 50)
    
    return data

if __name__ == "__main__":
    main()
