#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者工具集构建脚本
自动处理图标并构建exe文件
"""

import os
import sys
import subprocess
import shutil
from PIL import Image


def create_high_quality_ico():
    """创建高质量的ICO文件"""
    if not os.path.exists("icon.png"):
        print("❌ 未找到icon.png文件")
        return False
    
    try:
        print("🎨 创建高质量ICO文件...")
        
        # 打开原始PNG
        original = Image.open("icon.png")
        print(f"   原始图片: {original.size[0]}x{original.size[1]}, {original.mode}")
        
        # 转换为RGBA
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        
        # 创建多个标准尺寸
        sizes = [16, 24, 32, 48, 64, 128, 256]
        images = []
        
        for size in sizes:
            # 高质量缩放
            resized = original.resize((size, size), Image.Resampling.LANCZOS)
            images.append(resized)
            print(f"   生成尺寸: {size}x{size}")
        
        # 保存为ICO，包含所有尺寸
        images[0].save("icon.ico", format='ICO', 
                      sizes=[(img.width, img.height) for img in images],
                      append_images=images[1:])
        
        # 验证生成的ICO文件
        ico_check = Image.open("icon.ico")
        print(f"✅ ICO文件创建成功，包含 {getattr(ico_check, 'n_frames', 1)} 个尺寸")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建ICO文件失败: {e}")
        return False


def create_fixed_spec():
    """创建修复的spec文件"""
    print("📄 创建修复的spec文件...")
    
    # 获取绝对路径
    current_dir = os.path.abspath('.')
    icon_path = os.path.join(current_dir, 'icon.ico')
    
    # 确保使用正斜杠（PyInstaller兼容性更好）
    icon_path = icon_path.replace('\\', '/')
    
    # 准备数据文件列表（包含图标文件）
    datas = []
    if os.path.exists('icon.ico'):
        datas.append(('icon.ico', '.'))
    if os.path.exists('icon.png'):
        datas.append(('icon.png', '.'))
    
    datas_str = str(datas).replace("'", '"')
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
# 开发者工具集构建配置

block_cipher = None

a = Analysis(
    ['toolkit_main.py'],
    pathex=['{current_dir.replace(chr(92), '/')}'],
    binaries=[],
    datas={datas_str},
    hiddenimports=['PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui', 'tools.json_formatter_tool', 'tools.timestamp_converter_tool', 'tools.base_tool'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='开发者工具集',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{icon_path}',
)
'''
    
    spec_filename = "json_formatter_fixed.spec"
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ 创建spec文件: {spec_filename}")
    print(f"   图标路径: {icon_path}")
    
    return spec_filename


def build_with_multiple_methods():
    """使用多种方法尝试构建"""
    print("🔨 开始多方法构建...")
    
    # 方法1: 使用修复的spec文件
    print("\n方法1: 使用修复的spec文件")
    spec_file = create_fixed_spec()
    
    if build_with_spec(spec_file):
        return True
    
    # 方法2: 直接命令行，使用绝对路径
    print("\n方法2: 使用绝对路径命令行构建")
    if build_with_absolute_path():
        return True
    
    # 方法3: 使用相对路径但指定工作目录
    print("\n方法3: 指定工作目录构建")
    if build_with_workdir():
        return True
    
    print("❌ 所有构建方法都失败了")
    return False


def build_with_spec(spec_file):
    """使用spec文件构建"""
    try:
        # 清理旧文件（除了即将使用的spec文件）
        cleanup_old_files(exclude_spec=True)
        
        cmd = [sys.executable, "-m", "PyInstaller", spec_file, "--clean"]
        print(f"执行命令: {' '.join(cmd)}")
        
        # 使用stdout和stderr参数以便更好地捕获错误信息
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            print(f"❌ 构建失败，错误信息:")
            print(result.stderr)
            return False
        
        if check_build_result():
            print("✅ spec文件构建成功")
            return True
        else:
            print("❌ spec文件构建失败")
            return False
            
    except Exception as e:
        print(f"❌ spec文件构建出错: {e}")
        return False


def build_with_absolute_path():
    """使用绝对路径构建"""
    try:
        cleanup_old_files()
        
        icon_path = os.path.abspath('icon.ico')
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed", 
            "--clean",
            f"--icon={icon_path}",
            "--name=开发者工具集",
            "--hidden-import=PyQt5",
            "--hidden-import=PyQt5.QtWidgets", 
            "--hidden-import=PyQt5.QtCore",
            "--hidden-import=PyQt5.QtGui",
            "toolkit_main.py"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 构建失败，错误信息:")
            print(result.stderr)
            return False
        
        if check_build_result():
            print("✅ 绝对路径构建成功")
            return True
        else:
            print("❌ 绝对路径构建失败")
            return False
            
    except Exception as e:
        print(f"❌ 绝对路径构建出错: {e}")
        return False


def build_with_workdir():
    """指定工作目录构建"""
    try:
        cleanup_old_files()
        
        current_dir = os.getcwd()
        icon_path = os.path.join(current_dir, 'icon.ico')
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--clean",
            f"--icon={icon_path}",
            "--name=开发者工具集",
            "--hidden-import=PyQt5",
            "--hidden-import=PyQt5.QtWidgets",
            "--hidden-import=PyQt5.QtCore",
            "--hidden-import=PyQt5.QtGui",
            "--workpath", os.path.join(current_dir, "build"),
            "--distpath", os.path.join(current_dir, "dist"),
            "--specpath", current_dir,
            "toolkit_main.py"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ 构建失败，错误信息:")
            print(result.stderr)
            return False
        
        if check_build_result():
            print("✅ 工作目录构建成功")
            return True
        else:
            print("❌ 工作目录构建失败")
            return False
            
    except Exception as e:
        print(f"❌ 工作目录构建出错: {e}")
        return False


def cleanup_old_files(exclude_spec=False):
    """清理旧的构建文件"""
    print("🧹 清理旧文件...")
    
    # 清理build目录
    if os.path.exists("build"):
        try:
            shutil.rmtree("build")
            print("   清理build目录")
        except Exception as e:
            print(f"   清理build目录失败: {e}")
    
    # 清理dist目录
    if os.path.exists("dist"):
        try:
            shutil.rmtree("dist")
            print("   清理dist目录")
        except Exception as e:
            print(f"   清理dist目录失败: {e}")
    
    # 清理spec文件（除非要排除当前使用的spec文件）
    if not exclude_spec:
        spec_files = ["json_formatter_fixed.spec"]
        for spec_file in spec_files:
            if os.path.exists(spec_file):
                try:
                    os.remove(spec_file)
                    print(f"   清理{spec_file}")
                except Exception as e:
                    print(f"   清理{spec_file}失败: {e}")


def check_build_result():
    """检查构建结果"""
    exe_path = os.path.join("dist", "开发者工具集.exe")
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path)
        print(f"✅ 构建成功: {exe_path}")
        print(f"   文件大小: {file_size / 1024 / 1024:.1f} MB")
        return True
    else:
        print("❌ 构建失败: 未找到生成的exe文件")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("开发者工具集构建脚本")
    print("=" * 50)
    
    # 检查必要文件
    required_files = ["toolkit_main.py", "icon.png"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    # 创建高质量图标
    if not create_high_quality_ico():
        print("❌ 图标创建失败")
        return False
    
    # 开始构建
    if build_with_multiple_methods():
        print("\n🎉 所有构建任务完成!")
        return True
    else:
        print("\n💥 构建失败!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)