@echo off
title 开发者工具集

echo ==================================================
echo           开发者工具集 PyQt5 版本
echo ==================================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python环境，请先安装Python 3.6或更高版本
    echo    下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

REM 检查并安装PyQt5
echo.
echo 🔍 检查PyQt5依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  未找到PyQt5，正在安装...
    python -m pip install PyQt5
    if errorlevel 1 (
        echo ❌ PyQt5安装失败
        pause
        exit /b 1
    )
    echo ✅ PyQt5安装完成
) else (
    echo ✅ PyQt5已安装
)

echo.
echo 🚀 启动开发者工具集...
echo.

REM 运行主程序
python start_toolkit.py

echo.
echo 👋 程序已退出
pause