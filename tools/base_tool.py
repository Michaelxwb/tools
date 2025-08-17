#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具基类
定义工具的通用接口和功能
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.main_frame = None
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """设置用户界面 - 子类必须实现"""
        pass
    
    def show(self):
        """显示工具界面"""
        try:
            if self.main_frame and self.main_frame.winfo_exists():
                self.main_frame.pack(fill=tk.BOTH, expand=True)
        except tk.TclError:
            # 如果框架已被销毁，重新创建
            self.setup_ui()
    
    def hide(self):
        """隐藏工具界面"""
        try:
            if self.main_frame and self.main_frame.winfo_exists():
                self.main_frame.pack_forget()
        except tk.TclError:
            # 框架已被销毁，无需操作
            pass
    
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        try:
            self.parent_frame.clipboard_clear()
            self.parent_frame.clipboard_append(text)
            return True
        except Exception:
            return False
    
    def show_message(self, title, message, msg_type="info"):
        """显示消息"""
        from tkinter import messagebox
        
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
    
    def create_button_frame(self, parent, buttons_config):
        """创建按钮框架"""
        button_frame = ttk.Frame(parent, padding="10")
        button_frame.pack(fill=tk.X)
        
        # 居中的按钮容器
        button_container = ttk.Frame(button_frame)
        button_container.pack(expand=True)
        
        for i, config in enumerate(buttons_config):
            btn = ttk.Button(button_container, 
                           text=config.get('text', ''),
                           command=config.get('command', None),
                           width=config.get('width', 12),
                           style=config.get('style', 'TButton'))
            btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        return button_frame