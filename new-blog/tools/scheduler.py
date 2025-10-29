#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化更新任务调度器
支持定时更新、错误重试、通知等功能
"""

import schedule
import time
import subprocess
import smtplib
from email.mime.text import MimeText
from datetime import datetime
import configparser
import os
import logging

class UpdateScheduler:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini', encoding='utf-8')
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('update_log.txt', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def should_update_today(self):
        """判断今天是否需要更新"""
        weekend_skip = self.config.getboolean('update_schedule', 'weekend_skip', fallback=True)
        
        if weekend_skip and datetime.now().weekday() >= 5:  # 周六=5, 周日=6
            return False
        return True
    
    def run_update_script(self):
        """执行数据更新脚本"""
        if not self.should_update_today():
            self.logger.info("今日为周末，跳过更新")
            return True
        
        try:
            self.logger.info("开始执行数据更新...")
            
            # 执行Python更新脚本
            result = subprocess.run(
                ['python', 'update_market_data.py'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.logger.info("数据更新成功")
                self.run_blog_update()
                return True
            else:
                self.logger.error(f"数据更新失败: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"更新过程出错: {e}")
            return False
    
    def run_blog_update(self):
        """执行博客更新和部署"""
        try:
            self.logger.info("开始更新博客...")
            
            # 切换到博客根目录
            os.chdir('..')
            
            # 执行hexo命令
            commands = [
                ['hexo', 'clean'],
                ['hexo', 'generate'],
                ['hexo', 'deploy']
            ]
            
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"命令 {' '.join(cmd)} 执行失败: {result.stderr}")
            
            # 提交源代码
            git_commands = [
                ['git', 'add', '.'],
                ['git', 'commit', '-m', f'自动更新市场数据 - {datetime.now().strftime("%Y-%m-%d")}'],
                ['git', 'push', 'origin', 'source']
            ]
            
            for cmd in git_commands:
                subprocess.run(cmd, capture_output=True)
            
            self.logger.info("博客更新完成")
            
        except Exception as e:
            self.logger.error(f"博客更新失败: {e}")
        finally:
            # 切回tools目录
            os.chdir('tools')
    
    def send_notification(self, title, message):
        """发送通知"""
        if not self.config.getboolean('notification', 'email_notify', fallback=False):
            return
        
        try:
            email = self.config.get('notification', 'email_address')
            if not email:
                return
            
            # 这里需要配置SMTP服务器信息
            # 示例使用QQ邮箱，实际使用时需要配置
            msg = MimeText(message, 'plain', 'utf-8')
            msg['Subject'] = title
            msg['From'] = email
            msg['To'] = email
            
            # 注意：需要在config.ini中添加SMTP配置
            # server = smtplib.SMTP('smtp.qq.com', 587)
            # server.starttls()
            # server.login(email, 'your_password')
            # server.send_message(msg)
            # server.quit()
            
            self.logger.info("通知已发送")
            
        except Exception as e:
            self.logger.error(f"发送通知失败: {e}")
    
    def scheduled_update(self):
        """计划任务更新函数"""
        self.logger.info("执行计划更新任务")
        
        success = self.run_update_script()
        
        if success:
            self.send_notification(
                "数据更新成功",
                f"市场数据已于 {datetime.now().strftime('%Y-%m-%d %H:%M')} 成功更新"
            )
        else:
            self.send_notification(
                "数据更新失败",
                f"市场数据更新失败，时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
    
    def start_scheduler(self):
        """启动调度器"""
        if not self.config.getboolean('update_schedule', 'auto_update', fallback=False):
            self.logger.info("自动更新已禁用")
            return
        
        update_time = self.config.get('update_schedule', 'update_time', fallback='09:00')
        
        # 设置每日更新时间
        schedule.every().day.at(update_time).do(self.scheduled_update)
        
        self.logger.info(f"调度器已启动，每日 {update_time} 自动更新")
        
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
            except KeyboardInterrupt:
                self.logger.info("调度器已停止")
                break
            except Exception as e:
                self.logger.error(f"调度器错误: {e}")
                time.sleep(300)  # 出错后等待5分钟

def main():
    """主函数"""
    scheduler = UpdateScheduler()
    
    print("数据更新调度器")
    print("1. 立即执行更新")
    print("2. 启动定时调度")
    print("3. 退出")
    
    choice = input("请选择操作 (1-3): ")
    
    if choice == '1':
        scheduler.scheduled_update()
    elif choice == '2':
        scheduler.start_scheduler()
    else:
        print("退出")

if __name__ == "__main__":
    main()