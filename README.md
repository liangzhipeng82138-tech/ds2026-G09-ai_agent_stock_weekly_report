# T-E2：AI Agent 自动生成股市周报

| 项目   | 内容 |
|--------|------|
| 课程   | 数据分析与经济决策（ds2026） |
| 题目   | T-E2：AI_Agent自动生成股市周报 |
| 小组   | 第 09 组 |
| 成员   | 梁志鹏（25210177）、吴璇子（25210264）、黄悦（25210145）、王鹤洋（25210243）、柯骋（25210150）、罗天（25210207）、易忠凯 |
| GitHub | https://github.com/liangzhipeng82138-tech/ds2026-G09-ai_agent_stock_weekly_report |
| Pages  | https://liangzhipeng82138-tech.github.io/ds2026-G09-ai_agent_stock_weekly_report/ |
| 日期   | 2026-05-15 |

---

## 项目简介

本项目构建一个完整的自动化股市周报生成系统：每周自动拉取 A 股核心数据，调用 AI API 生成分析摘要，结合 Quarto 模板渲染成排版精美的 PDF 周报和 HTML 网页版。同时提供炫酷的静态 HTML 交互式周报页面。

### 核心流程

```
数据获取 (akshare/yfinance) → 数据清洗 (pandas) → 分析与可视化 (matplotlib/plotly) → AI摘要生成 (Claude/GPT) → 排版渲染 (Quarto/HTML)
```

---

## 小组分工

| 章节 | 负责人 | 核心内容 |
|------|--------|----------|
| 第1章 大盘整体行情 | 梁志鹏 | 核心指数涨跌幅、市场情绪、北向资金、全局定性 |
| 第2章 板块与行业轮动 | 吴璇子 | 申万行业涨跌排名、热门题材、赛道轮动 |
| 第3章 资金流向分析 | 黄悦 | 北向/主力/散户资金、龙虎榜、成交额 |
| 第4章 重点个股与热点 | 王鹤洋 | 龙头股/黑马股、个股公告、连板分析 |
| 第5章 宏观与政策面 | 柯骋 | CPI/PMI/社融、政策解读、外围市场 |
| 第6章 风险与情绪研判 | 罗天 | 估值分析、恐慌指数、风险汇总 |
| 第7章 下周展望与策略 | 易忠凯 | 走势预判、策略建议、全文汇总 |

---

## 项目目录结构

```
ds2026-G09-ai_agent_stock_weekly_report/
├── readme.md                    ← 本文件
├── index.html                   ← 第1章静态HTML周报
├── pages/                       ← 其他章节HTML页面
│   ├── index_2.html
│   ├── index_3.html
│   ├── index_4.html
│   ├── index_5.html
│   ├── index_6.html
│   └── index_7.html
├── data_raw/                    ← 原始数据（直接获取，不做修改）
├── data_clean/                  ← 清洗后的数据
├── output/                      ← 图表、报告、结果文件
├── 01_get_data.ipynb            ← 数据获取
├── 02_data_clean.ipynb          ← 数据清洗与整理
├── 03_analysis.ipynb            ← 探索性/验证性分析
├── 04_visualization.ipynb       ← 数据可视化
├── _quarto.yml                  ← Quarto 项目配置
├── report_template.qmd          ← 周报 Quarto 模板
├── scripts/
│   ├── 01_fetch_data.py         ← 数据获取脚本
│   ├── 02_generate_summary.py   ← AI 生成摘要脚本
│   └── 03_render_report.py      ← 调用 Quarto 渲染脚本
├── data/
│   └── history/                 ← 历史周报数据归档
├── demo_static/
│   └── demo_report.qmd          ← 静态演示版
├── .github/
│   └── workflows/
│       └── weekly_report.yml    ← 定时触发 GitHub Actions
└── prompt/                      ← 作业要求文档
```

---

## AI 工具使用说明

本项目使用了以下 AI 工具辅助开发：

- **CodeBuddy (GLM-5.1)**：用于生成项目框架代码、HTML/CSS 页面设计、Notebook 代码骨架
- **Claude API**：用于自动生成股市周报分析摘要文字
- AI 生成的代码均已通过本地测试，分析结论在 AI 输出基础上进行了人工审校与补充

---

## 快速开始

```bash
# 安装依赖
pip install akshare yfinance anthropic python-dotenv pandas matplotlib plotly

# 获取数据
python scripts/01_fetch_data.py

# 生成 AI 摘要（需设置 ANTHROPIC_API_KEY）
python scripts/02_generate_summary.py

# 渲染 Quarto 报告
quarto render report_template.qmd --to html,pdf
```

---

*最后更新：2026-05-16*
