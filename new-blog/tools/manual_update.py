#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动输入市场数据更新脚本
当无法自动获取数据时，可以手动输入进行更新

使用方法：
python manual_update.py

"""

import re
import os
from datetime import datetime

def manual_update():
    """手动输入数据进行更新"""
    print("=" * 50)
    print("沪深300与M2数据手动更新")
    print("=" * 50)
    
    # 获取用户输入
    print("\n请输入最新数据：")
    hs300_close = float(input("沪深300收盘点位: "))
    hs300_change = float(input("沪深300涨跌幅(%): "))
    m2_growth = float(input("M2同比增速(%): "))
    
    # 生成投资建议
    signal_score = 0
    
    # M2增速信号
    if m2_growth > 8.0:
        signal_score += 2
    elif m2_growth > 7.5:
        signal_score += 1
    elif m2_growth < 6.5:
        signal_score -= 2
    
    # 股指变化信号
    if hs300_change > 2:
        signal_score += 1
    elif hs300_change < -2:
        signal_score -= 1
    
    # 生成建议
    if signal_score >= 3:
        advice, color = "积极乐观", "#27ae60"
    elif signal_score >= 1:
        advice, color = "谨慎乐观", "#f39c12"
    elif signal_score >= -1:
        advice, color = "观望", "#95a5a6"
    else:
        advice, color = "谨慎", "#e74c3c"
    
    print(f"\n生成的投资建议: {advice}")
    confirm = input("确认更新博客? (y/N): ")
    
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    # 更新博客文件
    blog_post_path = "source/_posts/沪深300与M2增速走势分析.md"
    
    if not os.path.exists(blog_post_path):
        print(f"博客文件不存在: {blog_post_path}")
        return
    
    # 读取文件
    with open(blog_post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(
        r'updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
        f'updated: {current_date} 09:00:00',
        content
    )
    
    # 更新数据表格
    new_row = f"""        <tr>
          <td style="padding: 8px;">{current_date}</td>
          <td style="padding: 8px; text-align: right;">{hs300_close:.2f}</td>
          <td style="padding: 8px; text-align: right; color: {'red' if hs300_change > 0 else 'green'};">{hs300_change:+.2f}%</td>
          <td style="padding: 8px; text-align: right;">{m2_growth:.1f}</td>
          <td style="padding: 8px; text-align: center;">
            <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px;">{advice}</span>
          </td>
        </tr>"""
    
    # 替换第一行数据
    pattern = r'(<tr>\s*<td style="padding: 8px;">\d{4}-\d{2}-\d{2}</td>.*?</tr>)'
    content = re.sub(pattern, new_row, content, count=1, flags=re.DOTALL)
    
    # 更新分析部分
    content = re.sub(
        r'(\*\*日期\*\*): \d{4}年\d{1,2}月\d{1,2}日',
        f'**日期**: {datetime.now().strftime("%Y年%m月%d日")}',
        content
    )
    
    content = re.sub(
        r'(\*\*沪深300指数\*\*): [\d,]+\.?\d* \([+-]?[\d.]+%\)',
        f'**沪深300指数**: {hs300_close:.2f} ({hs300_change:+.2f}%)',
        content
    )
    
    content = re.sub(
        r'(\*\*M2同比增速\*\*): [\d.]+%',
        f'**M2同比增速**: {m2_growth:.1f}%',
        content
    )
    
    # 更新时间戳
    content = re.sub(
        r'数据更新时间: <span id="update-time">[\d-: ]+</span>',
        f'数据更新时间: <span id="update-time">{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>',
        content
    )
    
    # 保存文件
    with open(blog_post_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n" + "=" * 50)
    print("更新完成！")
    print(f"沪深300: {hs300_close:.2f} ({hs300_change:+.2f}%)")
    print(f"M2增速: {m2_growth:.1f}%")
    print(f"投资建议: {advice}")
    print("=" * 50)
    
    print("\n下一步操作:")
    print("1. hexo generate")
    print("2. hexo deploy")
    print("或运行 daily_update.bat 完成发布")

if __name__ == "__main__":
    manual_update()