"""
T-E2 AI Agent自动生成股市周报 — 数据获取脚本

功能：
1. 获取六大核心指数日线行情（上证/深证/创业板/科创50/沪深300/中证500）
2. 获取全市场涨跌家数和涨跌停数据
3. 获取北向资金流向数据
4. 获取两市成交额数据
5. 获取美股三大指数作为外围参考

输出：data/weekly_data.json + data_raw/ 目录下各CSV文件
"""

import akshare as ak
import yfinance as yf
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta


# ===== 配置 =====
INDEX_MAP = {
    '上证指数': 'sh000001',
    '深证成指': 'sz399001',
    '创业板指': 'sz399006',
    '科创50':  'sh000688',
    '沪深300': 'sh000300',
    '中证500': 'sh000905',
}

US_INDEX = {
    '道琼斯': '^DJI',
    '标普500': '^GSPC',
    '纳斯达克': '^IXIC',
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data_raw')
DATA_DIR = os.path.join(BASE_DIR, 'data')


def ensure_dirs():
    """创建必要的目录"""
    for d in [DATA_RAW_DIR, DATA_DIR, os.path.join(DATA_DIR, 'history')]:
        os.makedirs(d, exist_ok=True)
    print(f'目录已就绪: {DATA_RAW_DIR}, {DATA_DIR}')


def fetch_index_data():
    """获取A股核心指数日线数据"""
    results = {}
    
    for name, code in INDEX_MAP.items():
        try:
            print(f'正在获取 {name} ({code}) ...')
            df = ak.stock_zh_index_daily(symbol=code)
            df = df.tail(15).copy()
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            # 保存原始数据
            raw_path = os.path.join(DATA_RAW_DIR, f'index_{name}.csv')
            df.to_csv(raw_path, index=False, encoding='utf-8-sig')
            
            # 计算本周指标
            if len(df) >= 6:
                this_week_close = float(df['close'].iloc[-1])
                last_week_close = float(df['close'].iloc[-6])
                weekly_return = (this_week_close / last_week_close - 1) * 100
                
                this_week_high = float(df.tail(5)['high'].max())
                this_week_low = float(df.tail(5)['low'].min())
                amplitude = (this_week_high - this_week_low) / last_week_close * 100
                
                results[name] = {
                    'close': this_week_close,
                    'last_week_close': last_week_close,
                    'change_pct': round(weekly_return, 2),
                    'amplitude': round(amplitude, 2),
                    'date': str(df['date'].iloc[-1].strftime('%Y-%m-%d')),
                }
            
            print(f'  ✓ {name}: 收盘={results.get(name, {}).get("close", "N/A")}, 涨跌幅={results.get(name, {}).get("change_pct", "N/A")}%')
            time.sleep(0.5)  # 避免请求过快
            
        except Exception as e:
            print(f'  ✗ {name} 获取失败: {e}')
            results[name] = None
    
    return results


def fetch_market_sentiment():
    """获取全市场涨跌家数统计"""
    try:
        print('正在获取全市场行情 ...')
        spot_df = ak.stock_zh_a_spot_em()
        
        # 保存原始数据
        raw_path = os.path.join(DATA_RAW_DIR, 'stock_spot_all.csv')
        spot_df.to_csv(raw_path, index=False, encoding='utf-8-sig')
        
        # 统计涨跌家数
        change_col = None
        for col in spot_df.columns:
            if '涨跌幅' in str(col):
                change_col = col
                break
        
        if change_col:
            valid = spot_df.dropna(subset=[change_col])
            rise = int((valid[change_col] > 0).sum())
            fall = int((valid[change_col] < 0).sum())
            flat = int((valid[change_col] == 0).sum())
            limit_up = int((valid[change_col] >= 9.9).sum())
            limit_down = int((valid[change_col] <= -9.9).sum())
            
            sentiment = {
                'rise_count': rise,
                'fall_count': fall,
                'flat_count': flat,
                'limit_up': limit_up,
                'limit_down': limit_down,
                'profit_rate': round(rise / len(valid) * 100, 1),
            }
            print(f'  ✓ 上涨{rise}家, 下跌{fall}家, 涨停{limit_up}, 跌停{limit_down}')
            return sentiment
        else:
            print(f'  ✗ 未找到涨跌幅列, 可用列: {list(spot_df.columns)}')
            return None
            
    except Exception as e:
        print(f'  ✗ 市场情绪获取失败: {e}')
        return None


def fetch_northbound_flow():
    """获取北向资金流向数据"""
    try:
        print('正在获取北向资金数据 ...')
        nb_df = ak.stock_hsgt_north_net_flow_in_em(symbol='北向')
        nb_df = nb_df.tail(15).copy()
        
        # 保存原始数据
        raw_path = os.path.join(DATA_RAW_DIR, 'northbound_flow.csv')
        nb_df.to_csv(raw_path, index=False, encoding='utf-8-sig')
        
        # 提取本周数据
        weekly_data = nb_df.tail(5).to_dict(orient='records')
        print(f'  ✓ 北向资金: 获取到 {len(nb_df)} 条记录')
        return weekly_data
        
    except Exception as e:
        print(f'  ✗ 北向资金获取失败: {e}')
        return []


def fetch_us_index():
    """获取美股三大指数数据"""
    results = {}
    
    for name, ticker in US_INDEX.items():
        try:
            print(f'正在获取 {name} ({ticker}) ...')
            df = yf.download(ticker, period='15d', progress=False)
            if not df.empty:
                close = float(df['Close'].iloc[-1])
                prev_close = float(df['Close'].iloc[-6]) if len(df) >= 6 else close
                change_pct = (close / prev_close - 1) * 100
                
                results[name] = {
                    'close': round(close, 2),
                    'change_pct': round(change_pct, 2),
                }
                print(f'  ✓ {name}: 收盘={close:.2f}, 涨跌幅={change_pct:+.2f}%')
        except Exception as e:
            print(f'  ✗ {name} 获取失败: {e}')
            results[name] = None
    
    return results


def main():
    """主函数：获取所有数据并保存"""
    print('=' * 50)
    print('AI Agent 股市周报 — 数据获取')
    print(f'运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 50)
    
    ensure_dirs()
    
    # 获取数据
    index_data = fetch_index_data()
    sentiment = fetch_market_sentiment()
    northbound = fetch_northbound_flow()
    us_data = fetch_us_index()
    
    # 汇总为 JSON
    weekly_data = {
        'report_date': datetime.now().strftime('%Y-%m-%d'),
        'period': {
            'start': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'end': datetime.now().strftime('%Y-%m-%d'),
        },
        'indices': {k: v for k, v in index_data.items() if v is not None},
        'sentiment': sentiment,
        'northbound': northbound,
        'us_indices': {k: v for k, v in us_data.items() if v is not None},
    }
    
    # 保存
    output_path = os.path.join(DATA_DIR, 'weekly_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(weekly_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f'\n数据已保存至: {output_path}')
    print(f'数据项: {len(weekly_data)} 个')
    print('✓ 数据获取完成！')


if __name__ == '__main__':
    main()
