#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者工具集 - 调试版本
"""

import tkinter as tk
import traceback
from toolkit_main import DeveloperToolkit


def debug_main():
    """调试版主函数"""
    print("🔧 开发者工具集 - 调试模式")
    print("=" * 50)
    
    try:
        print("1. 创建主窗口...")
        root = tk.Tk()
        
        print("2. 初始化工具集...")
        app = DeveloperToolkit(root)
        
        print("3. 启动成功！")
        print("💡 现在可以测试工具切换功能")
        print("=" * 50)
        
        root.mainloop()
        
        print("程序正常退出")
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("\n详细错误信息:")
        traceback.print_exc()
        input("\n按回车键退出...")


if __name__ == "__main__":
    debug_main()