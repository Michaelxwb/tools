#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller安装脚本
解决网络超时和文件占用问题
"""

import subprocess
import sys
import time
import os


def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller已安装，版本: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller未安装")
        return False


def install_with_method(method_name, command, timeout=300):
    """使用指定方法安装PyInstaller"""
    print(f"\n🔄 {method_name}")
    print(f"执行命令: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, timeout=timeout, 
                              capture_output=True, text=True)
        print("✅ 安装成功!")
        return True
    except subprocess.TimeoutExpired:
        print("⏰ 安装超时，可能是网络问题")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        if e.stderr:
            print(f"错误详情: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False


def main():
    """主安装流程"""
    print("=" * 50)
    print("PyInstaller 安装工具")
    print("=" * 50)
    
    # 检查是否已安装
    if check_pyinstaller():
        print("\n✅ PyInstaller已经安装，无需重复安装")
        return True
    
    print("\n开始安装PyInstaller...")
    
    # 安装方法列表
    methods = [
        {
            "name": "方法1: 使用用户目录安装",
            "command": [sys.executable, "-m", "pip", "install", "--user", "pyinstaller"],
            "timeout": 300
        },
        {
            "name": "方法2: 使用清华大学镜像源",
            "command": [sys.executable, "-m", "pip", "install", 
                       "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/", 
                       "--trusted-host", "pypi.tuna.tsinghua.edu.cn",
                       "pyinstaller"],
            "timeout": 300
        },
        {
            "name": "方法3: 使用阿里云镜像源 + 用户目录",
            "command": [sys.executable, "-m", "pip", "install", "--user",
                       "-i", "https://mirrors.aliyun.com/pypi/simple/",
                       "--trusted-host", "mirrors.aliyun.com",
                       "pyinstaller"],
            "timeout": 300
        },
        {
            "name": "方法4: 使用豆瓣镜像源",
            "command": [sys.executable, "-m", "pip", "install",
                       "-i", "https://pypi.douban.com/simple/",
                       "--trusted-host", "pypi.douban.com",
                       "pyinstaller"],
            "timeout": 300
        },
        {
            "name": "方法5: 强制重新安装",
            "command": [sys.executable, "-m", "pip", "install", "--user", 
                       "--force-reinstall", "--no-deps", "pyinstaller"],
            "timeout": 180
        }
    ]
    
    # 逐个尝试安装方法
    for method in methods:
        if install_with_method(method["name"], method["command"], method["timeout"]):
            # 验证安装是否成功
            time.sleep(2)  # 等待安装完成
            if check_pyinstaller():
                print(f"\n🎉 安装成功! 使用了{method['name']}")
                return True
            else:
                print("⚠️ 安装命令执行成功，但验证失败，继续尝试下一种方法...")
    
    # 所有方法都失败
    print("\n❌ 所有安装方法都失败了")
    print("\n📋 手动安装建议:")
    print("1. 关闭所有Python相关程序和IDE")
    print("2. 以管理员身份运行命令提示符")
    print("3. 执行以下命令之一:")
    print("   pip install --user pyinstaller")
    print("   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ pyinstaller")
    print("4. 或者下载离线安装包:")
    print("   https://pypi.org/project/pyinstaller/#files")
    print("   然后执行: pip install pyinstaller-5.13.2-py3-none-win_amd64.whl")
    
    return False


if __name__ == "__main__":
    success = main()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ 安装完成! 现在可以运行 python build.py 来构建exe文件")
    else:
        print("❌ 安装失败，请参考上面的手动安装建议")
    print("=" * 50)
    
    input("\n按回车键退出...")