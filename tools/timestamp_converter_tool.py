#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间戳转换工具
"""

import tkinter as tk
from tkinter import ttk
import time
import datetime
from .base_tool import BaseTool


class TimestampConverterTool(BaseTool):
    """时间戳转换工具类"""
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.parent_frame, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 初始化更新标志
        self.is_updating = True
        
        # 设置样式
        self.setup_styles()
        
        # 创建当前时间显示区域
        self.create_current_time_area()
        
        # 创建时间戳转换区域
        self.create_timestamp_converter_area()
        
        # 创建时间转时间戳区域
        self.create_datetime_converter_area()
        
        # 启动时间更新
        self.update_current_time()
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 主要功能按钮样式
        style.configure("Primary.TButton", 
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background='#0078d4')
        
        # 次要功能按钮样式
        style.configure("Secondary.TButton",
                       font=('Segoe UI', 9, 'bold'),
                       foreground='#323130',
                       background='#f3f2f1')
        
        # 危险操作按钮样式
        style.configure("Danger.TButton",
                       font=('Segoe UI', 9, 'bold'),
                       foreground='white',
                       background='#d13438')
        
        # 配置悬停效果
        style.map("Primary.TButton",
                 background=[('active', '#106ebe'), ('pressed', '#005a9e')])
        style.map("Secondary.TButton",
                 background=[('active', '#edebe9'), ('pressed', '#e1dfdd')])
        style.map("Danger.TButton",
                 background=[('active', '#a4262c'), ('pressed', '#8b1f24')])
    
    def create_current_time_area(self):
        """创建当前时间显示区域"""
        current_frame = ttk.LabelFrame(self.main_frame, text="当前时间", padding="15")
        current_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 当前时间显示
        time_display_frame = ttk.Frame(current_frame)
        time_display_frame.pack(fill=tk.X)
        
        ttk.Label(time_display_frame, text="当前Unix时间戳:", font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.current_timestamp_var = tk.StringVar()
        timestamp_label = ttk.Label(time_display_frame, textvariable=self.current_timestamp_var, 
                                   font=('Consolas', 12, 'bold'), foreground='#0078d4')
        timestamp_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 停止和复制按钮
        button_frame = ttk.Frame(time_display_frame)
        button_frame.pack(side=tk.RIGHT)
        
        self.stop_btn = ttk.Button(button_frame, text="⏸️ 停止", command=self.toggle_update, 
                                  width=10, style="Danger.TButton")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = ttk.Button(button_frame, text="📋 复制", 
                             command=lambda: self.copy_current_timestamp(), 
                             width=10, style="Secondary.TButton")
        copy_btn.pack(side=tk.LEFT, padx=5)
    
    def create_timestamp_converter_area(self):
        """创建时间戳转换区域"""
        ts_frame = ttk.LabelFrame(self.main_frame, text="Unix时间戳转换", padding="15")
        ts_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 输入行
        input_frame = ttk.Frame(ts_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(input_frame, text="Unix时间戳", font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.timestamp_entry = ttk.Entry(input_frame, font=('Consolas', 12), width=15)
        self.timestamp_entry.pack(side=tk.LEFT, padx=(20, 10))
        
        convert_btn = ttk.Button(input_frame, text="🔄 转换", command=self.convert_timestamp, 
                                width=10, style="Primary.TButton")
        convert_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        result_frame = ttk.Frame(ts_frame)
        result_frame.pack(fill=tk.X)
        
        self.timestamp_result_var = tk.StringVar()
        result_entry = ttk.Entry(result_frame, textvariable=self.timestamp_result_var, 
                                font=('Consolas', 12), state='readonly', width=25)
        result_entry.pack(side=tk.LEFT, padx=(20, 10))
        
        copy_result_btn = ttk.Button(result_frame, text="📋 复制", 
                                    command=lambda: self.copy_to_clipboard(self.timestamp_result_var.get()), 
                                    width=10, style="Secondary.TButton")
        copy_result_btn.pack(side=tk.LEFT, padx=5)
    
    def create_datetime_converter_area(self):
        """创建时间转时间戳区域"""
        dt_frame = ttk.LabelFrame(self.main_frame, text="时间转Unix时间戳", padding="15")
        dt_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 输入行
        input_frame = ttk.Frame(dt_frame)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(input_frame, text="时间转Unix时间戳(年-月-日 时:分:秒)", font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.datetime_entry = ttk.Entry(input_frame, font=('Consolas', 12), width=20)
        self.datetime_entry.pack(side=tk.LEFT, padx=(20, 10))
        
        convert_dt_btn = ttk.Button(input_frame, text="转换", command=self.convert_datetime, width=8)
        convert_dt_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示
        result_frame = ttk.Frame(dt_frame)
        result_frame.pack(fill=tk.X)
        
        self.datetime_result_var = tk.StringVar()
        result_entry = ttk.Entry(result_frame, textvariable=self.datetime_result_var, 
                                font=('Consolas', 12), state='readonly', width=15)
        result_entry.pack(side=tk.LEFT, padx=(20, 10))
        
        copy_dt_result_btn = ttk.Button(result_frame, text="复制", 
                                       command=lambda: self.copy_to_clipboard(self.datetime_result_var.get()), 
                                       width=8)
        copy_dt_result_btn.pack(side=tk.LEFT, padx=5)
        
        # 时间单位选择
        unit_frame = ttk.Frame(dt_frame)
        unit_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.time_unit = tk.StringVar(value="秒")
        
        ttk.Radiobutton(unit_frame, text="秒", variable=self.time_unit, value="秒").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(unit_frame, text="毫秒", variable=self.time_unit, value="毫秒").pack(side=tk.LEFT, padx=10)
        
        copy_unit_btn = ttk.Button(unit_frame, text="复制", 
                                  command=self.copy_with_unit, width=8)
        copy_unit_btn.pack(side=tk.LEFT, padx=(20, 0))
    
    def update_current_time(self):
        """更新当前时间显示"""
        try:
            if self.is_updating and hasattr(self, 'current_timestamp_var'):
                current_timestamp = int(time.time())
                self.current_timestamp_var.set(str(current_timestamp))
            
            # 每秒更新一次
            if hasattr(self, 'parent_frame') and self.parent_frame.winfo_exists():
                self.parent_frame.after(1000, self.update_current_time)
        except (tk.TclError, AttributeError):
            # 如果组件已被销毁，停止更新
            pass
    
    def toggle_update(self):
        """切换时间更新状态"""
        self.is_updating = not self.is_updating
        if self.is_updating:
            self.stop_btn.config(text="停止")
        else:
            self.stop_btn.config(text="开始")
    
    def copy_current_timestamp(self):
        """复制当前时间戳"""
        timestamp = self.current_timestamp_var.get()
        if self.copy_to_clipboard(timestamp):
            self.show_message("成功", "当前时间戳已复制到剪贴板")
    
    def convert_timestamp(self):
        """转换时间戳为可读时间"""
        try:
            timestamp_str = self.timestamp_entry.get().strip()
            if not timestamp_str:
                self.show_message("警告", "请输入时间戳", "warning")
                return
            
            # 尝试解析时间戳
            timestamp = float(timestamp_str)
            
            # 判断是秒还是毫秒（毫秒时间戳通常大于10位数）
            if timestamp > 10000000000:  # 毫秒时间戳
                timestamp = timestamp / 1000
            
            # 转换为可读时间
            dt = datetime.datetime.fromtimestamp(timestamp)
            readable_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            
            self.timestamp_result_var.set(readable_time)
            
        except ValueError:
            self.show_message("错误", "请输入有效的时间戳数字", "error")
        except OSError:
            self.show_message("错误", "时间戳超出有效范围", "error")
        except Exception as e:
            self.show_message("错误", f"转换失败: {str(e)}", "error")
    
    def convert_datetime(self):
        """转换时间为时间戳"""
        try:
            datetime_str = self.datetime_entry.get().strip()
            if not datetime_str:
                self.show_message("警告", "请输入时间", "warning")
                return
            
            # 尝试解析多种时间格式
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%Y/%m/%d %H:%M:%S",
                "%Y/%m/%d %H:%M",
                "%Y/%m/%d"
            ]
            
            dt = None
            for fmt in formats:
                try:
                    dt = datetime.datetime.strptime(datetime_str, fmt)
                    break
                except ValueError:
                    continue
            
            if dt is None:
                self.show_message("错误", "无法解析时间格式\n支持格式:\n• YYYY-MM-DD HH:MM:SS\n• YYYY-MM-DD HH:MM\n• YYYY-MM-DD\n• YYYY/MM/DD HH:MM:SS\n• YYYY/MM/DD HH:MM\n• YYYY/MM/DD", "error")
                return
            
            # 转换为时间戳
            timestamp = int(dt.timestamp())
            self.datetime_result_var.set(str(timestamp))
            
        except Exception as e:
            self.show_message("错误", f"转换失败: {str(e)}", "error")
    
    def copy_with_unit(self):
        """根据选择的单位复制时间戳"""
        timestamp_str = self.datetime_result_var.get()
        if not timestamp_str:
            self.show_message("警告", "请先转换时间", "warning")
            return
        
        try:
            timestamp = int(timestamp_str)
            
            if self.time_unit.get() == "毫秒":
                result = str(timestamp * 1000)
            else:
                result = timestamp_str
            
            if self.copy_to_clipboard(result):
                unit_text = self.time_unit.get()
                self.show_message("成功", f"时间戳({unit_text})已复制到剪贴板")
        
        except ValueError:
            self.show_message("错误", "无效的时间戳", "error")