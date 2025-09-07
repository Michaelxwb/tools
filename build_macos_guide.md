# macOS 构建 Windows EXE 指南

## 🚨 当前状态
Wine 在 macOS 上存在兼容性问题，特别是 Apple Silicon 芯片。

## ✅ 推荐方案

### 方案1：使用虚拟机（推荐）
```bash
# 安装Parallels Desktop或VirtualBox
# 在Windows虚拟机中运行：
python build_exe.py
```

### 方案2：使用GitHub Actions（云构建）
创建 `.github/workflows/build.yml`：
```yaml
name: Build Windows EXE
on: [push]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    - name: Build EXE
      run: python build_exe.py
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: DeveloperToolkit-windows
        path: dist/DeveloperToolkit.exe
```

### 方案3：使用在线构建服务
- **PyInstaller在线**: 使用Windows云服务器
- **GitHub Actions**: 免费Windows构建环境

### 方案4：双系统/Windows机器
直接在Windows系统上运行：
```bash
python build_exe.py
```

## 🛠️ 手动Wine安装（高级用户）

### Apple Silicon (M1/M2) 特殊说明
```bash
# 使用Rosetta 2
softwareupdate --install-rosetta

# 安装CrossOver（付费但稳定）
brew install --cask crossover

# 或使用UTM虚拟机
brew install --cask utm
```

### Intel Mac
```bash
# 标准Wine安装
brew install --cask wine-stable

# 然后运行（可能需要多次尝试）
wine python -m pip install pyinstaller
wine python -m PyInstaller --onefile --windowed toolkit_main.py
```

## 📁 预期输出
成功构建后，文件位置：
- **本地Windows**: `./dist/DeveloperToolkit.exe`
- **GitHub Actions**: 下载artifacts中的EXE文件
- **虚拟机**: 共享文件夹中的EXE文件

## 🎯 最简单方案
**推荐使用GitHub Actions** - 免费、可靠、跨平台兼容