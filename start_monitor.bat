@echo off
chcp 65001 >nul
title Git配置监控器

echo.
echo ==========================================
echo           Git配置监控器
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ? 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查配置文件
if not exist "config.json" (
    echo ? 错误: 配置文件 config.json 不存在
    echo ?? 请复制 config.example.json 为 config.json 并修改配置
    pause
    exit /b 1
)

REM 检查依赖包
echo ?? 检查依赖包...
pip show watchdog >nul 2>&1
if errorlevel 1 (
    echo ?? 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ? 依赖包安装失败
        pause
        exit /b 1
    )
)

echo ? 环境检查完成
echo.
echo ?? 启动Git配置监控器...
echo ?? 按 Ctrl+C 停止监控
echo.

python git_monitor.py

echo.
echo ?? 监控器已停止
pause
