@echo off
title 开发者工具集构建工具

echo ==================================================
echo        开发者工具集 PyQt5 版本构建工具
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

REM 检查并安装Pillow
echo.
echo 🔍 检查Pillow依赖...
python -c "from PIL import Image" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  未找到Pillow，正在安装...
    python -m pip install Pillow
    if errorlevel 1 (
        echo ❌ Pillow安装失败
        pause
        exit /b 1
    )
    echo ✅ Pillow安装完成
) else (
    echo ✅ Pillow已安装
)

REM 检查并安装PyInstaller
echo.
echo 🔍 检查PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  未找到PyInstaller，正在安装...
    python install_pyinstaller.py
    if errorlevel 1 (
        echo ❌ PyInstaller安装失败
        pause
        exit /b 1
    )
    echo ✅ PyInstaller安装完成
) else (
    echo ✅ PyInstaller已安装
)

echo.
echo 🚀 开始构建...
echo.

REM 执行构建脚本
python fix_icon_build.py

if errorlevel 1 (
    echo.
    echo ❌ 构建失败!
    pause
    exit /b 1
)

echo.
echo 🎉 构建完成!
echo.
echo 生成的exe文件位于 dist 目录中
echo.
pause