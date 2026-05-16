# T-E2：AI Agent 自动生成股市周报（PDF + HTML）

> 难度：⭐⭐⭐ 较难（技术集成）｜类别：Quarto + AI Agent 在线书/报告  
> 核心工具：`Quarto` · `akshare` · `yfinance` · LLM API（Claude / GPT）  
> 建议人数：7～8 人｜预计完成时间：2 周

---

## 一、项目背景

「AI + 数据 + 自动排版」是当前金融行业最热门的工作流之一。本题目标是构建一个完整的自动化报告生成系统：每周自动拉取 A 股和美股的关键数据，调用 AI API 生成摘要文字，结合 Quarto 模板渲染成排版精美的 PDF 周报和 HTML 网页版——整个过程几乎无需人工干预。

---

## 二、学习目标

完成本题后，你将能够：

- 设计「数据层→分析层→生成层→排版层」的多层自动化流程
- 使用 Anthropic Claude API 或 OpenAI API 生成结构化分析文字
- 使用 Quarto 的参数化报告功能（`params`）实现模板复用
- 将 Quarto 渲染的 HTML 报告发布到 GitHub Pages
- 理解自动化报告的设计原则：可靠性 > 美观性


---

## 四、项目目录结构

```
T-E2_WeeklyReport/
├── readme.md
├── _quarto.yml                   ← Quarto 项目配置
├── report_template.qmd           ← 周报模板（核心）
├── scripts/
│   ├── 01_fetch_data.py          ← 数据获取脚本
│   ├── 02_generate_summary.py    ← AI 生成摘要脚本
│   └── 03_render_report.py       ← 调用 Quarto 渲染的脚本
├── data/
│   ├── weekly_data.json          ← 本周数据（JSON 格式，供模板读取）
│   └── history/                  ← 历史周报数据归档
├── output/
│   ├── weekly_report.pdf
│   └── weekly_report.html
├── .github/
│   └── workflows/
│       └── weekly_report.yml     ← 定时触发（每周五下午）
└── demo_static/                  ← 阶段一：静态演示版
    └── demo_report.qmd
```

---

## 五、任务分解

### 阶段一：静态版（`demo_static/demo_report.qmd`）

先用硬编码数据写好模板，验证排版效果：

````markdown
---
title: "A 股 & 美股周报"
subtitle: "第 XX 周（YYYY-MM-DD 至 YYYY-MM-DD）"
author: "ds2026 第 X 组"
date: today
format:
  html:
    toc: true
    theme: flatly
    self-contained: true
  pdf:
    documentclass: article
    papersize: a4
    geometry: margin=2cm
    include-in-header:
      text: |
        \usepackage{ctex}
---

# 本周市场概览

```{python}
#| echo: false
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 阶段一：手动填写本周数据
weekly_data = {
    '上证指数': {'close': 3321.5, 'change_pct': 1.23},
    '深证成指': {'close': 10543.2, 'change_pct': 0.87},
    '创业板指': {'close': 2156.8, 'change_pct': -0.45},
    '标普500':  {'close': 5432.1, 'change_pct': 2.15},
    '纳斯达克': {'close': 17654.3, 'change_pct': 3.21},
}

df = pd.DataFrame(weekly_data).T.reset_index()
df.columns = ['指数', '收盘价', '周涨跌幅(%)']
df['方向'] = df['周涨跌幅(%)'].apply(lambda x: '▲' if x >= 0 else '▼')
df['显示'] = df.apply(
    lambda r: f"{r['方向']} {abs(r['周涨跌幅(%)']):.2f}%", axis=1
)
df[['指数', '收盘价', '显示']].style \
    .applymap(lambda v: 'color: red' if '▲' in str(v) else 'color: green',
              subset=['显示']) \
    .set_caption('主要指数周度表现')
```

# 本周 A 股热点

```{python}
#| echo: false
# 申万行业涨幅排名（静态版手动填写）
sectors = {
    '通信': 4.5, '电子': 3.2, '计算机': 2.8,
    '汽车': 1.5, '医药': 0.3, '银行': -0.5,
    '地产': -1.2, '食品饮料': -2.1,
}
# 绘制行业涨跌幅柱状图
fig, ax = plt.subplots(figsize=(10, 4))
colors = ['#c0392b' if v >= 0 else '#27ae60' for v in sectors.values()]
ax.barh(list(sectors.keys()), list(sectors.values()), color=colors)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_title('本周申万行业涨跌幅排名（%）')
ax.set_xlabel('涨跌幅（%）')
plt.tight_layout()
plt.show()
```

# AI 生成摘要

> **注意**：以下内容为阶段一手动撰写示例，阶段二将替换为 AI 自动生成。

本周 A 股整体呈震荡上行态势，科技板块领涨，通信和电子行业表现突出……
````

---

### 阶段二：自动化数据获取（`scripts/01_fetch_data.py`）

```python
import akshare as ak
import yfinance as yf
import json
import pandas as pd
from datetime import datetime, timedelta

def get_weekly_data():
    """获取本周主要指数和行业数据"""
    data = {}

    # A 股主要指数（使用 akshare）
    try:
        # 上证指数
        sh = ak.stock_zh_index_daily(symbol='sh000001')
        sh = sh.tail(10)  # 近两周
        weekly_return = (sh['close'].iloc[-1] / sh['close'].iloc[-6] - 1) * 100
        data['上证指数'] = {
            'close': float(sh['close'].iloc[-1]),
            'change_pct': float(weekly_return),
            'date': str(sh.index[-1])
        }
    except Exception as e:
        print(f'上证指数获取失败：{e}')

    # 美股指数（使用 yfinance）
    try:
        sp500 = yf.download('^GSPC', period='10d', progress=False)
        weekly_return = (sp500['Close'].iloc[-1] / sp500['Close'].iloc[-6] - 1) * 100
        data['标普500'] = {
            'close': float(sp500['Close'].iloc[-1]),
            'change_pct': float(weekly_return),
        }
    except Exception as e:
        print(f'标普500获取失败：{e}')

    # 申万行业（akshare）
    try:
        sw = ak.sw_index_daily_indicator(symbol='801010', indicator='近一周')
        # 实际字段名需根据接口返回调整
        data['sectors'] = sw.to_dict(orient='records')
    except Exception as e:
        print(f'行业数据获取失败：{e}')
        data['sectors'] = []

    # 保存
    with open('../data/weekly_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    print(f'数据获取完成：{len(data)} 个数据项')
    return data

if __name__ == '__main__':
    get_weekly_data()
```

---

### 阶段二：AI 摘要生成（`scripts/02_generate_summary.py`）

```python
import anthropic
import json
import os

def generate_market_summary(weekly_data: dict) -> str:
    """调用 Claude API 生成市场摘要"""

    client = anthropic.Anthropic(
        api_key=os.environ.get('ANTHROPIC_API_KEY')
    )

    prompt = f"""
你是一位专业的金融分析师，请根据以下本周市场数据，
撰写一段 300-400 字的市场周报摘要，风格专业、客观、简洁。

本周数据：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

要求：
1. 概括主要指数涨跌情况
2. 点评 2-3 个表现突出的行业及可能原因
3. 简要展望下周需要关注的因素
4. 不要使用「根据数据」「如上所示」等套话
5. 直接输出正文，不需要标题
"""

    message = client.messages.create(
        model='claude-sonnet-4-20250514',
        max_tokens=1000,
        messages=[{'role': 'user', 'content': prompt}]
    )

    return message.content[0].text

if __name__ == '__main__':
    with open('../data/weekly_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    summary = generate_market_summary(data)
    print(summary)

    # 保存摘要
    with open('../data/ai_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
```

> **API Key 管理**：  
> - 开发时：将 Key 存入 `.env` 文件（加入 `.gitignore`），用 `python-dotenv` 加载  
> - GitHub Actions 中：在仓库 Settings → Secrets 添加 `ANTHROPIC_API_KEY`

---

### GitHub Actions 定时触发（每周五 16:00）

```yaml
# .github/workflows/weekly_report.yml
name: Weekly Market Report

on:
  schedule:
    - cron: '0 8 * * 5'   # UTC 时间每周五 08:00 = 北京时间 16:00
  workflow_dispatch:        # 允许手动触发（测试用）

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install akshare yfinance anthropic python-dotenv pandas matplotlib

      - name: Fetch data
        run: python scripts/01_fetch_data.py

      - name: Generate AI summary
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python scripts/02_generate_summary.py

      - name: Install Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Render report
        run: quarto render report_template.qmd --to html,pdf

      - name: Commit and push output
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add output/ data/
          git commit -m "chdir: weekly report $(date +%Y-%m-%d)"
          git push
```

---

## 六、结果解读指引

- AI 生成的摘要是否准确反映了数据？有无「幻觉」（捏造数据）？
- 相比人工撰写，自动生成摘要的优势和局限是什么？
- 如果某周数据获取失败（网络问题、接口变更），系统如何「降级」处理？
- 这套流程用于实际工作需要解决哪些额外问题（时效性、数据来源授权、合规等）？

---

## 七、AI 辅助提示词

**设计 prompt 模板：**
```
我要让 AI 根据股市数据生成周报摘要，请帮我设计一个 prompt，
输入是 JSON 格式的指数涨跌幅和行业排名数据，
输出是 300-400 字的专业中文市场评论，
要求不捏造数据、不过度乐观或悲观、适合机构投资者阅读。
```

**Quarto 参数化报告：**
```
我想用 Quarto 做参数化报告，每次渲染时传入不同的日期参数，
报告标题和数据文件路径根据日期自动变化。
请给我一个完整的 _quarto.yml 和 .qmd 文件示例，
说明如何在命令行传参：quarto render report.qmd -P date:2026-05-09
```

---

## 八、参考资源

- Quarto 参数化报告：<https://quarto.org/docs/computations/parameters.html>
- Anthropic Python SDK：<https://github.com/anthropics/anthropic-sdk-python>
- GitHub Actions 定时任务：<https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule>
- akshare 股指接口文档：<https://akshare.akfamily.xyz/data/index/index.html>

---

*最后更新：2026-05-10*
