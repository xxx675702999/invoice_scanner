# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import os

# ==================== 用户配置区域 ====================
MAIN_SCRIPT = 'mian_V5.py'  # 主程序入口
APP_NAME = '苏苏专用发票识别系统'         # 生成的可执行文件名称
ICON_FILE = 'app.ico'                 # 程序图标（可选）
# =====================================================

block_cipher = None

# 自动收集依赖项
ocr_data = collect_data_files('paddleocr')
paddle_libs = collect_dynamic_libs('paddle')

a = Analysis(
    [MAIN_SCRIPT],
    pathex=[],
    binaries=[
        # CPU版本不需要CUDA相关配置
        *paddle_libs
    ],
    datas=[
        # 包含OCR字典文件
        *collect_data_files('paddleocr.ppocr.utils', include_py_files=False),

        # 包含Windows运行时组件
        (r'C:\Windows\System32\vcomp140.dll', '.'),  # OpenMP
        (r'C:\Windows\System32\msvcp140.dll', '.'),  # MSVC运行时
    ],
    hiddenimports=[
       # *collect_submodules('pathlib'),
        'pathlib',
        'pkg_resources.py2_warn',
        'paddle.nn.functional.tensor',
        'rapidfuzz.process_cpp_impl',
        'pdf2image._poppler',
        'numpy',  # 显式声明numpy依赖
        'paddle.libs.mklml'  # CPU加速库
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'test',
        'tests',
        'cuda',  # 排除CUDA相关模块
        'nvidia'  # 排除NVIDIA相关模块
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=ICON_FILE
)