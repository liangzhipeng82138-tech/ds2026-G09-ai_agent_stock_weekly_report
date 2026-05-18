"""
02_generate_summary.py - AI摘要生成脚本
调用LLM API根据周度数据生成市场分析摘要

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

import json
import os
from pathlib import Path


def generate_market_summary(weekly_data: dict) -> str:
    """
    调用AI API生成市场摘要
    支持Anthropic Claude或OpenAI GPT
    """
    # 尝试使用Anthropic Claude
    anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')

    prompt = f"""
你是一位专业的金融分析师，请根据以下本周市场数据，
撰写一段300-400字的市场周报摘要，风格专业、客观、简洁。

本周数据：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

要求：
1. 概括主要指数涨跌情况
2. 点评2-3个表现突出的行业及可能原因
3. 简要展望下周需要关注的因素
4. 不要使用「根据数据」「如上所示」等套话
5. 直接输出正文，不需要标题
6. 不要捏造数据，只使用提供的数据
"""

    if anthropic_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            message = client.messages.create(
                model='claude-sonnet-4-20250514',
                max_tokens=1000,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f'⚠️ Claude API调用失败：{e}')

    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f'⚠️ OpenAI API调用失败：{e}')

    # 降级方案：返回基于数据的模板摘要
    print('⚠️ API不可用，使用模板生成摘要')
    return generate_template_summary(weekly_data)


def generate_template_summary(data: dict) -> str:
    """降级方案：基于数据模板生成摘要（无需API）"""
    indices = data.get('a_share_indices', {})
    summary_parts = []

    # 指数概览
    up_indices = [(k, v) for k, v in indices.items() if v.get('change_pct', 0) > 0]
    down_indices = [(k, v) for k, v in indices.items() if v.get('change_pct', 0) < 0]

    if up_indices:
        best = max(up_indices, key=lambda x: x[1]['change_pct'])
        summary_parts.append(
            f"本周A股市场整体呈震荡上行态势，{best[0]}以{best[1]['change_pct']:.2f}%的周涨幅领跑。"
        )

    if down_indices:
        worst = min(down_indices, key=lambda x: x[1]['change_pct'])
        summary_parts.append(
            f"{worst[0]}下跌{abs(worst[1]['change_pct']):.2f}%，表现相对偏弱。"
        )

    # 行业点评
    sectors = data.get('sw_sectors', {}).get('涨幅TOP5', [])
    if sectors:
        top = sectors[0]
        summary_parts.append(
            f"行业方面，{top['name']}板块表现突出，周涨幅达{top['change_pct']:.2f}%，"
            f"主要受{top.get('driver', '多重因素驱动')}影响。"
        )

    # 展望
    summary_parts.append(
        "展望下周，建议关注中美贸易对话进展、央行LPR调降落地、"
        "以及科技板块短线情绪变化，操作上控制仓位、把握结构性行情。"
    )

    return ''.join(summary_parts)


if __name__ == '__main__':
    # 加载数据
    data_path = Path(__file__).parent.parent / 'data' / 'weekly_data.json'
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 生成摘要
    summary = generate_market_summary(data)
    print('\n📝 生成的市场摘要：')
    print('-' * 50)
    print(summary)
    print('-' * 50)

    # 保存摘要
    output_path = Path(__file__).parent.parent / 'data' / 'ai_summary.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f'\n✅ 摘要已保存至 {output_path}')
