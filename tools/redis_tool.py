#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis连接工具
支持单机和集群模式
"""

import json
import os
import redis
from redis.cluster import RedisCluster
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTextEdit, QComboBox, QTreeWidget, 
                             QTreeWidgetItem, QSplitter, QGroupBox, QSpinBox,
                             QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QSizePolicy, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from .base_tool import BaseTool


class RedisConnectionThread(QThread):
    """Redis连接线程"""
    connection_result = pyqtSignal(bool, str)
    data_loaded = pyqtSignal(dict)
    
    def __init__(self, host, port, password=None, db=0, cluster_mode=False):
        super().__init__()
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.cluster_mode = cluster_mode
        self.redis_client = None
        self.operation = None
        self.pattern = "*"
    
    def run(self):
        """线程主执行方法"""
        try:
            if self.cluster_mode:
                # 集群模式：智能检测和连接
                try:
                    # 步骤1：先测试单机连接获取集群信息
                    test_client = redis.Redis(
                        host=self.host,
                        port=self.port,
                        password=self.password,
                        decode_responses=True,
                        socket_connect_timeout=5,
                        socket_timeout=5
                    )
                    
                    # 检查是否是集群节点
                    try:
                        info = test_client.info()
                        if info.get('redis_mode') != 'cluster':
                            test_client.close()
                            self.connection_result.emit(False, "这不是集群节点，请使用单机模式")
                            return
                    except:
                        pass
                    
                    # 获取集群节点信息
                    try:
                        nodes_info = test_client.execute_command('CLUSTER', 'NODES')
                        test_client.close()
                        
                        # 解析所有节点
                        startup_nodes = []
                        for line in nodes_info.split('\n'):
                            if line.strip() and 'myself' in line:
                                parts = line.split()
                                host_port = parts[1]
                                if '@' in host_port:
                                    host_port = host_port.split('@')[0]
                                if ':' in host_port:
                                    node_host, node_port = host_port.split(':')
                                    startup_nodes.append({"host": node_host, "port": int(node_port)})
                        
                        if not startup_nodes:
                            startup_nodes = [{"host": self.host, "port": self.port}]
                            
                    except:
                        startup_nodes = [{"host": self.host, "port": self.port}]
                    
                    # 使用发现的节点连接
                    self.redis_client = RedisCluster(
                        startup_nodes=startup_nodes,
                        password=self.password,
                        decode_responses=True,
                        skip_full_coverage_check=True,
                        socket_connect_timeout=15,
                        socket_timeout=15,
                        socket_keepalive=True,
                        retry_on_timeout=True,
                        retry_on_error=[ConnectionError, TimeoutError],
                        max_connections=32
                    )
                    
                except Exception as e:
                    # 最后尝试：使用单个节点连接
                    try:
                        self.redis_client = RedisCluster(
                            host=self.host,
                            port=self.port,
                            password=self.password,
                            decode_responses=True,
                            skip_full_coverage_check=True,
                            socket_connect_timeout=15,
                            socket_timeout=15,
                            max_connections=32
                        )
                    except Exception as e2:
                        # 检查具体错误类型
                        error_str = str(e2).lower()
                        if "cluster" in error_str and "not" in error_str:
                            raise Exception("目标Redis不是集群模式，请检查配置")
                        elif "connection" in error_str or "timeout" in error_str:
                            raise Exception(f"连接失败: {e2}")
                        else:
                            raise e2
            else:
                # 单机模式
                self.redis_client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    db=self.db,
                    decode_responses=True,
                    socket_connect_timeout=10,
                    socket_timeout=10,
                    socket_keepalive=True,
                    health_check_interval=30,
                    retry_on_timeout=True
                )
                
                # 测试连接
                self.redis_client.ping()
                
                # 检查是否是集群节点（提供提示）
                try:
                    info = self.redis_client.info()
                    if info.get('redis_mode') == 'cluster' and not self.cluster_mode:
                        self.connection_result.emit(False, "这是集群节点，请使用集群模式连接")
                        return
                except:
                    pass
                    
            self.connection_result.emit(True, "连接成功")
            
        except Exception as e:
            # 智能错误分析
            error_msg = str(e)
            error_lower = error_msg.lower()
            
            if "cluster" in error_lower and ("not" in error_lower or "no" in error_lower):
                error_msg = "目标Redis不是集群模式，请使用单机模式"
            elif "clusterdown" in error_lower:
                error_msg = "集群已下线，请检查集群状态"
            elif "timeout" in error_lower:
                error_msg = "连接超时，请检查网络、防火墙或Redis配置"
            elif "connection" in error_lower or "refused" in error_lower:
                error_msg = "连接被拒绝，请检查Redis是否运行、端口是否正确"
            elif "auth" in error_lower or "password" in error_lower:
                error_msg = "认证失败，请检查密码是否正确"
            elif "busy" in error_lower:
                error_msg = "Redis正忙，请稍后重试"
            else:
                error_msg = f"连接失败: {error_msg}"
                
            self.connection_result.emit(False, error_msg)
    
    def load_keys(self, pattern="*"):
        """加载所有key"""
        if not self.redis_client:
            self.data_loaded.emit({})
            return
            
        try:
            if self.cluster_mode:
                # 集群模式：使用RedisCluster的scan_iter
                keys = list(self.redis_client.scan_iter(match=pattern))
            else:
                # 单机模式
                keys = list(self.redis_client.scan_iter(match=pattern))
            
            key_data = {}
            for key in keys:
                try:
                    key_type = self.redis_client.type(key)
                    ttl = self.redis_client.ttl(key)
                    key_data[key] = {
                        'type': key_type,
                        'ttl': ttl
                    }
                except Exception as e:
                    # 跳过无法访问的key
                    continue
            
            self.data_loaded.emit(key_data)
        except Exception as e:
            print(f"加载key失败: {e}")
            self.data_loaded.emit({})
    
    def get_value(self, key, key_type):
        """获取值"""
        if not self.redis_client:
            return "未连接到Redis"
            
        try:
            if key_type == 'string':
                return self.redis_client.get(key)
            elif key_type == 'list':
                return self.redis_client.lrange(key, 0, -1)
            elif key_type == 'set':
                return list(self.redis_client.smembers(key))
            elif key_type == 'zset':
                return self.redis_client.zrange(key, 0, -1, withscores=True)
            elif key_type == 'hash':
                return self.redis_client.hgetall(key)
            else:
                return f"不支持的数据类型: {key_type}"
        except Exception as e:
            return f"获取值失败: {str(e)}"


class RedisTool(BaseTool):
    """Redis连接工具类"""
    
    def __init__(self, parent_widget=None):
        super().__init__(parent_widget)
        self.redis_client = None
        self.connection_thread = None
        # 使用更可靠的路径
        home_dir = os.path.expanduser("~")
        self.session_file = os.path.join(home_dir, ".redis_sessions.json")
        print(f"会话文件路径: {self.session_file}")
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主窗口部件
        self.main_widget = QWidget(self.parent_widget)
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建连接配置区域
        self.create_connection_area()
        main_layout.addWidget(self.connection_group)
        
        # 创建数据展示区域
        self.create_data_area()
        main_layout.addWidget(self.data_group, 1)
        
        # 延迟加载会话，确保UI完全初始化
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self.load_sessions)
    
    def create_connection_area(self):
        """创建连接配置区域"""
        # 创建主布局容器（不使用GroupBox）
        connection_container = QWidget()
        main_layout = QVBoxLayout(connection_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 标题标签
        title_label = QLabel("Redis连接配置")
        title_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                font-size: 14px;
                color: #0078d4;
                margin-bottom: 10px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # 创建所有输入控件
        self.session_combo = QComboBox()
        self.host_input = QLineEdit("localhost")
        self.port_input = QLineEdit("6379")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.db_input = QSpinBox()
        self.cluster_checkbox = QCheckBox("集群模式")
        
        # 设置控件属性
        self.session_combo.setFixedWidth(150)
        self.session_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.host_input.setFixedWidth(120)
        self.port_input.setFixedWidth(80)
        self.password_input.setFixedWidth(120)
        self.db_input.setRange(0, 15)
        self.db_input.setValue(0)
        self.db_input.setFixedWidth(60)
        
        # 统一样式
        input_style = """
            QLineEdit, QSpinBox, QComboBox {
                height: 30px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 13px;
                background-color: white;
                color: #333;
            }
            QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
                border-color: #0078d4;
                outline: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                selection-background-color: #0078d4;
                selection-color: white;
                color: #333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #ccc;
                border-left-style: solid;
            }
            QComboBox::item {
                color: #333;
                background-color: white;
            }
            QComboBox::item:selected {
                color: white;
                background-color: #0078d4;
            }
            QLabel {
                font-weight: bold;
                font-size: 13px;
                color: #333;
                margin-bottom: 3px;
            }
            QCheckBox {
                font-weight: bold;
                font-size: 13px;
                color: #333;
                spacing: 5px;
            }
        """
        
        # 创建输入组
        def create_input_group(label_text, widget, width=None):
            group = QWidget()
            group_layout = QVBoxLayout(group)
            group_layout.setContentsMargins(0, 0, 0, 0)
            group_layout.setSpacing(2)
            
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 13px;")
            
            if width:
                widget.setFixedWidth(width)
            widget.setFixedHeight(30)
            widget.setStyleSheet(input_style)
            
            group_layout.addWidget(label)
            group_layout.addWidget(widget)
            
            return group
        
        # 连接配置表单
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)
        form_layout.setAlignment(Qt.AlignLeft)
        
        # 添加各个输入组
        form_layout.addWidget(create_input_group("会话", self.session_combo, 150))
        form_layout.addWidget(create_input_group("主机", self.host_input, 120))
        form_layout.addWidget(create_input_group("端口", self.port_input, 80))
        form_layout.addWidget(create_input_group("密码", self.password_input, 120))
        form_layout.addWidget(create_input_group("数据库", self.db_input, 60))
        
        # 集群模式
        cluster_group = QWidget()
        cluster_layout = QVBoxLayout(cluster_group)
        cluster_layout.setContentsMargins(0, 0, 0, 0)
        cluster_layout.setSpacing(2)
        
        cluster_label = QLabel("模式")
        cluster_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.cluster_checkbox.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.cluster_checkbox.setFixedHeight(30)
        
        cluster_layout.addWidget(cluster_label)
        cluster_layout.addWidget(self.cluster_checkbox)
        
        form_layout.addWidget(cluster_group)
        
        # 操作按钮
        # 连接按钮
        self.connect_btn = QPushButton("🔗 连接")
        self.connect_btn.setFixedWidth(80)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #0078d4;
                color: white;
                border: 2px solid #0078d4;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #106ebe;
                border-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
                border-color: #005a9e;
            }
        """)
        self.connect_btn.clicked.connect(self.connect_redis)
        form_layout.addWidget(self.connect_btn)
        
        self.disconnect_btn = QPushButton("❌ 断开")
        self.disconnect_btn.setFixedWidth(80)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #dc3545;
                color: white;
                border: 2px solid #dc3545;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
                border-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
                border-color: #bd2130;
            }
        """)
        self.disconnect_btn.clicked.connect(self.disconnect_redis)
        self.disconnect_btn.setEnabled(False)
        form_layout.addWidget(self.disconnect_btn)
        
        # 会话管理按钮
        self.save_session_btn = QPushButton("💾 保存")
        self.save_session_btn.setFixedWidth(80)
        self.save_session_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #28a745;
                color: white;
                border: 2px solid #28a745;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #218838;
                border-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
                border-color: #1e7e34;
            }
        """)
        self.save_session_btn.clicked.connect(self.save_current_session)
        form_layout.addWidget(self.save_session_btn)
        
        # 测试连接按钮
        self.test_btn = QPushButton("🧪 测试")
        self.test_btn.setFixedWidth(80)
        self.test_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #17a2b8;
                color: white;
                border: 2px solid #17a2b8;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #138496;
                border-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
                border-color: #117a8b;
            }
        """)
        self.test_btn.clicked.connect(self.test_connection)
        form_layout.addWidget(self.test_btn)
        
        self.delete_session_btn = QPushButton("🗑️ 删除")
        self.delete_session_btn.setFixedWidth(80)
        self.delete_session_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                font-size: 13px;
                background-color: #6c757d;
                color: white;
                border: 2px solid #6c757d;
                padding: 6px 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a6268;
                border-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
                border-color: #545b62;
            }
        """)
        self.delete_session_btn.clicked.connect(self.delete_current_session)
        form_layout.addWidget(self.delete_session_btn)
        
        form_layout.addStretch()
        main_layout.addLayout(form_layout)
        
        # 状态标签（单独一行显示）
        self.status_label = QLabel("未连接")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-weight: bold;
                padding: 5px 10px;
                background-color: transparent;
                min-width: 80px;
                text-align: left;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # 将容器添加到connection_group中
        self.connection_group = connection_container
    
    def create_data_area(self):
        """创建数据展示区域"""
        self.data_group = QGroupBox("Redis数据")
        self.data_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #28a745;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #28a745;
            }
        """)
        
        layout = QVBoxLayout(self.data_group)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 搜索区域
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索模式:")
        search_label.setStyleSheet("font-weight: bold;")
        self.search_input = QLineEdit("*")
        self.search_input.setPlaceholderText("输入key搜索模式...")
        self.search_input.setFixedWidth(200)
        
        self.search_btn = QPushButton("🔍 搜索")
        self.search_btn.setFixedWidth(80)
        self.search_btn.setStyleSheet("""
            QPushButton {
                font-weight: bold;
                background-color: #6f42c1;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5e2e8c;
            }
        """)
        self.search_btn.clicked.connect(self.load_keys)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # 数据展示区域
        self.data_splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：key列表
        self.key_tree = QTreeWidget()
        self.key_tree.setHeaderLabels(["Key", "Type", "TTL"])
        self.key_tree.setAlternatingRowColors(True)
        self.key_tree.setStyleSheet("""
            QTreeWidget {
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
            QTreeWidget::item {
                padding: 4px;
            }
            QTreeWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        self.key_tree.itemClicked.connect(self.show_key_value)
        
        # 右侧：值展示
        self.value_tabs = QTabWidget()
        self.value_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        
        # 创建不同类型的展示页面
        self.create_value_tabs()
        
        self.data_splitter.addWidget(self.key_tree)
        self.data_splitter.addWidget(self.value_tabs)
        self.data_splitter.setSizes([300, 500])
        
        layout.addWidget(self.data_splitter)
    
    def create_value_tabs(self):
        """创建值展示标签页"""
        # 字符串值
        self.string_tab = QWidget()
        string_layout = QVBoxLayout(self.string_tab)
        self.string_text = QTextEdit()
        self.string_text.setFont(QFont("Consolas", 10))
        string_layout.addWidget(self.string_text)
        self.value_tabs.addTab(self.string_tab, "字符串")
        
        # 列表值
        self.list_tab = QWidget()
        list_layout = QVBoxLayout(self.list_tab)
        self.list_table = QTableWidget()
        self.list_table.setColumnCount(2)
        self.list_table.setHorizontalHeaderLabels(["索引", "值"])
        self.list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        list_layout.addWidget(self.list_table)
        self.value_tabs.addTab(self.list_tab, "列表")
        
        # 集合值
        self.set_tab = QWidget()
        set_layout = QVBoxLayout(self.set_tab)
        self.set_table = QTableWidget()
        self.set_table.setColumnCount(1)
        self.set_table.setHorizontalHeaderLabels(["值"])
        self.set_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        set_layout.addWidget(self.set_table)
        self.value_tabs.addTab(self.set_tab, "集合")
        
        # 有序集合值
        self.zset_tab = QWidget()
        zset_layout = QVBoxLayout(self.zset_tab)
        self.zset_table = QTableWidget()
        self.zset_table.setColumnCount(2)
        self.zset_table.setHorizontalHeaderLabels(["值", "分数"])
        self.zset_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        zset_layout.addWidget(self.zset_table)
        self.value_tabs.addTab(self.zset_tab, "有序集合")
        
        # 哈希值
        self.hash_tab = QWidget()
        hash_layout = QVBoxLayout(self.hash_tab)
        self.hash_table = QTableWidget()
        self.hash_table.setColumnCount(2)
        self.hash_table.setHorizontalHeaderLabels(["字段", "值"])
        self.hash_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        hash_layout.addWidget(self.hash_table)
        self.value_tabs.addTab(self.hash_tab, "哈希")
    
    def connect_redis(self):
        """连接Redis"""
        host = self.host_input.text()
        port = int(self.port_input.text())
        password = self.password_input.text() if self.password_input.text() else None
        db = self.db_input.value()
        cluster_mode = self.cluster_checkbox.isChecked()
        
        # 确保之前的线程已清理
        if self.connection_thread and self.connection_thread.isRunning():
            self.connection_thread.quit()
            self.connection_thread.wait()
        
        # 添加调试信息
        print(f"正在连接: host={host}, port={port}, cluster_mode={cluster_mode}")
        
        self.connection_thread = RedisConnectionThread(host, port, password, db, cluster_mode)
        self.connection_thread.connection_result.connect(self.on_connection_result)
        self.connection_thread.data_loaded.connect(self.on_data_loaded)
        self.connection_thread.start()
        
        self.status_label.setText("连接中...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #007bff;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #007bff;
                border-radius: 4px;
                background-color: #e6f3ff;
            }
        """)
    
    def disconnect_redis(self):
        """断开Redis连接"""
        try:
            # 安全地关闭Redis连接
            if self.redis_client:
                try:
                    self.redis_client.close()
                except:
                    pass  # 忽略关闭时的错误
                self.redis_client = None
            
            # 安全地停止线程
            if self.connection_thread and self.connection_thread.isRunning():
                self.connection_thread.quit()
                self.connection_thread.wait(1000)  # 等待最多1秒
            
            self.connection_thread = None
            
            # 清空UI
            self.key_tree.clear()
            self.status_label.setText("已断开")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #6c757d;
                    font-weight: bold;
                    padding: 5px;
                    border: 1px solid #6c757d;
                    border-radius: 4px;
                    background-color: #f8f9fa;
                }
            """)
            
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            
        except Exception as e:
            print(f"断开连接时出错: {e}")
            # 即使出错也确保UI状态正确
            self.redis_client = None
            self.connection_thread = None
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
    
    def on_connection_result(self, success, message):
        """连接结果处理"""
        if success:
            self.redis_client = self.connection_thread.redis_client
            self.status_label.setText("已连接")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    font-weight: bold;
                    padding: 5px;
                    border: 1px solid #28a745;
                    border-radius: 4px;
                    background-color: #d4edda;
                }
            """)
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.load_keys()
        else:
            self.status_label.setText(f"连接失败: {message}")
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #dc3545;
                    font-weight: bold;
                    padding: 5px;
                    border: 1px solid #dc3545;
                    border-radius: 4px;
                    background-color: #f8d7da;
                }
            """)
    
    def on_data_loaded(self, data):
        """数据加载完成"""
        self.key_tree.clear()
        for key, info in data.items():
            item = QTreeWidgetItem(self.key_tree)
            item.setText(0, key)
            item.setText(1, info['type'])
            item.setText(2, str(info['ttl']) if info['ttl'] > 0 else '永久')
            item.setData(0, Qt.UserRole, info['type'])
    
    def load_keys(self):
        """加载key列表"""
        if self.connection_thread and self.connection_thread.redis_client:
            pattern = self.search_input.text() or "*"
            self.connection_thread.load_keys(pattern)
    
    def show_key_value(self, item):
        """显示key的值"""
        if not item:
            return
            
        key = item.text(0)
        key_type = item.data(0, Qt.UserRole)
        
        try:
            if self.connection_thread and self.connection_thread.redis_client:
                value = self.connection_thread.get_value(key, key_type)
                self.display_value(key_type, value)
            else:
                self.show_message("警告", "请先连接到Redis", "warning")
        except Exception as e:
            self.show_message("错误", f"获取值失败: {str(e)}", "error")
    
    def display_value(self, key_type, value):
        """显示值"""
        if key_type == 'string':
            self.value_tabs.setCurrentWidget(self.string_tab)
            self.string_text.setPlainText(str(value))
        elif key_type == 'list':
            self.value_tabs.setCurrentWidget(self.list_tab)
            self.list_table.setRowCount(len(value))
            for i, val in enumerate(value):
                self.list_table.setItem(i, 0, QTableWidgetItem(str(i)))
                self.list_table.setItem(i, 1, QTableWidgetItem(str(val)))
        elif key_type == 'set':
            self.value_tabs.setCurrentWidget(self.set_tab)
            self.set_table.setRowCount(len(value))
            for i, val in enumerate(value):
                self.set_table.setItem(i, 0, QTableWidgetItem(str(val)))
        elif key_type == 'zset':
            self.value_tabs.setCurrentWidget(self.zset_tab)
            self.zset_table.setRowCount(len(value))
            for i, (val, score) in enumerate(value):
                self.zset_table.setItem(i, 0, QTableWidgetItem(str(val)))
                self.zset_table.setItem(i, 1, QTableWidgetItem(str(score)))
        elif key_type == 'hash':
            self.value_tabs.setCurrentWidget(self.hash_tab)
            self.hash_table.setRowCount(len(value))
            for i, (field, val) in enumerate(value.items()):
                self.hash_table.setItem(i, 0, QTableWidgetItem(str(field)))
                self.hash_table.setItem(i, 1, QTableWidgetItem(str(val)))
    
    def copy_key(self, key):
        """复制key到剪贴板"""
        if self.copy_to_clipboard(key):
            self.show_message("成功", f"Key已复制: {key}")
    
    def show_message(self, title, message, msg_type="info"):
        """显示消息"""
        if msg_type == "error":
            QMessageBox.critical(self.main_widget, title, message)
        elif msg_type == "warning":
            QMessageBox.warning(self.main_widget, title, message)
        else:
            QMessageBox.information(self.main_widget, title, message)
    
    def load_sessions(self):
        """加载保存的会话"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
                print(f"成功加载 {len(sessions)} 个会话")
            else:
                sessions = []
                print("会话文件不存在，创建空会话列表")
            
            self.session_combo.clear()
            self.session_combo.addItem("新建会话", None)
            
            for session in sessions:
                name = session.get('name', f"{session['host']}:{session['port']}")
                # 限制会话名称长度，避免下拉框显示问题
                if len(name) > 30:
                    display_name = name[:27] + "..."
                else:
                    display_name = name
                self.session_combo.addItem(display_name, session)
                print(f"添加会话: {name}")
                
            if sessions:
                # 自动选择第一个会话
                self.session_combo.setCurrentIndex(1)
                self.load_session_config(self.session_combo.currentText())
                
        except Exception as e:
            print(f"加载会话失败: {e}")
            self.session_combo.addItem("新建会话", None)
    
    def load_session_config(self, session_name):
        """加载会话配置"""
        if session_name == "新建会话" or session_name is None:
            return
            
        session_data = self.session_combo.currentData()
        if session_data:
            self.host_input.setText(session_data.get('host', 'localhost'))
            self.port_input.setText(str(session_data.get('port', 6379)))
            self.password_input.setText(session_data.get('password', ''))
            self.db_input.setValue(session_data.get('db', 0))
            self.cluster_checkbox.setChecked(session_data.get('cluster_mode', False))
    
    def save_current_session(self):
        """保存当前会话"""
        try:
            # 获取当前配置
            session_name = f"{self.host_input.text()}:{self.port_input.text()}"
            # 限制会话名称长度
            if len(session_name) > 30:
                session_name = session_name[:27] + "..."
                
            session_config = {
                'name': session_name,
                'host': self.host_input.text(),
                'port': int(self.port_input.text()),
                'password': self.password_input.text(),
                'db': self.db_input.value(),
                'cluster_mode': self.cluster_checkbox.isChecked(),
                'timestamp': str(int(__import__('time').time()))
            }
            
            # 加载现有会话
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
            else:
                sessions = []
            
            # 检查是否已存在相同配置
            existing_index = -1
            for i, session in enumerate(sessions):
                if (session['host'] == session_config['host'] and
                    session['port'] == session_config['port'] and
                    session['db'] == session_config['db'] and
                    session['cluster_mode'] == session_config['cluster_mode']):
                    existing_index = i
                    break
            
            if existing_index >= 0:
                # 更新现有会话
                sessions[existing_index] = session_config
            else:
                # 添加新会话
                sessions.append(session_config)
            
            # 保存会话
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)
            
            # 重新加载会话列表
            self.load_sessions()
            
            # 选择刚保存的会话
            index = self.session_combo.findText(session_config['name'])
            if index >= 0:
                self.session_combo.setCurrentIndex(index)
            
            self.show_message("成功", "会话已保存")
            
        except Exception as e:
            self.show_message("错误", f"保存会话失败: {str(e)}", "error")
    
    def delete_current_session(self):
        """删除当前会话"""
        try:
            current_text = self.session_combo.currentText()
            if current_text == "新建会话":
                self.show_message("警告", "无法删除新建会话", "warning")
                return
            
            session_data = self.session_combo.currentData()
            if not session_data:
                return
            
            # 确认删除
            reply = QMessageBox.question(
                self.main_widget,
                "确认删除",
                f"确定要删除会话 '{current_text}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # 加载现有会话
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    sessions = json.load(f)
            else:
                sessions = []
            
            # 删除匹配的会话
            sessions = [s for s in sessions if not (
                s['host'] == session_data['host'] and
                s['port'] == session_data['port'] and
                s['db'] == session_data['db'] and
                s['cluster_mode'] == session_data['cluster_mode']
            )]
            
            # 保存更新后的会话列表
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(sessions, f, ensure_ascii=False, indent=2)
            
            # 重新加载会话列表
            self.load_sessions()
            self.session_combo.setCurrentIndex(0)  # 选择"新建会话"
            
            self.show_message("成功", "会话已删除")
            
        except Exception as e:
            self.show_message("错误", f"删除会话失败: {str(e)}", "error")
    
    def test_connection(self):
        """测试连接"""
        try:
            import redis
            host = self.host_input.text()
            port = int(self.port_input.text())
            password = self.password_input.text() if self.password_input.text() else None
            cluster_mode = self.cluster_checkbox.isChecked()
            
            test_result = []
            
            if cluster_mode:
                # 测试集群连接
                try:
                    startup_nodes = [{"host": host, "port": port}]
                    rc = redis.cluster.RedisCluster(
                        startup_nodes=startup_nodes,
                        password=password,
                        decode_responses=True,
                        socket_connect_timeout=5,
                        socket_timeout=5
                    )
                    info = rc.info()
                    cluster_info = rc.cluster_info()
                    test_result.append("✅ 集群连接成功")
                    test_result.append(f"节点数: {len(info)}")
                    test_result.append(f"集群状态: {cluster_info.get('cluster_state', 'unknown')}")
                    rc.close()
                except Exception as e:
                    test_result.append(f"❌ 集群连接失败: {str(e)}")
                    
                # 测试单机模式（作为对比）
                try:
                    r = redis.Redis(host=host, port=port, password=password, decode_responses=True)
                    r.ping()
                    info = r.info()
                    test_result.append(f"✅ 单机模式可用: Redis {info.get('redis_version', 'unknown')}")
                    r.close()
                except Exception as e:
                    test_result.append(f"❌ 单机模式失败: {str(e)}")
            else:
                # 测试单机连接
                try:
                    r = redis.Redis(host=host, port=port, password=password, db=0, decode_responses=True)
                    r.ping()
                    info = r.info()
                    test_result.append(f"✅ 单机连接成功: Redis {info.get('redis_version', 'unknown')}")
                    test_result.append(f"模式: {info.get('redis_mode', 'unknown')}")
                    if info.get('redis_mode') == 'cluster':
                        test_result.append("💡 提示：这是集群节点，请使用集群模式连接")
                    r.close()
                except Exception as e:
                    test_result.append(f"❌ 单机连接失败: {str(e)}")
            
            # 显示测试结果
            result_text = "\n".join(test_result)
            QMessageBox.information(self.main_widget, "连接测试结果", result_text)
            
        except Exception as e:
            QMessageBox.critical(self.main_widget, "测试错误", f"测试失败: {str(e)}")
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.redis_client:
                try:
                    self.redis_client.close()
                except:
                    pass
            
            if self.connection_thread and self.connection_thread.isRunning():
                self.connection_thread.quit()
                self.connection_thread.wait(1000)
                
        except Exception as e:
            print(f"清理资源时出错: {e}")