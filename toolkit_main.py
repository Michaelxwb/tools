#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者工具集 - 主程序
集成多种开发常用工具
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
from tools.json_formatter_tool import JSONFormatterTool
from tools.timestamp_converter_tool import TimestampConverterTool


class DeveloperToolkit:
    def __init__(self, root):
        self.root = root
        self.root.title("开发者工具集")
        self.root.geometry("1200x800")
        
        # 初始化工具实例字典
        self.tools = {}
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.setup_ui()
        
    def get_resource_path(self, relative_path):
        """获取资源文件路径，兼容打包后的exe"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def set_window_icon(self):
        """设置窗口图标"""
        try:
            icon_files = ["icon.ico", "icon.png"]
            
            for icon_file in icon_files:
                paths_to_try = [
                    icon_file,
                    self.get_resource_path(icon_file),
                    os.path.join(".", icon_file),
                ]
                
                for icon_path in paths_to_try:
                    if os.path.exists(icon_path):
                        try:
                            if icon_path.endswith('.ico'):
                                self.root.iconbitmap(icon_path)
                                return
                            elif icon_path.endswith('.png'):
                                try:
                                    from PIL import Image, ImageTk
                                    img = Image.open(icon_path)
                                    img = img.resize((32, 32), Image.Resampling.LANCZOS)
                                    photo = ImageTk.PhotoImage(img)
                                    self.root.iconphoto(True, photo)
                                    self.root._icon_photo = photo
                                    return
                                except ImportError:
                                    pass
                        except Exception:
                            continue
        except Exception:
            pass
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 工具选择按钮样式
        style.configure("Tool.TButton",
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 10))
        
        # 选中的工具按钮样式
        style.configure("SelectedTool.TButton",
                       font=('Segoe UI', 11, 'bold'),
                       padding=(20, 10),
                       background='#0078d4',
                       foreground='white')
        
        # 标题样式
        style.configure("Title.TLabel",
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#323130')
    
    def setup_ui(self):
        """创建用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 工具选择区域
        tool_frame = ttk.Frame(main_frame)
        tool_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(tool_frame, text="选择工具:", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        # 工具按钮
        self.tool_buttons = {}
        
        # JSON格式化工具按钮
        json_btn = ttk.Button(tool_frame, text="📝 JSON格式化", 
                             command=lambda: self.switch_tool('json_formatter'),
                             style="Tool.TButton")
        json_btn.pack(side=tk.LEFT, padx=5)
        self.tool_buttons['json_formatter'] = json_btn
        
        # 时间戳转换工具按钮
        timestamp_btn = ttk.Button(tool_frame, text="⏰ 时间戳转换", 
                                  command=lambda: self.switch_tool('timestamp_converter'),
                                  style="Tool.TButton")
        timestamp_btn.pack(side=tk.LEFT, padx=5)
        self.tool_buttons['timestamp_converter'] = timestamp_btn
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # 工具内容区域
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 默认显示JSON格式化工具
        self.current_tool = None
        # 延迟初始化，确保界面完全创建后再加载工具
        self.root.after(100, lambda: self.switch_tool('json_formatter'))
    
    def switch_tool(self, tool_name):
        """切换工具"""
        if self.current_tool == tool_name:
            return
        
        # 清空当前内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 清空工具缓存，因为父框架已被销毁
        self.tools.clear()
        
        # 更新按钮样式
        for name, button in self.tool_buttons.items():
            if name == tool_name:
                button.configure(style="SelectedTool.TButton")
            else:
                button.configure(style="Tool.TButton")
        
        # 创建新工具实例
        if tool_name == 'json_formatter':
            self.tools[tool_name] = JSONFormatterTool(self.content_frame)
        elif tool_name == 'timestamp_converter':
            self.tools[tool_name] = TimestampConverterTool(self.content_frame)
        
        self.current_tool = tool_name


def main():
    """主函数"""
    root = tk.Tk()
    app = DeveloperToolkit(root)
    root.mainloop()


if __name__ == "__main__":
    main()