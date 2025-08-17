#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON格式化工具
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from .base_tool import BaseTool


class JSONFormatterTool(BaseTool):
    """JSON格式化工具类"""
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        self.main_frame = ttk.Frame(self.parent_frame, padding="5")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置样式
        self.setup_styles()
        
        # 创建按钮区域
        self.create_button_area()
        
        # 创建内容区域
        self.create_content_area()
        
        # 创建状态栏
        self.create_status_bar()
    
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
    
    def create_button_area(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.main_frame, padding="8")
        button_frame.pack(fill=tk.X, pady=(0, 12))
        
        # 居中的按钮容器
        button_container = ttk.Frame(button_frame)
        button_container.pack(expand=True)
        
        # 主要功能按钮组
        main_group = ttk.Frame(button_container)
        main_group.pack(side=tk.LEFT, padx=(0, 20))
        
        # 格式化按钮
        format_btn = ttk.Button(main_group, text="✨ 格式化", command=self.format_json, 
                               width=12, style="Primary.TButton")
        format_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 压缩按钮
        compress_btn = ttk.Button(main_group, text="📦 压缩", command=self.compress_json, 
                                 width=10, style="Secondary.TButton")
        compress_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 验证按钮
        validate_btn = ttk.Button(main_group, text="✅ 验证", command=self.validate_json, 
                                 width=10, style="Secondary.TButton")
        validate_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 辅助功能按钮组
        aux_group = ttk.Frame(button_container)
        aux_group.pack(side=tk.LEFT)
        
        # 清空按钮
        clear_btn = ttk.Button(aux_group, text="🗑️ 清空", command=self.clear_all, 
                              width=10, style="Danger.TButton")
        clear_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        # 文件操作按钮
        open_btn = ttk.Button(aux_group, text="📂 打开", command=self.open_file, 
                             width=10, style="Secondary.TButton")
        open_btn.pack(side=tk.LEFT, padx=3, pady=2)
        
        save_btn = ttk.Button(aux_group, text="💾 保存", command=self.save_file, 
                             width=10, style="Secondary.TButton")
        save_btn.pack(side=tk.LEFT, padx=3, pady=2)
    
    def create_content_area(self):
        """创建内容区域"""
        # 可拖动的分割窗口
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # 左侧输入区域
        input_frame = ttk.LabelFrame(self.paned_window, text="📝 输入JSON", padding="5")
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # 输入文本框
        self.input_text = tk.Text(input_frame, wrap=tk.WORD, font=('Consolas', 10), 
                                 relief=tk.FLAT, borderwidth=1)
        input_scrollbar = ttk.Scrollbar(input_frame, orient=tk.VERTICAL, command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=input_scrollbar.set)
        
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 右侧输出区域
        output_frame = ttk.LabelFrame(self.paned_window, text="✨ 格式化结果", padding="5")
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # 输出文本框
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, font=('Consolas', 10),
                                  relief=tk.FLAT, borderwidth=1)
        output_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=output_scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 将左右面板添加到分割窗口
        self.paned_window.add(input_frame, weight=1)
        self.paned_window.add(output_frame, weight=1)
        
        # 设置初始分割位置
        self.main_frame.after(100, self.set_initial_sash_position)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 - 支持JSON和Python字典格式 | 拖动中间分割线调整窗口大小")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(10, 0), padx=5)
    
    def set_initial_sash_position(self):
        """设置初始分割位置为窗口中央"""
        try:
            if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
                window_width = self.main_frame.winfo_width()
                if window_width > 100:
                    self.paned_window.sashpos(0, window_width // 2 - 50)
        except (tk.TclError, AttributeError):
            # 如果组件已被销毁或不存在，重试
            if hasattr(self, 'main_frame'):
                self.main_frame.after(100, self.set_initial_sash_position)
    
    def parse_input(self, input_text):
        """智能解析输入内容，支持JSON和Python字典格式"""
        errors = []
        
        # 首先尝试标准JSON解析
        try:
            return json.loads(input_text)
        except json.JSONDecodeError as e:
            line_num = getattr(e, 'lineno', 1)
            col_num = getattr(e, 'colno', 1)
            error_msg = str(e.msg) if hasattr(e, 'msg') else str(e)
            
            lines = input_text.split('\n')
            if line_num <= len(lines):
                error_line = lines[line_num - 1]
                pointer = ' ' * (col_num - 1) + '^'
                context = f"第{line_num}行，第{col_num}列:\n{error_line}\n{pointer}"
            else:
                context = f"第{line_num}行，第{col_num}列"
            
            errors.append(f"JSON格式错误: {error_msg}\n位置: {context}")
        
        # 如果JSON解析失败，尝试作为Python字典解析
        try:
            import ast
            return ast.literal_eval(input_text)
        except (ValueError, SyntaxError) as e:
            if hasattr(e, 'lineno') and hasattr(e, 'offset'):
                line_num = e.lineno
                col_num = e.offset or 1
                lines = input_text.split('\n')
                if line_num <= len(lines):
                    error_line = lines[line_num - 1]
                    pointer = ' ' * (col_num - 1) + '^'
                    context = f"第{line_num}行，第{col_num}列:\n{error_line}\n{pointer}"
                else:
                    context = f"第{line_num}行，第{col_num}列"
                errors.append(f"Python字典格式错误: {str(e)}\n位置: {context}")
            else:
                errors.append(f"Python字典格式错误: {str(e)}")
        
        # 如果都失败，抛出详细错误
        error_summary = "无法解析输入内容，发现以下问题:\n\n" + "\n\n".join(errors)
        error_summary += "\n\n建议检查:\n• 括号、引号是否配对\n• 逗号是否正确使用\n• 键名是否用引号包围\n• 是否有多余的逗号"
        raise ValueError(error_summary)
    
    def format_json(self):
        """格式化JSON"""
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            json_obj = self.parse_input(input_text)
            formatted_json = json.dumps(json_obj, ensure_ascii=False, indent=4, sort_keys=True)
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", formatted_json)
            
            self.status_var.set("JSON格式化完成")
            
        except ValueError as e:
            self.show_detailed_error("格式化失败", str(e))
            self.status_var.set("格式化失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("错误", f"格式化失败: {str(e)}", "error")
            self.status_var.set("格式化失败")
    
    def compress_json(self):
        """压缩JSON"""
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            json_obj = self.parse_input(input_text)
            compressed_json = json.dumps(json_obj, ensure_ascii=False, separators=(',', ':'))
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", compressed_json)
            
            self.status_var.set("JSON压缩完成")
            
        except ValueError as e:
            self.show_detailed_error("压缩失败", str(e))
            self.status_var.set("压缩失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("错误", f"压缩失败: {str(e)}", "error")
            self.status_var.set("压缩失败")
    
    def validate_json(self):
        """验证JSON"""
        try:
            input_text = self.input_text.get("1.0", tk.END).strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            self.parse_input(input_text)
            self.show_message("验证结果", "✅ 格式正确！\n\n已成功解析为JSON对象")
            self.status_var.set("格式验证通过")
            
        except ValueError as e:
            self.show_detailed_error("验证失败", str(e))
            self.status_var.set("格式验证失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("验证结果", f"格式错误: {str(e)}", "error")
            self.status_var.set("格式验证失败")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.status_var.set("已清空")
    
    def open_file(self):
        """打开文件"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择JSON文件",
                filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                
                self.status_var.set(f"已打开文件: {os.path.basename(file_path)}")
                
        except Exception as e:
            self.show_message("错误", f"打开文件失败: {str(e)}", "error")
            self.status_var.set("打开文件失败")
    
    def save_file(self):
        """保存文件"""
        try:
            output_content = self.output_text.get("1.0", tk.END).strip()
            if not output_content:
                self.show_message("警告", "没有内容可保存", "warning")
                return
            
            file_path = filedialog.asksaveasfilename(
                title="保存JSON文件",
                defaultextension=".json",
                filetypes=[("JSON文件", "*.json"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                
                self.status_var.set(f"已保存文件: {os.path.basename(file_path)}")
                self.show_message("成功", "文件保存成功！")
                
        except Exception as e:
            self.show_message("错误", f"保存文件失败: {str(e)}", "error")
            self.status_var.set("保存文件失败")
    
    def show_detailed_error(self, title, error_message):
        """显示详细的错误信息对话框"""
        error_window = tk.Toplevel(self.parent_frame)
        error_window.title(title)
        error_window.geometry("600x400")
        error_window.resizable(True, True)
        
        error_window.transient(self.parent_frame)
        error_window.grab_set()
        
        main_frame = ttk.Frame(error_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="❌ " + title, 
                               font=('Segoe UI', 12, 'bold'),
                               foreground='#d13438')
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        error_text = tk.Text(text_frame, wrap=tk.WORD, font=('Consolas', 10),
                            relief=tk.FLAT, borderwidth=1, background='#f8f8f8')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=error_text.yview)
        error_text.configure(yscrollcommand=scrollbar.set)
        
        error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        error_text.insert("1.0", error_message)
        error_text.configure(state=tk.DISABLED)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        copy_btn = ttk.Button(button_frame, text="📋 复制错误信息", 
                             command=lambda: self.copy_to_clipboard(error_message))
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = ttk.Button(button_frame, text="关闭", 
                              command=error_window.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (error_window.winfo_width() // 2)
        y = (error_window.winfo_screenheight() // 2) - (error_window.winfo_height() // 2)
        error_window.geometry(f"+{x}+{y}")
        
        close_btn.focus_set()