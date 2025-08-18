# -*- mode: python ; coding: utf-8 -*-
# 开发者工具集构建配置

block_cipher = None

a = Analysis(
    ['toolkit_main.py'],
    pathex=['D:/workspace/tools'],
    binaries=[],
    datas=[("icon.ico", "."), ("icon.png", ".")],
    hiddenimports=['PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui', 'tools.json_formatter_tool', 'tools.timestamp_converter_tool', 'tools.base_tool'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='开发者工具集',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='D:/workspace/tools/icon.ico',
)
