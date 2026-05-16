"""
T-E2 AI Agent自动生成股市周报 — 渲染脚本

功能：
1. 调用 Quarto 渲染周报模板
2. 输出 HTML 和 PDF 格式
3. 将输出文件复制到 output/ 目录
"""

import os
import shutil
import subprocess
from datetime import datetime

# ===== 配置 =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'report_template.qmd')


def check_quarto():
    """检查 Quarto 是否已安装"""
    try:
        result = subprocess.run(['quarto', '--version'], 
                              capture_output=True, text=True, timeout=10)
        version = result.stdout.strip()
        print(f'Quarto 版本: {version}')
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print('错误: 未找到 Quarto，请先安装: https://quarto.org/docs/get-started/')
        return False


def render_report(formats=None):
    """渲染周报"""
    if formats is None:
        formats = ['html', 'pdf']
    
    if not os.path.exists(TEMPLATE_PATH):
        print(f'错误: 未找到模板文件 {TEMPLATE_PATH}')
        return False
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    for fmt in formats:
        print(f'\n正在渲染 {fmt.upper()} 格式 ...')
        try:
            cmd = ['quarto', 'render', TEMPLATE_PATH, '--to', fmt]
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  cwd=BASE_DIR, timeout=120)
            
            if result.returncode == 0:
                print(f'  ✓ {fmt.upper()} 渲染成功')
                
                # 复制输出文件到 output/ 目录
                expected_files = {
                    'html': 'report_template.html',
                    'pdf': 'report_template.pdf',
                }
                
                src = os.path.join(BASE_DIR, expected_files.get(fmt, ''))
                if os.path.exists(src):
                    dst = os.path.join(OUTPUT_DIR, f'weekly_report.{fmt}')
                    shutil.copy2(src, dst)
                    print(f'  已复制至: {dst}')
            else:
                print(f'  ✗ {fmt.upper()} 渲染失败:')
                print(f'  {result.stderr[:500]}')
                
        except subprocess.TimeoutExpired:
            print(f'  ✗ {fmt.upper()} 渲染超时')
        except Exception as e:
            print(f'  ✗ {fmt.upper()} 渲染异常: {e}')
    
    return True


def main():
    """主函数"""
    print('=' * 50)
    print('AI Agent 股市周报 — 渲染报告')
    print(f'运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 50)
    
    if not check_quarto():
        return
    
    render_report()
    
    print('\n输出目录内容:')
    for f in os.listdir(OUTPUT_DIR):
        size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
        print(f'  {f} ({size/1024:.1f} KB)')
    
    print('\n✓ 渲染完成！')


if __name__ == '__main__':
    main()
