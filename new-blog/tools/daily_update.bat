@echo off
echo =========================================
echo 沪深300与M2数据每日更新脚本
echo =========================================

REM 切换到博客目录
cd /d "g:\SeaLee_AI知识库\SeaLeee.github.io\new-blog"

echo 1. 更新市场数据...
python scripts\update_market_data.py

echo.
echo 2. 清理缓存...
call hexo clean

echo.
echo 3. 生成静态文件...
call hexo generate

echo.
echo 4. 提交更改到Git...
git add .
git commit -m "自动更新: 市场数据 %date:~0,10%"

echo.
echo 5. 部署到GitHub Pages...
call hexo deploy

echo.
echo =========================================
echo 更新完成！博客已发布最新数据
echo =========================================
pause