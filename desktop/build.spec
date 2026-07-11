# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 打包规范文件
=========================
生成类似微信的独立桌面应用 exe（无控制台、独立窗口、任务栏图标）。

使用方式：
    cd desktop
    pyinstaller build.spec

输出：dist/学生会人事管理系统.exe（单文件，双击即可运行）
"""
import os

block_cipher = None

# 路径定义
# SPECPATH 是 PyInstaller 注入的全局变量，指向 spec 文件所在目录
try:
    SPEC_DIR = SPECPATH
except NameError:
    SPEC_DIR = os.getcwd()
ROOT_DIR = os.path.dirname(SPEC_DIR)                  # 项目根目录

# 需要打包进去的资源文件：(源路径, 目标目录)
datas = [
    # 前端页面（QWebEngineView 通过 HTTP 从内嵌 Flask 加载）
    (os.path.join(ROOT_DIR, 'index.html'), '.'),
    # 应用图标（托盘 + 任务栏）
    (os.path.join(ROOT_DIR, 'school-logo.png'), '.'),
    # Flask 后端源码（桌面端通过 importlib 内嵌加载）
    (os.path.join(ROOT_DIR, 'main.py'), '.'),
    # PWA 配置
    (os.path.join(ROOT_DIR, 'manifest.json'), '.'),
]

# 隐式导入（PyInstaller 无法自动检测的模块）
hiddenimports = [
    'flask',
    'flask.json',
    'jinja2',
    'markupsafe',
    'itsdangerous',
    'click',
    'werkzeug',
    # PySide6 子模块
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'PySide6.QtWebEngineWidgets',
    'PySide6.QtWebEngineCore',
    'PySide6.QtNetwork',
    # 第三方
    'win11toast',
    'PIL',
    'PIL.PngImagePlugin',
    # 桌面端模块
    'config',
    'network',
    'notifier',
    'bridge',
    'tray',
]

a = Analysis(
    ['main.py'],
    pathex=[SPEC_DIR, ROOT_DIR],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',       # 不需要 Tkinter
        'unittest',
        'pydoc',
        'test',
    ],
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
    name='学生会人事管理系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                    # 压缩，减小体积
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,                # ★ 关键：无控制台窗口，类似微信的纯 GUI 应用
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(ROOT_DIR, 'school-logo.png'),  # 任务栏/窗口图标
)
