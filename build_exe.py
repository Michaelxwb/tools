#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台Windows EXE构建脚本
支持在macOS/Linux上构建Windows .exe可执行文件
"""

import subprocess
import sys
import os
import shutil
import platform


def check_cross_platform_support():
    """检查跨平台构建支持"""
    print("🔍 检查跨平台构建环境...")
    
    # 检查PyInstaller是否支持交叉编译
    try:
        result = subprocess.run([sys.executable, '-m', 'PyInstaller', '--help'], 
                              capture_output=True, text=True)
        if '--target-arch' in result.stdout or '--platform' in result.stdout:
            print("✅ PyInstaller支持交叉编译")
            return True
    except:
        pass
    
    print("⚠️  标准PyInstaller不支持直接交叉编译")
    print("🔄 将使用Wine或Docker方案...")
    return False


def build_windows_exe_wine():
    """使用Wine在macOS/Linux上构建Windows EXE"""
    print("🍷 使用Wine构建Windows EXE...")
    
    # 清理旧的构建文件
    for item in ['build', 'dist', 'DeveloperToolkit.spec']:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    # 检查Wine是否可用（更健壮的检测）
    wine_commands = ['wine', 'wine64', 'wine-stable', 'wine-devel']
    wine_cmd = None
    
    for cmd in wine_commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                wine_cmd = cmd
                print(f"✅ Wine已安装: {cmd}")
                break
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    if not wine_cmd:
        print("❌ Wine未正确安装或运行")
        print("💡 安装Wine:")
        print("   macOS Intel: brew install --cask wine-stable")
        print("   macOS Apple Silicon: brew install --cask wine-crossover")
        print("   Ubuntu: sudo apt install wine64")
        print("   CentOS: sudo yum install wine")
        print("   或访问: https://wiki.winehq.org/Download")
        return False
    
    return wine_cmd
    
    # 检查并安装Windows Python到Wine
    try:
        result = subprocess.run(['wine', 'python', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Windows Python环境就绪")
        else:
            raise FileNotFoundError
    except:
        print("🔄 正在安装Windows Python到Wine...")
        try:
            # 下载并安装Python到Wine
            python_url = "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
            python_installer = "python-3.9.13-amd64.exe"
            
            if not os.path.exists(python_installer):
                print(f"📥 下载Python安装器...")
                subprocess.run(['curl', '-L', '-o', python_installer, python_url], check=True)
            
            # 静默安装Python到Wine
            subprocess.run(['wine', python_installer, '/quiet', 'InstallAllUsers=0'], check=True)
            print("✅ Windows Python安装完成")
            
            # 清理安装器
            os.remove(python_installer)
            
        except Exception as e:
            print(f"❌ Python安装失败: {e}")
            print("💡 手动安装: wine python-3.9.13-amd64.exe")
            return False
    
    # 使用Wine运行Windows Python和PyInstaller
    wine_cmd = build_windows_exe_wine()  # 获取wine命令
    if not wine_cmd:
        return False
    
    # 尝试不同的Python路径
    python_paths = ['python', 'python3', 'C:\Python39\python.exe', 'C:\Python310\python.exe']
    wine_python = None
    
    for py_path in python_paths:
        try:
            result = subprocess.run([wine_cmd, py_path, '--version'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                wine_python = py_path
                print(f"✅ 找到Wine Python: {py_path}")
                break
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            continue
    
    if not wine_python:
        print("🔄 尝试安装Windows Python到Wine...")
        try:
            # 下载Python安装器
            python_url = "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
            python_installer = "python-3.9.13-amd64.exe"
            
            if not os.path.exists(python_installer):
                print(f"📥 下载Python安装器...")
                subprocess.run(['curl', '-L', '-o', python_installer, python_url], check=True)
            
            # 静默安装Python到Wine
            subprocess.run([wine_cmd, python_installer, '/quiet', 'InstallAllUsers=0'], check=True)
            print("✅ Windows Python安装完成")
            wine_python = 'python'
            
            # 清理安装器
            os.remove(python_installer)
            
        except Exception as e:
            print(f"❌ Python安装失败: {e}")
            print("💡 手动安装: wine python-3.9.13-amd64.exe")
            return False
    
    # 安装PyInstaller到Wine
    try:
        subprocess.run([wine_cmd, wine_python, '-m', 'pip', 'install', 'pyinstaller'], 
                     check=True, timeout=300)
        print("✅ PyInstaller安装到Wine完成")
    except Exception as e:
        print(f"⚠️  PyInstaller安装警告: {e}")
    
    build_cmd = [
        wine_cmd, wine_python, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=DeveloperToolkit',
        '--icon=icon.ico',
        '--add-data=icon.ico;.',  # Windows路径分隔符
        '--add-data=tools;tools',  # Windows路径分隔符
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=redis',
        '--hidden-import=redis.cluster',
        '--clean',
        '--noconfirm',
        'toolkit_main.py'
    ]
    
    try:
        subprocess.run(build_cmd, check=True)
        exe_path = os.path.join('dist', 'DeveloperToolkit.exe')
        if os.path.exists(exe_path):
            print("✅ Windows EXE构建完成！")
            print(f"📁 文件位置: {os.path.abspath(exe_path)}")
            print(f"📊 文件大小: {os.path.getsize(exe_path) / 1024 / 1024:.1f} MB")
            return True
        else:
            print("❌ EXE文件未生成")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Wine构建失败: {e}")
        return False


def build_windows_exe_docker():
    """使用Docker构建Windows EXE（简化版，使用Wine替代）"""
    print("⚠️  Docker Windows容器在macOS/Linux上不可用")
    print("💡 建议使用Wine方案")
    return False


def build_windows_exe():
    """主构建函数"""
    print("=" * 60)
    print("🪟 Windows EXE跨平台构建工具")
    print("=" * 60)
    print(f"当前系统: {platform.system()} {platform.machine()}")
    print(f"Python版本: {sys.version}")
    
    # 清理旧的构建文件
    for item in ['build', 'dist', 'DeveloperToolkit.exe', 'DeveloperToolkit.spec']:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    # 根据系统选择构建方法
    if platform.system() == 'Windows':
        print("✅ 在Windows系统上，使用原生构建")
        return build_windows_exe_native()
    else:
        print("🔄 在非Windows系统上，使用Wine构建Windows EXE")
        print("=" * 50)
        print("📋 macOS Wine构建指南:")
        print("1. 安装Wine: brew install --cask wine-stable")
        print("2. 如果遇到SIGKILL错误，尝试:")
        print("   - 重启终端")
        print("   - 检查系统完整性保护")
        print("   - 使用Rosetta 2 (Apple Silicon)")
        print("3. 首次运行会自动安装Windows Python")
        print("=" * 50)
        
        # 强制使用Wine方案
        wine_cmd = build_windows_exe_wine()
        if wine_cmd:
            print("🍷 使用Wine构建Windows EXE")
            return build_windows_exe_wine()
        else:
            print("❌ Wine未正确安装或运行")
            print("💡 解决方案:")
            print("   1. 重新安装: brew reinstall --cask wine-stable")
            print("   2. 检查权限: sudo spctl --master-disable")
            print("   3. 使用替代方案: 在Windows虚拟机中构建")
            print("   4. 或直接在Windows系统上运行")
            return False


def build_windows_exe_native():
    """Windows原生构建"""
    print("🪟 Windows原生构建...")
    
    build_cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=DeveloperToolkit',
        '--icon=icon.ico',
        '--add-data=icon.ico;.',  # Windows路径分隔符
        '--add-data=tools;tools',  # Windows路径分隔符
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=redis',
        '--hidden-import=redis.cluster',
        '--clean',
        '--noconfirm',
        'toolkit_main.py'
    ]
    
    try:
        subprocess.run(build_cmd, check=True)
        exe_path = os.path.join('dist', 'DeveloperToolkit.exe')
        if os.path.exists(exe_path):
            print("✅ Windows EXE构建完成！")
            print(f"📁 文件位置: {os.path.abspath(exe_path)}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建失败: {e}")
        return False


if __name__ == "__main__":
    success = build_windows_exe()
    if success:
        print("\n🎉 Windows EXE构建成功！")
        print("📦 生成的文件: DeveloperToolkit.exe")
        print("✅ 可在Windows系统上直接运行")
    else:
        print("\n❌ Windows EXE构建失败")