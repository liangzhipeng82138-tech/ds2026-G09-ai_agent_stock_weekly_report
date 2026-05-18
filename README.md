# T-E2：AI Agent 自动生成股市周报

> **课程**：数据分析与经济决策（ds2026）  
> **题目**：T-E2：AI Agent自动生成股市周报  
> **小组**：第09组  
> **GitHub**：https://github.com/liangzhipeng82138-tech/ds2026-G09-ai_agent_stock_weekly_report  
> **Pages**：https://liangzhipeng82138-tech.github.io/ds2026-G09-ai_agent_stock_weekly_report/

---

## 📋 小组成员与分工

| 成员 | 学号 | 角色 | 负责章节 |
|------|------|------|---------|
| 梁志鹏 | 25210177 | 大盘整体行情分析师 | 第一章：大盘整体行情概览 |
| 吴璇子 | 25210264 | 板块与行业轮动分析师 | 第二章：板块与行业轮动分析 |
| 黄悦 | 25210145 | 资金流向分析师 | 第三章：资金流向分析 |
| 王鹤洋 | 25210243 | 重点个股与热点事件分析师 | 第四章：重点个股与热点事件 |
| 柯骋 | 25210150 | 宏观与政策面分析师 | 第五章：宏观与政策面分析 |
| 罗天 | 25210207 | 风险与情绪研判分析师 | 第六章：风险与情绪研判 |

---

## 📁 项目目录结构

```
group_0518/
├── index.html                      ← 炫酷静态HTML周报主页（左侧导航+章节切换）
├── pages/
│   ├── index_1.html                ← 第一章：大盘整体行情概览
│   ├── index_2.html                ← 第二章：板块与行业轮动分析
│   ├── index_3.html                ← 第三章：资金流向分析
│   ├── index_4.html                ← 第四章：重点个股与热点事件
│   ├── index_5.html                ← 第五章：宏观与政策面分析
│   └── index_6.html                ← 第六章：风险与情绪研判
├── menbers/
│   ├── liangzhipeng/               ← 梁志鹏的Quarto文件
│   │   ├── _quarto.yml
│   │   └── index.qmd
│   ├── wuxuanzi/                   ← 吴璇子的Quarto文件
│   │   ├── _quarto.yml
│   │   └── index.qmd
│   ├── huangyue/                   ← 黄悦的Quarto文件
│   │   ├── _quarto.yml
│   │   └── index.qmd
│   ├── wangheyang/                 ← 王鹤洋的Quarto文件
│   │   ├── _quarto.yml
│   │   └── index.qmd
│   ├── kecheng/                    ← 柯骋的Quarto文件
│   │   ├── _quarto.yml
│   │   └── index.qmd
│   └── luotian/                   ← 罗天的Quarto文件
│       ├── _quarto.yml
│       └── index.qmd
├── scripts/
│   ├── 01_fetch_data.py            ← 数据获取脚本（akshare + yfinance）
│   ├── 02_generate_summary.py      ← AI摘要生成脚本（Claude/GPT API）
│   └── 03_render_report.py         ← Quarto渲染脚本
├── data/
│   ├── weekly_data.json            ← 本周市场数据（JSON格式）
│   └── history/                    ← 历史周报数据归档
├── prompt/                         ← 作业要求文件
│   ├── T-E2_AI_Agent自动生成股市周报.md
│   ├── 小组成员与作业完成方案.md
│   └── 小组作业要求.md
├── .github/
│   └── workflows/
│       └── weekly_report.yml       ← GitHub Actions定时触发
├── readme.md                       ← 本文件
└── report_template.qmd            ← Quarto周报模板
```

---

## 🚀 使用说明

### 在线查看

直接打开 `index.html` 即可在浏览器中查看完整的股市周报，支持左侧导航切换章节。

### 数据获取（自动化）

```bash
# 安装依赖
pip install akshare yfinance anthropic python-dotenv pandas matplotlib

# 1. 获取数据
python scripts/01_fetch_data.py

# 2. 生成AI摘要（需设置ANTHROPIC_API_KEY或OPENAI_API_KEY环境变量）
python scripts/02_generate_summary.py

# 3. 渲染Quarto报告
python scripts/03_render_report.py
```

### Quarto渲染

每位成员可在自己的目录下独立渲染：

```bash
cd menbers/liangzhipeng
quarto render
```

---

## 🤖 AI工具使用说明

本项目使用了以下AI工具：

- **Cursor / CodeBuddy**：辅助编写代码和HTML页面

所有AI生成的内容均经过小组成员审核和修改，确保数据准确性和分析合理性。

---

## 📊 本周报告摘要（2026-W20）

本周A股市场整体呈震荡上行态势，科技成长板块领涨。科创50以1.62%的周涨幅领跑，创业板指上涨1.31%。通信、电子、计算机行业表现突出，受5G-A商用牌照发放和AI产业政策催化。北向资金全周净流入82.3亿元，重点加仓科技方向。央行MLF降息10bp释放宽松信号。但房地产链持续承压，消费复苏偏弱。综合判断当前市场为结构性行情，科技主线清晰。

---

*最后更新：2026-05-15*
