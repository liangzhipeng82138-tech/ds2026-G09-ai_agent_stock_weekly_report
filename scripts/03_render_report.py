"""
03_render_report.py - 调用Quarto渲染报告
将数据和摘要整合到Quarto模板中，渲染生成PDF和HTML报告

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
import subprocess
import os
from pathlib import Path
from datetime import datetime


def render_quarto_report(date_param: str = None):
    """
    调用Quarto渲染周报模板
    支持参数化渲染：quarto render report_template.qmd -P date:2026-05-15
    """
    project_root = Path(__file__).parent.parent
    template_path = project_root / 'report_template.qmd'
    output_dir = project_root / 'output'

    if not template_path.exists():
        print(f'⚠️ 模板文件不存在：{template_path}')
        print('   尝试使用demo模板...')
        template_path = project_root / 'demo_static' / 'demo_report.qmd'

    if not template_path.exists():
        print('❌ 未找到任何可用的Quarto模板')
        return False

    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)

    # 构建渲染命令
    cmd = ['quarto', 'render', str(template_path), '--to', 'html']

    if date_param:
        cmd.extend(['-P', f'date:{date_param}'])
    else:
        cmd.extend(['-P', f'date:{datetime.now().strftime("%Y-%m-%d")}'])

    # 执行渲染
    print(f'📝 正在渲染报告：{" ".join(cmd)}')
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(project_root))
        if result.returncode == 0:
            print('✅ HTML报告渲染成功')
        else:
            print(f'⚠️ HTML渲染警告：{result.stderr}')

        # 渲染PDF
        cmd_pdf = ['quarto', 'render', str(template_path), '--to', 'pdf']
        if date_param:
            cmd_pdf.extend(['-P', f'date:{date_param}'])

        print(f'📝 正在渲染PDF报告...')
        result_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True, cwd=str(project_root))
        if result_pdf.returncode == 0:
            print('✅ PDF报告渲染成功')
        else:
            print(f'⚠️ PDF渲染可能需要LaTeX环境：{result_pdf.stderr[:200]}')

        return True

    except FileNotFoundError:
        print('❌ 未找到Quarto，请先安装：https://quarto.org/docs/get-started/')
        return False


def copy_to_output():
    """将渲染结果复制到output目录"""
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    # 查找渲染生成的文件
    for pattern in ['*.html', '*.pdf']:
        for f in project_root.glob(pattern):
            dest = output_dir / f.name
            import shutil
            shutil.copy2(f, dest)
            print(f'  📄 {f.name} → {dest}')


if __name__ == '__main__':
    print('=' * 50)
    print('📊 开始渲染周报...')
    print('=' * 50)

    # 检查数据文件
    data_path = Path(__file__).parent.parent / 'data' / 'weekly_data.json'
    if data_path.exists():
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'✅ 数据文件已加载：{data_path}')
    else:
        print(f'⚠️ 数据文件不存在：{data_path}')
        print('   请先运行 01_fetch_data.py 获取数据')

    # 检查摘要文件
    summary_path = Path(__file__).parent.parent / 'data' / 'ai_summary.txt'
    if summary_path.exists():
        print(f'✅ AI摘要已就绪：{summary_path}')
    else:
        print(f'⚠️ AI摘要不存在，请先运行 02_generate_summary.py')

    # 渲染报告
    success = render_quarto_report()

    if success:
        # 复制输出
        print('\n📁 整理输出文件...')
        copy_to_output()
        print('\n✅ 周报渲染完成！')
    else:
        print('\n⚠️ Quarto渲染失败，但静态HTML周报已就绪（index.html）')
