#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标转换工具
将PNG图标转换为ICO格式
"""

import os
import sys


def convert_png_to_ico():
    """将PNG图标转换为ICO格式"""
    if not os.path.exists("icon.png"):
        print("❌ 找不到icon.png文件")
        return False
    
    try:
        # 尝试使用PIL/Pillow转换
        from PIL import Image
        
        print("🔄 正在转换PNG图标为ICO格式...")
        
        # 打开PNG图片
        img = Image.open("icon.png")
        
        # 转换为RGBA模式（支持透明度）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建多个尺寸的图标（Windows标准）
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # 调整图片大小并保存为ICO
        img.save("icon.ico", format='ICO', sizes=sizes)
        
        print("✅ 图标转换成功: icon.ico")
        return True
        
    except ImportError:
        print("❌ 需要安装Pillow库来转换图标")
        print("请运行: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ 图标转换失败: {e}")
        return False


def install_pillow():
    """安装Pillow库"""
    print("🔄 正在安装Pillow库...")
    
    import subprocess
    
    methods = [
        {
            "name": "使用用户目录安装",
            "command": [sys.executable, "-m", "pip", "install", "--user", "Pillow"]
        },
        {
            "name": "使用清华镜像源",
            "command": [sys.executable, "-m", "pip", "install", 
                       "-i", "https://pypi.tuna.tsinghua.edu.cn/simple/", 
                       "Pillow"]
        },
        {
            "name": "使用阿里云镜像源",
            "command": [sys.executable, "-m", "pip", "install",
                       "-i", "https://mirrors.aliyun.com/pypi/simple/",
                       "Pillow"]
        }
    ]
    
    for method in methods:
        try:
            print(f"尝试{method['name']}...")
            subprocess.run(method["command"], check=True, timeout=300)
            print("✅ Pillow安装成功")
            return True
        except Exception as e:
            print(f"❌ {method['name']}失败: {e}")
    
    return False


def main():
    """主函数"""
    print("=" * 50)
    print("图标转换工具")
    print("=" * 50)
    
    # 检查是否存在PNG图标
    if not os.path.exists("icon.png"):
        print("❌ 找不到icon.png文件")
        print("请确保icon.png文件在当前目录中")
        return False
    
    # 检查是否已经有ICO文件
    if os.path.exists("icon.ico"):
        print("⚠️ 发现已存在的icon.ico文件")
        choice = input("是否覆盖现有的icon.ico文件? (y/N): ").lower()
        if choice != 'y':
            print("取消转换")
            return True
    
    # 尝试转换
    if convert_png_to_ico():
        return True
    
    # 如果转换失败，尝试安装Pillow
    print("\n尝试安装Pillow库...")
    if install_pillow():
        # 重新尝试转换
        return convert_png_to_ico()
    
    print("\n❌ 无法完成图标转换")
    print("请手动安装Pillow: pip install Pillow")
    return False


if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 图标转换完成!")
        print("现在可以运行构建脚本来打包带图标的exe文件")
    else:
        print("\n❌ 图标转换失败")
    
    input("\n按回车键退出...")