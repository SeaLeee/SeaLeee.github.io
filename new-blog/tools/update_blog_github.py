#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions专用博客更新脚本
读取市场数据并更新博客文章
"""

import os
import json
import re
from datetime import datetime
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_blog.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlogUpdater:
    def __init__(self):
        self.blog_post_path = "../source/_posts/沪深300与M2增速走势分析.md"
        self.data_file = "market_data.json"
    
    def load_market_data(self):
        """加载市场数据"""
        if not os.path.exists(self.data_file):
            logger.error(f"数据文件不存在: {self.data_file}")
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info("市场数据加载成功")
            return data
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
            return None
    
    def generate_investment_advice(self, hs300_data, m_data):
        """生成投资建议"""
        try:
            signal_score = 0
            
            # M1-M2差值信号 (更重要的指标)
            m1_m2_diff = m_data.get("m1_m2_diff", 0)
            if m1_m2_diff > 0:  # M1增速 > M2增速，资金更活跃
                signal_score += 3
            elif m1_m2_diff > -2:  # 差值在合理范围内
                signal_score += 1
            elif m1_m2_diff < -5:  # 资金过度沉淀
                signal_score -= 2
            
            # 沪深300变化信号
            change_pct = hs300_data.get("change_pct", 0)
            if change_pct > 2:
                signal_score += 1
            elif change_pct < -2:
                signal_score -= 1
            
            # M2增速信号（流动性环境）
            m2_growth = m_data.get("m2_growth", 0)
            if m2_growth > 8.5:
                signal_score += 1
            elif m2_growth < 6.5:
                signal_score -= 1
            
            # 生成建议
            if signal_score >= 4:
                return "积极乐观", "#27ae60", "适当加仓，关注成长板块和流动性敏感板块"
            elif signal_score >= 2:
                return "谨慎乐观", "#f39c12", "维持仓位，重点关注M1-M2差值变化"
            elif signal_score >= -1:
                return "中性观望", "#95a5a6", "控制仓位，等待流动性结构改善"
            else:
                return "谨慎", "#e74c3c", "减仓观望，资金流动性结构不利"
                
        except Exception as e:
            logger.error(f"生成投资建议失败: {e}")
            return "中性观望", "#95a5a6", "数据异常，建议谨慎操作"
    
    def update_blog_content(self, market_data):
        """更新博客内容"""
        if not os.path.exists(self.blog_post_path):
            logger.error(f"博客文件不存在: {self.blog_post_path}")
            return False
        
        try:
            hs300_data = market_data.get("hs300", {})
            m_data = market_data.get("monetary", {})
            
            # 生成投资建议
            advice, color, description = self.generate_investment_advice(hs300_data, m_data)
            
            # 读取原文件
            with open(self.blog_post_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新文章更新时间
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = re.sub(
                r'updated: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',
                f'updated: {current_time}',
                content
            )
            
            # 更新数据更新时间戳
            content = re.sub(
                r'数据更新时间: <span id="update-time">[\d-: ]+</span>',
                f'数据更新时间: <span id="update-time">{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>',
                content
            )
            
            # 构建新的数据行
            date_str = hs300_data.get("date", datetime.now().strftime("%Y-%m-%d"))
            hs300_close = hs300_data.get("close", 0)
            hs300_change = hs300_data.get("change_pct", 0)
            m1_growth = m_data.get("m1_growth", 0)
            m2_growth = m_data.get("m2_growth", 0)
            m1_m2_diff = m_data.get("m1_m2_diff", 0)
            
            change_color = "red" if hs300_change >= 0 else "green"
            diff_color = "red" if m1_m2_diff >= 0 else "green"
            
            new_row = f"""        <tr>
          <td style="padding: 8px;">{date_str}</td>
          <td style="padding: 8px; text-align: right;">{hs300_close:.2f}</td>
          <td style="padding: 8px; text-align: right; color: {change_color};">{hs300_change:+.2f}%</td>
          <td style="padding: 8px; text-align: right;">{m1_growth:.1f}%</td>
          <td style="padding: 8px; text-align: right;">{m2_growth:.1f}%</td>
          <td style="padding: 8px; text-align: right; color: {diff_color};">{m1_m2_diff:+.1f}%</td>
          <td style="padding: 8px; text-align: center;">
            <span style="background: {color}; color: white; padding: 2px 8px; border-radius: 4px;">{advice}</span>
          </td>
        </tr>"""
            
            # 替换表格中的第一行数据（最新数据）
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
                f'**沪深300指数**: {hs300_close:.2f} ({hs300_change:+.2f}%)',
                content
            )
            
            content = re.sub(
                r'(\*\*M2同比增速\*\*): [\d.]+%',
                f'**M2同比增速**: {m2_growth:.1f}%',
                content
            )
            
            # 添加M1增速和差值信息
            content = re.sub(
                r'(\*\*M2同比增速\*\*: [\d.]+%)',
                f'**M1同比增速**: {m1_growth:.1f}%\n- **M2同比增速**: {m2_growth:.1f}%\n- **M1-M2差值**: {m1_m2_diff:+.1f}%',
                content
            )
            
            # 保存更新后的文件
            with open(self.blog_post_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info("博客文章更新成功")
            logger.info(f"沪深300: {hs300_close:.2f} ({hs300_change:+.2f}%)")
            logger.info(f"M1增速: {m1_growth:.1f}%, M2增速: {m2_growth:.1f}%")
            logger.info(f"M1-M2差值: {m1_m2_diff:+.1f}%")
            logger.info(f"投资建议: {advice}")
            
            return True
            
        except Exception as e:
            logger.error(f"更新博客失败: {e}")
            return False
    
    def run(self):
        """执行博客更新流程"""
        logger.info("开始更新博客...")
        
        # 加载市场数据
        market_data = self.load_market_data()
        if not market_data:
            logger.error("无法加载市场数据")
            return False
        
        # 更新博客内容
        if self.update_blog_content(market_data):
            logger.info("博客更新完成")
            return True
        else:
            logger.error("博客更新失败")
            return False

if __name__ == "__main__":
    updater = BlogUpdater()
    success = updater.run()
    
    if success:
        print("博客更新成功")
    else:
        print("博客更新失败")
        exit(1)