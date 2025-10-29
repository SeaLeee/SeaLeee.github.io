#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据完整性检查工具
用于验证博客数据的一致性和完整性
"""

import os
import re
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class DataIntegrityChecker:
    def __init__(self):
        self.blog_post_path = "../source/_posts/沪深300与M2增速走势分析.md"
        self.public_path = "../public/2025/10/29/沪深300与M2增速走势分析/index.html"
        self.data_file = "market_data.json"
    
    def check_blog_post_data(self):
        """检查博客文章中的数据"""
        if not os.path.exists(self.blog_post_path):
            return {"status": "error", "message": "博客文件不存在"}
        
        try:
            with open(self.blog_post_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取更新时间
            update_match = re.search(r'updated: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', content)
            update_time = update_match.group(1) if update_match else None
            
            # 提取最新数据行
            table_match = re.search(
                r'<tr>\s*<td[^>]*>(\d{4}-\d{2}-\d{2})</td>.*?<td[^>]*>([\d.]+)</td>.*?<td[^>]*>([+-]?[\d.]+)%</td>.*?<td[^>]*>([\d.]+)</td>',
                content,
                re.DOTALL
            )
            
            if table_match:
                latest_data = {
                    "date": table_match.group(1),
                    "hs300_close": float(table_match.group(2)),
                    "hs300_change": float(table_match.group(3)),
                    "m2_growth": float(table_match.group(4))
                }
            else:
                latest_data = None
            
            return {
                "status": "success",
                "update_time": update_time,
                "latest_data": latest_data
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_published_data(self):
        """检查已发布网站中的数据"""
        if not os.path.exists(self.public_path):
            return {"status": "error", "message": "发布文件不存在，请先生成网站"}
        
        try:
            with open(self.public_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找数据表格
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')
                if len(rows) > 1:  # 排除标题行
                    first_data_row = rows[1]
                    cells = first_data_row.find_all(['td', 'th'])
                    
                    if len(cells) >= 4:
                        published_data = {
                            "date": cells[0].get_text().strip(),
                            "hs300_close": cells[1].get_text().strip(),
                            "hs300_change": cells[2].get_text().strip(),
                            "m2_growth": cells[3].get_text().strip()
                        }
                    else:
                        published_data = None
                else:
                    published_data = None
            else:
                published_data = None
            
            return {
                "status": "success",
                "published_data": published_data
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_data_freshness(self):
        """检查数据新鲜度"""
        blog_check = self.check_blog_post_data()
        
        if blog_check["status"] != "success" or not blog_check.get("latest_data"):
            return {"status": "error", "message": "无法获取博客数据"}
        
        latest_date_str = blog_check["latest_data"]["date"]
        latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")
        current_date = datetime.now()
        
        days_old = (current_date - latest_date).days
        
        # 判断数据新鲜度
        if days_old == 0:
            freshness = "最新"
        elif days_old <= 1:
            freshness = "较新"
        elif days_old <= 3:
            freshness = "一般"
        else:
            freshness = "过期"
        
        return {
            "status": "success",
            "latest_date": latest_date_str,
            "days_old": days_old,
            "freshness": freshness
        }
    
    def check_data_consistency(self):
        """检查数据一致性"""
        blog_check = self.check_blog_post_data()
        published_check = self.check_published_data()
        
        if blog_check["status"] != "success":
            return {"status": "error", "message": f"博客检查失败: {blog_check.get('message')}"}
        
        if published_check["status"] != "success":
            return {"status": "error", "message": f"发布检查失败: {published_check.get('message')}"}
        
        blog_data = blog_check.get("latest_data")
        published_data = published_check.get("published_data")
        
        if not blog_data or not published_data:
            return {"status": "error", "message": "无法提取数据进行比较"}
        
        # 比较关键数据
        inconsistencies = []
        
        if blog_data["date"] != published_data["date"]:
            inconsistencies.append("日期不一致")
        
        try:
            blog_hs300 = float(blog_data["hs300_close"])
            pub_hs300 = float(published_data["hs300_close"].replace(',', ''))
            if abs(blog_hs300 - pub_hs300) > 0.01:
                inconsistencies.append("沪深300点位不一致")
        except:
            inconsistencies.append("沪深300数据格式错误")
        
        return {
            "status": "success",
            "consistent": len(inconsistencies) == 0,
            "inconsistencies": inconsistencies,
            "blog_data": blog_data,
            "published_data": published_data
        }
    
    def generate_health_report(self):
        """生成数据健康报告"""
        print("数据完整性检查报告")
        print("=" * 50)
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # 检查博客文件
        blog_check = self.check_blog_post_data()
        print("1. 博客文件检查:")
        if blog_check["status"] == "success":
            print("   ✓ 博客文件正常")
            if blog_check.get("update_time"):
                print(f"   ✓ 最后更新: {blog_check['update_time']}")
            if blog_check.get("latest_data"):
                data = blog_check["latest_data"]
                print(f"   ✓ 最新数据: {data['date']} | 沪深300: {data['hs300_close']} ({data['hs300_change']:+.2f}%) | M2: {data['m2_growth']}%")
        else:
            print(f"   ✗ 检查失败: {blog_check.get('message')}")
        
        print()
        
        # 检查发布状态
        published_check = self.check_published_data()
        print("2. 发布状态检查:")
        if published_check["status"] == "success":
            print("   ✓ 网站已发布")
            if published_check.get("published_data"):
                data = published_check["published_data"]
                print(f"   ✓ 发布数据: {data['date']} | 沪深300: {data['hs300_close']} | M2: {data['m2_growth']}")
        else:
            print(f"   ✗ 检查失败: {published_check.get('message')}")
        
        print()
        
        # 检查数据新鲜度
        freshness_check = self.check_data_freshness()
        print("3. 数据新鲜度:")
        if freshness_check["status"] == "success":
            freshness = freshness_check["freshness"]
            days_old = freshness_check["days_old"]
            
            if freshness == "最新":
                print(f"   ✓ 数据最新 (今日数据)")
            elif freshness in ["较新", "一般"]:
                print(f"   ⚠ 数据{freshness} ({days_old}天前)")
            else:
                print(f"   ✗ 数据过期 ({days_old}天前)")
        else:
            print(f"   ✗ 检查失败: {freshness_check.get('message')}")
        
        print()
        
        # 检查一致性
        consistency_check = self.check_data_consistency()
        print("4. 数据一致性:")
        if consistency_check["status"] == "success":
            if consistency_check["consistent"]:
                print("   ✓ 数据一致")
            else:
                print("   ✗ 数据不一致:")
                for issue in consistency_check["inconsistencies"]:
                    print(f"     - {issue}")
        else:
            print(f"   ✗ 检查失败: {consistency_check.get('message')}")
        
        print()
        print("=" * 50)

def main():
    """主函数"""
    checker = DataIntegrityChecker()
    checker.generate_health_report()

if __name__ == "__main__":
    main()