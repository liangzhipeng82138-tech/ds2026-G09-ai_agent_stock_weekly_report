"""
T-E2 AI Agent自动生成股市周报 — AI 摘要生成脚本

功能：
1. 读取 data/weekly_data.json 中的本周数据
2. 调用 LLM API 生成市场摘要文字
3. 保存摘要至 data/ai_summary.txt

支持 API:
- Anthropic Claude (默认)
- OpenAI GPT (备选)
"""

import json
import os
from datetime import datetime

# ===== 配置 =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 优先使用 Anthropic Claude，回退到 OpenAI GPT
USE_API = os.environ.get('WEEKLY_REPORT_API', 'anthropic')  # 'anthropic' 或 'openai'


def generate_summary_anthropic(weekly_data: dict) -> str:
    """调用 Anthropic Claude API 生成市场摘要"""
    import anthropic
    
    client = anthropic.Anthropic(
        api_key=os.environ.get('ANTHROPIC_API_KEY')
    )
    
    prompt = f"""
你是一位专业的A股市场分析师，请根据以下本周市场数据，撰写一段400-500字的市场周报摘要。

本周数据：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

要求：
1. 概括六大核心指数涨跌情况，指出最强和最弱指数
2. 分析市场情绪：涨跌家数、赚钱效应、涨跌停分布
3. 点评北向资金流向及其对市场的影响
4. 判断市场整体走势类型（全面上涨/全面下跌/震荡上行/结构性行情等）
5. 简要展望下周需关注的因素
6. 语言专业、客观、简洁，适合机构投资者阅读
7. 不要捏造数据，所有数值必须来自提供的数据
8. 不要使用"根据数据""如上所示"等套话
9. 直接输出正文，不需要标题
"""

    message = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1500,
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return message.content[0].text


def generate_summary_openai(weekly_data: dict) -> str:
    """调用 OpenAI GPT API 生成市场摘要"""
    from openai import OpenAI
    
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY')
    )
    
    prompt = f"""
你是一位专业的A股市场分析师，请根据以下本周市场数据，撰写一段400-500字的市场周报摘要。

本周数据：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

要求：
1. 概括六大核心指数涨跌情况，指出最强和最弱指数
2. 分析市场情绪：涨跌家数、赚钱效应、涨跌停分布
3. 点评北向资金流向及其对市场的影响
4. 判断市场整体走势类型
5. 简要展望下周需关注的因素
6. 语言专业、客观、简洁
7. 不要捏造数据
8. 直接输出正文，不需要标题
"""

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1500,
    )
    
    return response.choices[0].message.content


def generate_summary(weekly_data: dict) -> str:
    """根据配置选择 API 生成摘要"""
    if USE_API == 'anthropic':
        try:
            return generate_summary_anthropic(weekly_data)
        except Exception as e:
            print(f'Anthropic API 调用失败: {e}')
            print('尝试使用 OpenAI API ...')
            return generate_summary_openai(weekly_data)
    else:
        return generate_summary_openai(weekly_data)


def main():
    """主函数"""
    print('=' * 50)
    print('AI Agent 股市周报 — 摘要生成')
    print(f'运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'使用 API: {USE_API}')
    print('=' * 50)
    
    # 加载数据
    data_path = os.path.join(DATA_DIR, 'weekly_data.json')
    if not os.path.exists(data_path):
        print(f'错误: 未找到数据文件 {data_path}')
        print('请先运行 scripts/01_fetch_data.py')
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        weekly_data = json.load(f)
    
    print(f'已加载数据: {len(weekly_data)} 个数据项')
    
    # 生成摘要
    print('正在调用 AI API 生成摘要 ...')
    summary = generate_summary(weekly_data)
    
    # 保存摘要
    output_path = os.path.join(DATA_DIR, 'ai_summary.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f'\n摘要已保存至: {output_path}')
    print(f'摘要字数: {len(summary)}')
    print('\n--- 摘要内容 ---')
    print(summary)
    print('--- END ---')
    print('✓ 摘要生成完成！')


if __name__ == '__main__':
    main()
