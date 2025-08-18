#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者工具集 - 主程序
集成多种开发常用工具
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFrame, QSizePolicy,
                             QButtonGroup, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from tools.json_formatter_tool import JSONFormatterTool
from tools.timestamp_converter_tool import TimestampConverterTool


class DeveloperToolkit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("开发者工具集")
        self.setGeometry(100, 100, 1200, 800)
        
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
                            self.setWindowIcon(QIcon(icon_path))
                            return
                        except Exception:
                            continue
        except Exception:
            pass
    
    def setup_styles(self):
        """设置样式"""
        # 设置应用程序样式
        font = QFont("Segoe UI", 9)
        QApplication.setFont(font)
    
    def setup_ui(self):
        """创建用户界面"""
        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 工具选择区域
        tool_frame = QWidget()
        tool_layout = QHBoxLayout(tool_frame)
        tool_layout.setContentsMargins(0, 0, 0, 10)
        
        label = QLabel("选择工具:")
        font = QFont("Segoe UI", 12, QFont.Bold)
        label.setFont(font)
        tool_layout.addWidget(label)
        
        # 工具按钮
        self.tool_buttons = {}
        
        # JSON格式化工具按钮
        json_btn = QPushButton("📝 JSON格式化")
        json_btn.clicked.connect(lambda: self.switch_tool('json_formatter'))
        json_btn.setFixedHeight(40)
        json_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border: 2px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        tool_layout.addWidget(json_btn)
        self.tool_buttons['json_formatter'] = json_btn
        
        # 时间戳转换工具按钮
        timestamp_btn = QPushButton("⏰ 时间戳转换")
        timestamp_btn.clicked.connect(lambda: self.switch_tool('timestamp_converter'))
        timestamp_btn.setFixedHeight(40)
        timestamp_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 15px;
                padding: 10px 20px;
                border: 2px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        tool_layout.addWidget(timestamp_btn)
        self.tool_buttons['timestamp_converter'] = timestamp_btn
        
        tool_layout.addStretch()
        main_layout.addWidget(tool_frame)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # 工具内容区域
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.content_widget)
        
        # 默认显示JSON格式化工具
        self.current_tool = None
        self.switch_tool('json_formatter')
    
    def switch_tool(self, tool_name):
        """切换工具"""
        if self.current_tool == tool_name:
            return
        
        # 清空当前内容
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # 清空工具缓存
        self.tools.clear()
        
        # 更新按钮样式
        for name, button in self.tool_buttons.items():
            if name == tool_name:
                button.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        font-size: 15px;
                        padding: 10px 20px;
                        border: 2px solid #0078d4;
                        border-radius: 4px;
                        background-color: #0078d4;
                        color: white;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        font-weight: bold;
                        font-size: 15px;
                        padding: 10px 20px;
                        border: 2px solid #cccccc;
                        border-radius: 4px;
                        background-color: white;
                    }
                    QPushButton:hover {
                        background-color: #f0f0f0;
                    }
                """)
        
        # 创建新工具实例
        if tool_name == 'json_formatter':
            self.tools[tool_name] = JSONFormatterTool(self.content_widget)
        elif tool_name == 'timestamp_converter':
            self.tools[tool_name] = TimestampConverterTool(self.content_widget)
        
        # 添加工具到界面
        if tool_name in self.tools:
            self.content_layout.addWidget(self.tools[tool_name].main_widget)
        
        self.current_tool = tool_name


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("开发者工具集")
    
    # 设置样式表
    app.setStyleSheet("""
        QMainWindow {
            background-color: white;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 1ex;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    
    window = DeveloperToolkit()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()