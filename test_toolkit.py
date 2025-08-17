#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具集测试脚本
"""

import tkinter as tk
from toolkit_main import DeveloperToolkit


def test_toolkit():
    """测试工具集"""
    print("启动开发者工具集测试...")
    
    try:
        root = tk.Tk()
        app = DeveloperToolkit(root)
        
        print("✅ 工具集启动成功")
        print("💡 请在界面中测试工具切换功能")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_toolkit()