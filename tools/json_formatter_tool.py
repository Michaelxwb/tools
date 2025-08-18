#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON格式化工具
"""

import json
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTextEdit, QSplitter, QFileDialog, 
                             QMessageBox, QDialog, QStyle, QFrame, QSizePolicy,
                             QTreeWidget, QTreeWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor
from .base_tool import BaseTool


class JSONFormatterTool(BaseTool):
    """JSON格式化工具类"""
    
    def setup_ui(self):
        """设置用户界面"""
        # 主窗口部件
        self.main_widget = QWidget(self.parent_widget)
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建按钮区域
        self.create_button_area()
        main_layout.addWidget(self.button_area)
        
        # 创建内容区域
        self.create_content_area()
        main_layout.addWidget(self.content_area, 1)
        
        # 创建状态栏
        self.create_status_bar()
        main_layout.addWidget(self.status_bar)
    
    def create_button_area(self):
        """创建按钮区域"""
        self.button_area = QWidget()
        button_layout = QHBoxLayout(self.button_area)
        button_layout.setContentsMargins(8, 8, 8, 8)
        
        # 居中的按钮容器
        button_container = QWidget()
        container_layout = QHBoxLayout(button_container)
        container_layout.addStretch()
        
        # 主要功能按钮组
        main_group = QWidget()
        main_group_layout = QHBoxLayout(main_group)
        main_group_layout.setContentsMargins(0, 0, 0, 0)
        
        # 格式化按钮
        format_btn = QPushButton("✨ 格式化")
        format_btn.clicked.connect(self.format_json)
        format_btn.setFixedWidth(120)
        format_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        main_group_layout.addWidget(format_btn)
        
        # 压缩按钮
        compress_btn = QPushButton("📦 压缩")
        compress_btn.clicked.connect(self.compress_json)
        compress_btn.setFixedWidth(100)
        compress_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #498205;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3c6a04;
            }
            QPushButton:pressed {
                background-color: #2f5203;
            }
        """)
        main_group_layout.addWidget(compress_btn)
        
        # 验证按钮
        validate_btn = QPushButton("✅ 验证")
        validate_btn.clicked.connect(self.validate_json)
        validate_btn.setFixedWidth(100)
        validate_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #4868ac;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3b5a9a;
            }
            QPushButton:pressed {
                background-color: #2e4b89;
            }
        """)
        main_group_layout.addWidget(validate_btn)
        
        container_layout.addWidget(main_group)
        
        # 辅助功能按钮组
        aux_group = QWidget()
        aux_group_layout = QHBoxLayout(aux_group)
        aux_group_layout.setContentsMargins(0, 0, 0, 0)
        
        # 清空按钮
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setFixedWidth(100)
        clear_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #d13438;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #a4262c;
            }
            QPushButton:pressed {
                background-color: #8b1f24;
            }
        """)
        aux_group_layout.addWidget(clear_btn)
        
        # 文件操作按钮
        open_btn = QPushButton("📂 打开")
        open_btn.clicked.connect(self.open_file)
        open_btn.setFixedWidth(100)
        open_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #881798;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #721481;
            }
            QPushButton:pressed {
                background-color: #5c106a;
            }
        """)
        aux_group_layout.addWidget(open_btn)
        
        save_btn = QPushButton("💾 保存")
        save_btn.clicked.connect(self.save_file)
        save_btn.setFixedWidth(100)
        save_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #107c10;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:pressed {
                background-color: #0c5f0c;
            }
        """)
        aux_group_layout.addWidget(save_btn)
        
        container_layout.addWidget(aux_group)
        container_layout.addStretch()
        button_layout.addWidget(button_container)
    
    def create_content_area(self):
        """创建内容区域"""
        self.content_area = QSplitter(Qt.Horizontal)
        
        # 左侧输入区域
        input_widget = QFrame()
        input_widget.setFrameStyle(QFrame.StyledPanel)
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(5, 5, 5, 5)
        
        input_label = QLabel("📝 输入JSON")
        input_label.setStyleSheet("font-weight: bold;")
        input_layout.addWidget(input_label)
        
        # 输入文本框
        self.input_text = QTextEdit()
        font = QFont("Consolas", 10)
        self.input_text.setFont(font)
        input_layout.addWidget(self.input_text)
        
        # 右侧输出区域（使用标签页方式展示文本和树形视图）
        self.output_widget = QFrame()
        self.output_widget.setFrameStyle(QFrame.StyledPanel)
        self.output_layout = QVBoxLayout(self.output_widget)
        self.output_layout.setContentsMargins(5, 5, 5, 5)
        
        output_label = QLabel("✨ 格式化结果")
        output_label.setStyleSheet("font-weight: bold;")
        self.output_layout.addWidget(output_label)
        
        # 创建分割器用于文本视图和树形视图
        self.output_splitter = QSplitter(Qt.Vertical)
        
        # 输出文本框
        self.output_text = QTextEdit()
        self.output_text.setFont(font)
        self.output_text.setReadOnly(True)
        
        # 树形视图容器
        tree_container = QWidget()
        tree_layout = QVBoxLayout(tree_container)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        
        # 树形视图控制按钮
        tree_control_layout = QHBoxLayout()
        tree_control_layout.setContentsMargins(0, 0, 0, 5)
        
        expand_all_btn = QPushButton("展开全部")
        expand_all_btn.clicked.connect(self.expand_all_tree)
        expand_all_btn.setFixedWidth(80)
        expand_all_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        collapse_all_btn = QPushButton("快速折叠")
        collapse_all_btn.clicked.connect(self.collapse_all_tree)
        collapse_all_btn.setFixedWidth(80)
        collapse_all_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #4868ac;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3b5a9a;
            }
            QPushButton:pressed {
                background-color: #2e4b89;
            }
        """)
        
        tree_control_layout.addWidget(expand_all_btn)
        tree_control_layout.addWidget(collapse_all_btn)
        tree_control_layout.addStretch()
        
        tree_layout.addLayout(tree_control_layout)
        
        # 树形视图
        self.tree_view = QTreeWidget()
        self.tree_view.setHeaderLabels(["Key", "Value"])
        self.tree_view.header().setSectionResizeMode(QHeaderView.Interactive)
        self.tree_view.setAlternatingRowColors(True)
        self.tree_view.setStyleSheet("""
            QTreeWidget {
                alternate-background-color: #f0f0f0;
            }
        """)
        
        # 连接树形视图的点击事件
        self.tree_view.itemClicked.connect(self.on_tree_item_clicked)
        
        tree_layout.addWidget(self.tree_view)
        
        self.output_splitter.addWidget(self.output_text)
        self.output_splitter.addWidget(tree_container)
        self.output_splitter.setSizes([400, 400])
        
        self.output_layout.addWidget(self.output_splitter)
        
        # 添加到分割器
        self.content_area.addWidget(input_widget)
        self.content_area.addWidget(self.output_widget)
        self.content_area.setSizes([500, 500])
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QLabel()
        self.status_bar.setText("就绪 - 支持JSON和Python字典格式 | 拖动中间分割线调整窗口大小")
        self.status_bar.setStyleSheet("""
            QLabel {
                background-color: #f3f2f1;
                border: 1px solid #e1dfdd;
                padding: 4px;
                font-size: 12px;
            }
        """)
        self.status_bar.setFixedHeight(30)
    
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
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            json_obj = self.parse_input(input_text)
            formatted_json = json.dumps(json_obj, ensure_ascii=False, indent=4, sort_keys=True)
            
            self.output_text.clear()
            self.output_text.setPlainText(formatted_json)
            
            # 更新树形视图
            self.update_tree_view(json_obj)
            
            self.status_bar.setText("JSON格式化完成")
            
        except ValueError as e:
            self.show_detailed_error("格式化失败", str(e))
            self.status_bar.setText("格式化失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("错误", f"格式化失败: {str(e)}", "error")
            self.status_bar.setText("格式化失败")
    
    def update_tree_view(self, data):
        """更新树形视图"""
        self.tree_view.clear()
        if data is not None:
            self.add_tree_items(self.tree_view, data)
            self.tree_view.expandAll()
            self.tree_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            self.tree_view.header().setSectionResizeMode(1, QHeaderView.Stretch)
    
    def add_tree_items(self, parent, data, key=""):
        """递归添加树形项目"""
        if isinstance(data, dict):
            for k, v in data.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, str(k))
                if isinstance(v, (dict, list)):
                    item.setText(1, "..." if isinstance(v, dict) else f"[{len(v)} items]")
                    self.add_tree_items(item, v, k)
                else:
                    item.setText(1, str(v) if v is not None else "null")
                    # 设置不可展开的项
                    item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
        elif isinstance(data, list):
            for i, v in enumerate(data):
                item = QTreeWidgetItem(parent)
                item.setText(0, str(i))
                if isinstance(v, (dict, list)):
                    item.setText(1, "..." if isinstance(v, dict) else f"[{len(v)} items]")
                    self.add_tree_items(item, v, str(i))
                else:
                    item.setText(1, str(v) if v is not None else "null")
                    # 设置不可展开的项
                    item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicatorWhenChildless)
    
    def on_tree_item_clicked(self, item, column):
        """处理树形项目点击事件"""
        # 切换展开/折叠状态
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
    
    def expand_all_tree(self):
        """展开所有树节点"""
        self.tree_view.expandAll()
    
    def collapse_all_tree(self):
        """折叠所有树节点"""
        self.tree_view.collapseAll()
    
    def compress_json(self):
        """压缩JSON"""
        try:
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            json_obj = self.parse_input(input_text)
            compressed_json = json.dumps(json_obj, ensure_ascii=False, separators=(',', ':'))
            
            self.output_text.clear()
            self.output_text.setPlainText(compressed_json)
            
            # 更新树形视图
            self.update_tree_view(json_obj)
            
            self.status_bar.setText("JSON压缩完成")
            
        except ValueError as e:
            self.show_detailed_error("压缩失败", str(e))
            self.status_bar.setText("压缩失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("错误", f"压缩失败: {str(e)}", "error")
            self.status_bar.setText("压缩失败")
    
    def validate_json(self):
        """验证JSON"""
        try:
            input_text = self.input_text.toPlainText().strip()
            if not input_text:
                self.show_message("警告", "请输入JSON内容", "warning")
                return
            
            self.parse_input(input_text)
            self.show_message("验证结果", "✅ 格式正确！\n\n已成功解析为JSON对象")
            self.status_bar.setText("格式验证通过")
            
        except ValueError as e:
            self.show_detailed_error("验证失败", str(e))
            self.status_bar.setText("格式验证失败 - 请检查语法错误")
        except Exception as e:
            self.show_message("验证结果", f"格式错误: {str(e)}", "error")
            self.status_bar.setText("格式验证失败")
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.clear()
        self.output_text.clear()
        self.tree_view.clear()
        self.status_bar.setText("已清空")
    
    def open_file(self):
        """打开文件"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_widget,
                "选择JSON文件",
                "",
                "JSON文件 (*.json);;文本文件 (*.txt);;所有文件 (*.*)"
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.input_text.clear()
                self.input_text.setPlainText(content)
                
                self.status_bar.setText(f"已打开文件: {os.path.basename(file_path)}")
                
        except Exception as e:
            self.show_message("错误", f"打开文件失败: {str(e)}", "error")
            self.status_bar.setText("打开文件失败")
    
    def save_file(self):
        """保存文件"""
        try:
            output_content = self.output_text.toPlainText().strip()
            if not output_content:
                self.show_message("警告", "没有内容可保存", "warning")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_widget,
                "保存JSON文件",
                "",
                "JSON文件 (*.json);;文本文件 (*.txt);;所有文件 (*.*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                
                self.status_bar.setText(f"已保存文件: {os.path.basename(file_path)}")
                self.show_message("成功", "文件保存成功！")
                
        except Exception as e:
            self.show_message("错误", f"保存文件失败: {str(e)}", "error")
            self.status_bar.setText("保存文件失败")
    
    def show_detailed_error(self, title, error_message):
        """显示详细的错误信息对话框"""
        error_dialog = QDialog(self.main_widget)
        error_dialog.setWindowTitle(title)
        error_dialog.resize(600, 400)
        
        layout = QVBoxLayout(error_dialog)
        
        # 标题
        title_label = QLabel("❌ " + title)
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #d13438;
            }
        """)
        layout.addWidget(title_label)
        
        # 错误信息文本框
        error_text = QTextEdit()
        error_text.setPlainText(error_message)
        error_text.setReadOnly(True)
        font = QFont("Consolas", 10)
        error_text.setFont(font)
        error_text.setStyleSheet("background-color: #f8f8f8;")
        layout.addWidget(error_text, 1)
        
        # 按钮区域
        button_frame = QWidget()
        button_layout = QHBoxLayout(button_frame)
        
        copy_btn = QPushButton("📋 复制错误信息")
        copy_btn.clicked.connect(lambda: self.copy_to_clipboard(error_message))
        button_layout.addWidget(copy_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(error_dialog.close)
        button_layout.addWidget(close_btn)
        
        layout.addWidget(button_frame)
        
        error_dialog.exec_()