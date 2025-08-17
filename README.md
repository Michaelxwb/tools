# 开发者工具集

一个集成多种开发常用工具的桌面应用程序，提供简洁直观的图形界面。

## 功能特性

### 🛠️ 集成工具
- ✅ **JSON格式化工具**: JSON美化、压缩、验证等功能
- ✅ **时间戳转换工具**: Unix时间戳与可读时间相互转换
- ✅ **可扩展架构**: 支持快速接入新工具

### 📝 JSON格式化工具
- JSON格式化：将压缩的JSON转换为易读的格式
- JSON压缩：移除多余空格和换行，压缩JSON大小
- JSON验证：检查JSON格式是否正确
- 文件操作：支持打开和保存JSON文件
- 智能解析：支持JSON和Python字典格式

### ⏰ 时间戳转换工具
- 实时显示当前Unix时间戳
- Unix时间戳转可读时间格式
- 可读时间转Unix时间戳
- 支持秒和毫秒单位
- 多种时间格式支持
- 一键复制功能

### 🎨 界面特性
- 现代化设计风格
- 中文界面支持
- 工具间快速切换
- 可拖拽分割窗口
- 详细错误提示

## 使用方法

### 方法一：直接运行
1. 双击 `JSON格式化工具.exe` 直接运行

### 方法二：安装到桌面
1. 双击 `install.bat` 运行安装脚本
2. 程序将安装到桌面的"JSON格式化工具"文件夹中

## 界面说明

### 主要功能按钮
- **格式化**: 将JSON转换为易读的格式（带缩进和换行）
- **压缩**: 移除多余空格，压缩JSON大小
- **验证**: 检查JSON格式是否正确
- **清空**: 清空输入和输出区域
- **打开文件**: 从文件中加载JSON内容
- **保存文件**: 将格式化结果保存到文件

### 使用步骤
1. 在"输入JSON"区域粘贴或输入JSON内容
2. 点击相应的功能按钮（格式化/压缩/验证）
3. 在"格式化结果"区域查看处理结果
4. 可选择保存结果到文件

## 开发信息

### 技术栈
- Python 3.x
- tkinter (GUI框架)
- json (JSON处理)
- PyInstaller (打包工具)

### 源码结构
```
├── toolkit_main.py                # 主程序入口
├── tools/                         # 工具模块目录
│   ├── __init__.py               # 包初始化文件
│   ├── base_tool.py              # 工具基类
│   ├── json_formatter_tool.py    # JSON格式化工具
│   └── timestamp_converter_tool.py # 时间戳转换工具
├── fix_icon_build.py              # 构建脚本
├── convert_icon.py                # 图标转换工具
├── install_pyinstaller.py         # PyInstaller安装脚本
├── 一键构建带图标exe.bat           # 一键构建批处理
├── 安装PyInstaller.bat            # 安装工具批处理
├── 清理图标缓存.bat               # 图标缓存清理工具
├── requirements.txt               # 依赖包列表
├── README.md                     # 说明文档
├── demo.json                     # 示例JSON文件
└── icon.png                      # 程序图标
```

### 自行构建

#### 快速构建（推荐）
1. 双击运行 `安装PyInstaller.bat` 安装构建工具
2. 双击运行 `一键构建带图标exe.bat` 开始构建
3. 构建完成后，exe文件位于 `dist/` 目录中（开发者工具集.exe）

#### 图标支持
- 将PNG格式的图标文件命名为 `icon.png` 放在项目根目录
- 构建时会自动转换为ICO格式并嵌入exe文件
- 支持透明背景和多种尺寸（16x16到256x256）
- **窗口图标**：程序运行时窗口标题栏也会显示自定义图标

#### 手动构建
```bash
# 安装构建工具
pip install pyinstaller

# 构建exe文件
python fix_icon_build.py
```

#### 开发运行
```bash
# 直接运行主程序
python toolkit_main.py
```

#### 常见问题
- **网络超时**：使用批处理文件会自动尝试多个镜像源
- **文件图标不显示**：运行 `清理图标缓存.bat` 清理系统缓存
- **窗口图标不显示**：运行 `测试并重新构建.bat` 重新构建程序
- **权限问题**：以管理员身份运行

#### 图标测试
- 运行 `python 测试窗口图标.py` 测试图标设置功能
- 运行 `测试并重新构建.bat` 完整测试和重新构建流程

## 🔧 工具扩展

### 添加新工具
1. 在 `tools/` 目录下创建新的工具文件
2. 继承 `BaseTool` 基类
3. 实现 `setup_ui()` 方法
4. 在 `toolkit_main.py` 中注册新工具

### 工具开发示例
```python
from .base_tool import BaseTool
import tkinter as tk
from tkinter import ttk

class MyTool(BaseTool):
    def setup_ui(self):
        self.main_frame = ttk.Frame(self.parent_frame, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加你的UI组件
        ttk.Label(self.main_frame, text="我的工具").pack()
```

### 工具特性
- 统一的界面风格
- 内置剪贴板操作
- 标准化消息提示
- 自动布局管理
- 工具间独立运行

## 系统要求

- Windows 7/8/10/11
- 无需安装Python环境（exe版本）

## 许可证

MIT License

## 更新日志

### v1.0.0 - 工具集重构版
- 🔄 重构为工具集架构，支持多工具集成
- ✅ JSON格式化工具：完整迁移原有功能
- 🆕 时间戳转换工具：Unix时间戳与时间格式互转
- 🎨 现代化界面设计，工具间快速切换
- 🔧 可扩展架构，支持快速添加新工具
- 📦 统一构建和打包流程

### v0.9.0 - JSON格式化工具
- 初始版本发布
- 支持JSON格式化、压缩、验证功能
- 支持文件读写操作
- 提供Windows安装包