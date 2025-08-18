#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具基类
定义工具的通用接口和功能
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QMessageBox, QApplication, QFrame, QStyle)
from PyQt5.QtCore import Qt, pyqtSignal
from abc import ABC, abstractmethod


class BaseTool(ABC):
    """工具基类"""
    
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self.main_widget = None
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """设置用户界面 - 子类必须实现"""
        pass
    
    def show(self):
        """显示工具界面"""
        if self.main_widget:
            self.main_widget.show()
    
    def hide(self):
        """隐藏工具界面"""
        if self.main_widget:
            self.main_widget.hide()
    
    def copy_to_clipboard(self, text):
        """复制文本到剪贴板"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            return True
        except Exception:
            return False
    
    def show_message(self, title, message, msg_type="info"):
        """显示消息"""
        msg_box = QMessageBox(self.parent_widget) if self.parent_widget else QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif msg_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif msg_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        
        msg_box.exec_()
    
    def create_button_frame(self, parent, buttons_config):
        """创建按钮框架"""
        button_frame = QWidget(parent)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        # 居中的按钮容器
        button_container = QWidget()
        container_layout = QHBoxLayout(button_container)
        container_layout.addStretch()
        
        for config in buttons_config:
            btn = QPushButton(config.get('text', ''), button_container)
            btn.clicked.connect(config.get('command', lambda: None))
            if 'width' in config:
                btn.setFixedWidth(config['width'] * 10)  # 粗略转换
            # 样式需要在子类中设置
            container_layout.addWidget(btn)
        
        container_layout.addStretch()
        button_layout.addWidget(button_container)
        
        return button_frame