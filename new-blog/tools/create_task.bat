@echo off
REM Windows任务计划创建脚本
REM 用于在Windows系统中创建每日自动更新任务

echo ========================================
echo 创建Windows每日更新任务计划
echo ========================================

set TASK_NAME=MarketDataUpdate
set SCRIPT_PATH=%~dp0daily_update.bat
set UPDATE_TIME=09:00

echo 当前脚本路径: %SCRIPT_PATH%
echo 计划执行时间: 每日 %UPDATE_TIME%

REM 检查是否已存在同名任务
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if %errorlevel% equ 0 (
    echo 发现已存在的任务，正在删除...
    schtasks /delete /tn "%TASK_NAME%" /f
)

echo 正在创建新的计划任务...

REM 创建每日执行的计划任务
schtasks /create /tn "%TASK_NAME%" /tr "\"%SCRIPT_PATH%\"" /sc daily /st %UPDATE_TIME% /ru "SYSTEM" /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 任务创建成功！
    echo 任务名称: %TASK_NAME%
    echo 执行时间: 每日 %UPDATE_TIME%
    echo 执行脚本: %SCRIPT_PATH%
    echo ========================================
    echo.
    echo 您可以通过以下方式管理任务:
    echo 1. 打开"任务计划程序" (taskschd.msc)
    echo 2. 使用命令: schtasks /query /tn "%TASK_NAME%"
    echo 3. 删除任务: schtasks /delete /tn "%TASK_NAME%" /f
    echo.
) else (
    echo.
    echo ========================================
    echo 任务创建失败！
    echo 请检查权限或手动创建计划任务
    echo ========================================
)

pause