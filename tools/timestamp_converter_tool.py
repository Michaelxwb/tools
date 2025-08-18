#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间戳转换工具
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QGroupBox, QRadioButton, 
                             QFrame, QSizePolicy, QButtonGroup)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import time
import datetime
from .base_tool import BaseTool


class TimestampConverterTool(BaseTool):
    """时间戳转换工具类"""
    
    def setup_ui(self):
        """设置用户界面"""
        # 主窗口部件
        self.main_widget = QWidget(self.parent_widget)
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 初始化更新标志
        self.is_updating = True
        
        # 创建当前时间显示区域
        self.create_current_time_area()
        main_layout.addWidget(self.current_time_group)
        
        # 创建时间戳转换区域
        self.create_timestamp_converter_area()
        main_layout.addWidget(self.timestamp_converter_group)
        
        # 创建时间转时间戳区域
        self.create_datetime_converter_area()
        main_layout.addWidget(self.datetime_converter_group)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        # 启动时间更新
        self.update_current_time()
    
    def create_current_time_area(self):
        """创建当前时间显示区域"""
        self.current_time_group = QGroupBox("当前时间")
        group_layout = QVBoxLayout(self.current_time_group)
        group_layout.setContentsMargins(15, 15, 15, 15)
        
        # 当前时间显示
        time_display_frame = QWidget()
        time_display_layout = QHBoxLayout(time_display_frame)
        time_display_layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("当前Unix时间戳:")
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        time_display_layout.addWidget(label)
        
        self.current_timestamp_label = QLabel()
        self.current_timestamp_label.setFont(QFont("Consolas", 12, QFont.Bold))
        self.current_timestamp_label.setStyleSheet("color: #0078d4; font-size: 16px;")
        time_display_layout.addWidget(self.current_timestamp_label)
        time_display_layout.addStretch()
        
        # 停止和复制按钮
        self.stop_btn = QPushButton("⏸️ 停止")
        self.stop_btn.clicked.connect(self.toggle_update)
        self.stop_btn.setFixedWidth(80)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #d13438;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #a4262c;
            }
            QPushButton:pressed {
                background-color: #8b1f24;
            }
        """)
        time_display_layout.addWidget(self.stop_btn)
        
        copy_btn = QPushButton("📋 复制")
        copy_btn.clicked.connect(self.copy_current_timestamp)
        copy_btn.setFixedWidth(80)
        copy_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #881798;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #721481;
            }
            QPushButton:pressed {
                background-color: #5c106a;
            }
        """)
        time_display_layout.addWidget(copy_btn)
        
        group_layout.addWidget(time_display_frame)
    
    def create_timestamp_converter_area(self):
        """创建时间戳转换区域"""
        self.timestamp_converter_group = QGroupBox("Unix时间戳转换")
        group_layout = QVBoxLayout(self.timestamp_converter_group)
        group_layout.setContentsMargins(15, 15, 15, 15)
        
        # 输入行
        input_frame = QWidget()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 15)
        
        label = QLabel("Unix时间戳")
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        input_layout.addWidget(label)
        
        self.timestamp_entry = QLineEdit()
        self.timestamp_entry.setFont(QFont("Consolas", 12))
        self.timestamp_entry.setFixedWidth(150)
        input_layout.addWidget(self.timestamp_entry)
        
        convert_btn = QPushButton("🔄 转换")
        convert_btn.clicked.connect(self.convert_timestamp)
        convert_btn.setFixedWidth(80)
        convert_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px;
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
        input_layout.addWidget(convert_btn)
        input_layout.addStretch()
        
        group_layout.addWidget(input_frame)
        
        # 结果显示
        result_frame = QWidget()
        result_layout = QHBoxLayout(result_frame)
        result_layout.setContentsMargins(0, 0, 0, 0)
        
        self.timestamp_result_entry = QLineEdit()
        self.timestamp_result_entry.setFont(QFont("Consolas", 12))
        self.timestamp_result_entry.setReadOnly(True)
        self.timestamp_result_entry.setFixedWidth(250)
        result_layout.addWidget(self.timestamp_result_entry)
        
        copy_result_btn = QPushButton("📋 复制")
        copy_result_btn.clicked.connect(lambda: self.copy_to_clipboard(self.timestamp_result_entry.text()))
        copy_result_btn.setFixedWidth(80)
        copy_result_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #881798;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #721481;
            }
            QPushButton:pressed {
                background-color: #5c106a;
            }
        """)
        result_layout.addWidget(copy_result_btn)
        result_layout.addStretch()
        
        group_layout.addWidget(result_frame)
    
    def create_datetime_converter_area(self):
        """创建时间转时间戳区域"""
        self.datetime_converter_group = QGroupBox("时间转Unix时间戳")
        group_layout = QVBoxLayout(self.datetime_converter_group)
        group_layout.setContentsMargins(15, 15, 15, 15)
        group_layout.setSpacing(10)
        
        # 输入行
        input_frame = QWidget()
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("时间转Unix时间戳(年-月-日 时:分:秒)")
        font = QFont()
        font.setPointSize(12)
        label.setFont(font)
        input_layout.addWidget(label)
        
        self.datetime_entry = QLineEdit()
        self.datetime_entry.setFont(QFont("Consolas", 12))
        self.datetime_entry.setFixedWidth(200)
        input_layout.addWidget(self.datetime_entry)
        
        convert_dt_btn = QPushButton("🔄 转换")
        convert_dt_btn.clicked.connect(self.convert_datetime)
        convert_dt_btn.setFixedWidth(80)
        convert_dt_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px;
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
        input_layout.addWidget(convert_dt_btn)
        input_layout.addStretch()
        
        group_layout.addWidget(input_frame)
        
        # 结果显示
        result_frame = QWidget()
        result_layout = QHBoxLayout(result_frame)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(10)
        
        # 时间单位选择
        unit_group = QButtonGroup()
        second_radio = QRadioButton("秒")
        millisecond_radio = QRadioButton("毫秒")
        second_radio.setChecked(True)
        unit_group.addButton(second_radio)
        unit_group.addButton(millisecond_radio)
        
        # 将毫秒单选按钮保存为实例变量
        self.milliseconds_radio = millisecond_radio
        
        # 单位选择标签和控件
        unit_label = QLabel("单位:")
        unit_label.setFixedWidth(40)
        
        second_radio.setFixedWidth(40)
        millisecond_radio.setFixedWidth(60)
        
        # 结果显示框
        self.datetime_result_entry = QLineEdit()
        self.datetime_result_entry.setFont(QFont("Consolas", 12))
        self.datetime_result_entry.setReadOnly(True)
        self.datetime_result_entry.setFixedWidth(150)
        
        # 复制按钮
        copy_result_btn = QPushButton("📋 复制")
        copy_result_btn.clicked.connect(lambda: self.copy_to_clipboard(self.datetime_result_entry.text()))
        copy_result_btn.setFixedWidth(80)
        copy_result_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #881798;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #721481;
            }
            QPushButton:pressed {
                background-color: #5c106a;
            }
        """)
        
        # 将组件添加到结果布局
        result_layout.addWidget(unit_label)
        result_layout.addWidget(second_radio)
        result_layout.addWidget(millisecond_radio)
        result_layout.addWidget(self.datetime_result_entry)
        result_layout.addWidget(copy_result_btn)
        result_layout.addStretch()
        
        group_layout.addWidget(result_frame)
        
    def update_current_time(self):
        """更新当前时间显示"""
        if self.is_updating and hasattr(self, 'current_timestamp_label'):
            current_timestamp = int(time.time())
            self.current_timestamp_label.setText(str(current_timestamp))
        
        # 每秒更新一次
        QTimer.singleShot(800, self.update_current_time)
    
    def toggle_update(self):
        """切换时间更新状态"""
        self.is_updating = not self.is_updating
        if self.is_updating:
            self.stop_btn.setText("⏸️ 停止")
        else:
            self.stop_btn.setText("▶️ 开始")
    
    def copy_current_timestamp(self):
        """复制当前时间戳"""
        timestamp = self.current_timestamp_label.text()
        if self.copy_to_clipboard(timestamp):
            self.show_message("成功", "当前时间戳已复制到剪贴板")
    
    def convert_timestamp(self):
        """转换时间戳为可读时间"""
        try:
            timestamp_str = self.timestamp_entry.text().strip()
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
            
            self.timestamp_result_entry.setText(readable_time)
            
        except ValueError:
            self.show_message("错误", "请输入有效的时间戳数字", "error")
        except OSError:
            self.show_message("错误", "时间戳超出有效范围", "error")
        except Exception as e:
            self.show_message("错误", f"转换失败: {str(e)}", "error")
    
    def convert_datetime(self):
        """转换时间为时间戳"""
        try:
            datetime_str = self.datetime_entry.text().strip()
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
            
            # 根据用户选择的单位调整时间戳
            if self.milliseconds_radio.isChecked():
                timestamp = timestamp * 1000
            
            self.datetime_result_entry.setText(str(timestamp))
            
        except Exception as e:
            self.show_message("错误", f"转换失败: {str(e)}", "error")
    
    def copy_with_unit(self):
        """根据选择的单位复制时间戳"""
        timestamp_str = self.datetime_result_entry.text()
        if not timestamp_str:
            self.show_message("警告", "请先转换时间", "warning")
            return
        
        try:
            timestamp = int(timestamp_str)
            
            if self.milliseconds_radio.isChecked():
                result = str(timestamp * 1000)
            else:
                result = timestamp_str
            
            if self.copy_to_clipboard(result):
                unit_text = "毫秒" if self.milliseconds_radio.isChecked() else "秒"
                self.show_message("成功", f"时间戳({unit_text})已复制到剪贴板")
        
        except ValueError:
            self.show_message("错误", "无效的时间戳", "error")
