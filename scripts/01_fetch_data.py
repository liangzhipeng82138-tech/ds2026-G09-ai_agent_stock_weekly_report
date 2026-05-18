"""
01_fetch_data.py - 数据获取脚本
通过akshare和yfinance获取A股和美股主要指数、行业、资金流向等周度数据

| 项目   | 内容 |
|--------|------|
| 课程   | 数据分析与经济决策（ds2026） |
| 题目   | T-E2：AI Agent自动生成股市周报 |
| 小组   | 第09组 |
| 成员   | 梁志鹏（25210177）、吴璇子（25210264）、黄悦（25210145）、王鹤洋（25210243）、柯骋（25210150）、罗天（25210207） |
| GitHub | https://github.com/liangzhipeng82138-tech/ds2026-G09-ai_agent_stock_weekly_report |
| Pages  | https://liangzhipeng82138-tech.github.io/ds2026-G09-ai_agent_stock_weekly_report/ |
| 日期   | 2026-05-15 |
"""

import akshare as ak
import yfinance as yf
import json
import pandas as pd
from datetime import datetime, timedelta


def get_a_share_indices():
    """获取A股主要指数周度数据"""
    indices = {
        '上证指数': 'sh000001',
        '深证成指': 'sz399001',
        '创业板指': 'sz399006',
        '科创50': 'sh000688',
        '沪深300': 'sh000300',
        '中证500': 'sh000905',
    }
    result = {}
    for name, symbol in indices.items():
        try:
            df = ak.stock_zh_index_daily(symbol=symbol)
            df = df.tail(10)
            weekly_return = (df['close'].iloc[-1] / df['close'].iloc[-6] - 1) * 100
            amplitude = ((df['high'].iloc[-5:].max() - df['low'].iloc[-5:].min()) / df['close'].iloc[-6]) * 100
            result[name] = {
                'close': float(df['close'].iloc[-1]),
                'prev_close': float(df['close'].iloc[-6]),
                'change_pct': round(float(weekly_return), 2),
                'amplitude': round(float(amplitude), 2),
                'date': str(df.index[-1]) if hasattr(df.index, '__getitem__') else str(datetime.now().date())
            }
            print(f'  ✅ {name}: 收盘{result[name]["close"]}, 周涨跌{result[name]["change_pct"]}%')
        except Exception as e:
            print(f'  ❌ {name}获取失败：{e}')
    return result


def get_us_indices():
    """获取美股三大指数数据"""
    tickers = {
        '标普500': '^GSPC',
        '纳斯达克': '^IXIC',
        '道琼斯': '^DJI',
    }
    result = {}
    for name, ticker in tickers.items():
        try:
            data = yf.download(ticker, period='10d', progress=False)
            if len(data) >= 6:
                weekly_return = (data['Close'].iloc[-1] / data['Close'].iloc[-6] - 1) * 100
                result[name] = {
                    'close': round(float(data['Close'].iloc[-1]), 2),
                    'prev_close': round(float(data['Close'].iloc[-6]), 2),
                    'change_pct': round(float(weekly_return), 2),
                }
                print(f'  ✅ {name}: 收盘{result[name]["close"]}, 周涨跌{result[name]["change_pct"]}%')
        except Exception as e:
            print(f'  ❌ {name}获取失败：{e}')
    return result


def get_sw_sectors():
    """获取申万一级行业涨跌幅数据"""
    try:
        # 尝试获取申万行业数据
        df = ak.sw_index_daily_indicator(symbol='801010', indicator='近一周')
        return df.to_dict(orient='records')
    except Exception as e:
        print(f'  ⚠️ 行业数据获取失败：{e}，将使用备选方案')
        return []


def get_northbound_data():
    """获取北向资金数据"""
    try:
        df = ak.stock_em_hsgt_north_net_flow_in_em(symbol="北向资金")
        recent = df.tail(5)
        return {
            'weekly_net_flow': float(recent['当日净买入'].sum()),
            'daily_data': recent.to_dict(orient='records')
        }
    except Exception as e:
        print(f'  ⚠️ 北向资金数据获取失败：{e}')
        return {}


def get_weekly_data():
    """主函数：获取本周市场全量数据"""
    print('=' * 50)
    print('📊 开始获取周度市场数据...')
    print('=' * 50)

    data = {
        'report_info': {
            'title': 'A股 & 美股周报',
            'subtitle': f'第{datetime.now().isocalendar()[1]}周（{(datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")} 至 {datetime.now().strftime("%Y-%m-%d")}）',
            'author': 'ds2026 第09组',
            'date': datetime.now().strftime('%Y-%m-%d'),
        }
    }

    print('\n📈 [1/4] 获取A股主要指数...')
    data['a_share_indices'] = get_a_share_indices()

    print('\n📈 [2/4] 获取美股主要指数...')
    data['us_indices'] = get_us_indices()

    print('\n📊 [3/4] 获取申万行业数据...')
    data['sw_sectors'] = get_sw_sectors()

    print('\n💰 [4/4] 获取北向资金数据...')
    data['northbound'] = get_northbound_data()

    # 保存数据
    output_path = '../data/weekly_data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    print(f'\n✅ 数据获取完成！已保存至 {output_path}')
    print(f'   共获取 {len(data)} 个数据维度')
    return data


if __name__ == '__main__':
    get_weekly_data()
