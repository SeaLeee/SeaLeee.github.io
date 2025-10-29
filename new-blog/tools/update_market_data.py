#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深300与M2数据更新脚本
用于自动获取最新数据并更新博客文章

依赖库：
pip install requests pandas beautifulsoup4 akshare

使用方法：
python update_market_data.py

"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import re
import os

class MarketDataUpdater:
    def __init__(self):
        self.hs300_url = "http://api.example.com/hs300"  # 替换为实际API
        self.m2_url = "http://api.example.com/m2"        # 替换为实际API
        self.blog_post_path = "source/_posts/沪深300与M2增速走势分析.md"
        
    def fetch_hs300_data(self):
        """获取沪深300指数数据"""
        try:
            # 这里应该替换为实际的数据获取逻辑
            # 示例：使用akshare库
            import akshare as ak
            
            # 获取沪深300指数数据
            hs300_data = ak.stock_zh_index_daily(symbol="sh000300")
            latest_data = hs300_data.iloc[-1]
            
            return {
                "date": latest_data.name.strftime("%Y-%m-%d"),
                "close": float(latest_data['close']),
                "change_pct": float(latest_data['pct_chg']),
                "volume": float(latest_data['volume'])
            }
        except Exception as e:
            print(f"获取沪深300数据失败: {e}")
            # 返回模拟数据
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "close": 3850.23,
                "change_pct": 1.25,
                "volume": 15680000
            }
    
    def fetch_m2_data(self):
        """获取M2同比增速数据"""
        try:
            # 这里应该替换为实际的M2数据获取逻辑
            # M2数据通常每月公布一次，可能需要从央行网站爬取
            
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "m2_growth": 7.8,  # M2同比增速
                "m1_growth": 5.2   # M1同比增速（可选）
            }
        except Exception as e:
            print(f"获取M2数据失败: {e}")
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "m2_growth": 7.8,
                "m1_growth": 5.2
            }
    
    def generate_investment_advice(self, hs300_data, m2_data):
        """生成投资建议"""
        signal_score = 0
        
        # M2增速信号
        m2_growth = m2_data["m2_growth"]
        if m2_growth > 8.0:
            signal_score += 2
        elif m2_growth > 7.5:
            signal_score += 1
        elif m2_growth < 6.5:
            signal_score -= 2
        
        # 股指变化信号
        change_pct = hs300_data["change_pct"]
        if change_pct > 2:
            signal_score += 1
        elif change_pct < -2:
            signal_score -= 1
        
        # 生成建议文本
        if signal_score >= 3:
            return "积极乐观", "#27ae60", "适当加仓，关注成长板块"
        elif signal_score >= 1:
            return "谨慎乐观", "#f39c12", "维持仓位，精选个股"
        elif signal_score >= -1:
            return "观望", "#95a5a6", "保持谨慎，控制仓位"
        else:
            return "谨慎", "#e74c3c", "减仓观望，规避风险"
    
    def update_blog_post(self, hs300_data, m2_data):
        """更新博客文章内容"""
        if not os.path.exists(self.blog_post_path):
            print(f"博客文件不存在: {self.blog_post_path}")
            return
        
        # 生成投资建议
        advice, color, description = self.generate_investment_advice(hs300_data, m2_data)
        
        # 读取原文件
        with open(self.blog_post_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(
            r'updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
            f'updated: {current_date} 09:00:00',
            content
        )
        
        # 更新数据表格中的第一行（最新数据）
        new_row = f"""        <tr>
          <td style="padding: 8px;">{hs300_data['date']}</td>
          <td style="padding: 8px; text-align: right;">{hs300_data['close']:.2f}</td>
          <td style="padding: 8px; text-align: right; color: {'red' if hs300_data['change_pct'] > 0 else 'green'};">{hs300_data['change_pct']:+.2f}%</td>
          <td style="padding: 8px; text-align: right;">{m2_data['m2_growth']:.1f}</td>
          <td style="padding: 8px; text-align: center;">
            <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px;">{advice}</span>
          </td>
        </tr>"""
        
        # 替换表格中的第一行数据
        pattern = r'(<tr>\s*<td style="padding: 8px;">\d{4}-\d{2}-\d{2}</td>.*?</tr>)'
        content = re.sub(pattern, new_row, content, count=1, flags=re.DOTALL)
        
        # 更新分析部分的数据
        content = re.sub(
            r'(\*\*日期\*\*): \d{4}年\d{1,2}月\d{1,2}日',
            f'**日期**: {datetime.now().strftime("%Y年%m月%d日")}',
            content
        )
        
        content = re.sub(
            r'(\*\*沪深300指数\*\*): [\d,]+\.?\d* \([+-]?[\d.]+%\)',
            f'**沪深300指数**: {hs300_data["close"]:.2f} ({hs300_data["change_pct"]:+.2f}%)',
            content
        )
        
        content = re.sub(
            r'(\*\*M2同比增速\*\*): [\d.]+%',
            f'**M2同比增速**: {m2_data["m2_growth"]:.1f}%',
            content
        )
        
        # 更新时间戳
        content = re.sub(
            r'数据更新时间: <span id="update-time">[\d-: ]+</span>',
            f'数据更新时间: <span id="update-time">{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>',
            content
        )
        
        # 保存更新后的文件
        with open(self.blog_post_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"博客文章已更新: {self.blog_post_path}")
        print(f"沪深300: {hs300_data['close']:.2f} ({hs300_data['change_pct']:+.2f}%)")
        print(f"M2增速: {m2_data['m2_growth']:.1f}%")
        print(f"投资建议: {advice}")
    
    def generate_chart_data(self, hs300_data, m2_data):
        """生成图表数据（JSON格式）"""
        chart_data = {
            "date": hs300_data["date"],
            "hs300": hs300_data["close"],
            "hs300_change": hs300_data["change_pct"],
            "m2_growth": m2_data["m2_growth"],
            "update_time": datetime.now().isoformat()
        }
        
        # 保存为JSON文件，供前端图表使用
        with open("source/data/market_data.json", "w", encoding="utf-8") as f:
            json.dump(chart_data, f, ensure_ascii=False, indent=2)
        
        print("图表数据已保存: source/data/market_data.json")
    
    def run(self):
        """执行数据更新流程"""
        print("开始更新市场数据...")
        
        # 获取数据
        hs300_data = self.fetch_hs300_data()
        m2_data = self.fetch_m2_data()
        
        # 更新博客文章
        self.update_blog_post(hs300_data, m2_data)
        
        # 生成图表数据
        os.makedirs("source/data", exist_ok=True)
        self.generate_chart_data(hs300_data, m2_data)
        
        print("数据更新完成！")

if __name__ == "__main__":
    updater = MarketDataUpdater()
    updater.run()