#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证和备份系统
确保数据更新的可靠性和完整性
"""

import json
import os
import shutil
from datetime import datetime, timedelta
import pandas as pd
import configparser

class DataManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        self.backup_dir = "data_backup"
        self.data_file = "market_data.json"
        
        # 确保备份目录存在
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def validate_data(self, hs300_data, m2_data):
        """验证数据的合理性"""
        errors = []
        
        # 验证沪深300数据
        if not isinstance(hs300_data.get('close'), (int, float)):
            errors.append("沪深300收盘价格式错误")
        elif hs300_data['close'] < 1000 or hs300_data['close'] > 10000:
            errors.append(f"沪深300点位异常: {hs300_data['close']}")
        
        if not isinstance(hs300_data.get('change_pct'), (int, float)):
            errors.append("沪深300涨跌幅格式错误")
        elif abs(hs300_data['change_pct']) > 20:
            errors.append(f"沪深300涨跌幅异常: {hs300_data['change_pct']}%")
        
        # 验证M2数据
        if not isinstance(m2_data.get('m2_growth'), (int, float)):
            errors.append("M2增速格式错误")
        elif m2_data['m2_growth'] < 0 or m2_data['m2_growth'] > 20:
            errors.append(f"M2增速异常: {m2_data['m2_growth']}%")
        
        return errors
    
    def backup_current_data(self):
        """备份当前数据"""
        try:
            if os.path.exists(self.data_file):
                backup_filename = f"market_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = os.path.join(self.backup_dir, backup_filename)
                shutil.copy2(self.data_file, backup_path)
                print(f"数据已备份到: {backup_path}")
                return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
        return None
    
    def save_data(self, hs300_data, m2_data):
        """保存验证后的数据"""
        # 验证数据
        errors = self.validate_data(hs300_data, m2_data)
        if errors:
            print("数据验证失败:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        # 备份旧数据
        self.backup_current_data()
        
        # 保存新数据
        data = {
            "last_update": datetime.now().isoformat(),
            "hs300": hs300_data,
            "m2": m2_data,
            "validation_passed": True
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("数据保存成功")
            return True
        except Exception as e:
            print(f"数据保存失败: {e}")
            return False
    
    def load_latest_data(self):
        """加载最新数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载数据失败: {e}")
        return None
    
    def get_data_history(self, days=30):
        """获取历史数据"""
        history = []
        
        # 从备份文件中读取历史数据
        if os.path.exists(self.backup_dir):
            for filename in sorted(os.listdir(self.backup_dir)):
                if filename.startswith('market_data_') and filename.endswith('.json'):
                    filepath = os.path.join(self.backup_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            history.append(data)
                    except:
                        continue
        
        # 只返回最近指定天数的数据
        return history[-days:] if len(history) > days else history
    
    def cleanup_old_backups(self):
        """清理过期备份"""
        if not os.path.exists(self.backup_dir):
            return
        
        backup_days = int(self.config.get('backup', 'backup_days', fallback=30))
        cutoff_date = datetime.now() - timedelta(days=backup_days)
        
        for filename in os.listdir(self.backup_dir):
            filepath = os.path.join(self.backup_dir, filename)
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if file_time < cutoff_date:
                    try:
                        os.remove(filepath)
                        print(f"已清理过期备份: {filename}")
                    except Exception as e:
                        print(f"清理备份失败 {filename}: {e}")
    
    def generate_data_report(self):
        """生成数据质量报告"""
        latest_data = self.load_latest_data()
        if not latest_data:
            return "无可用数据"
        
        history = self.get_data_history(7)  # 最近7天
        
        report = f"""
数据质量报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}
{'='*50}

最新数据:
  更新时间: {latest_data.get('last_update', 'N/A')}
  沪深300: {latest_data.get('hs300', {}).get('close', 'N/A')}
  M2增速: {latest_data.get('m2', {}).get('m2_growth', 'N/A')}%
  验证状态: {'通过' if latest_data.get('validation_passed') else '失败'}

历史数据:
  可用记录: {len(history)} 条
  备份文件: {len(os.listdir(self.backup_dir)) if os.path.exists(self.backup_dir) else 0} 个

数据完整性: {'良好' if len(history) >= 5 else '需要补充'}
"""
        return report

def main():
    """主函数 - 演示数据管理功能"""
    dm = DataManager()
    
    print("数据管理系统演示")
    print("="*40)
    
    # 生成报告
    report = dm.generate_data_report()
    print(report)
    
    # 清理过期备份
    dm.cleanup_old_backups()

if __name__ == "__main__":
    main()