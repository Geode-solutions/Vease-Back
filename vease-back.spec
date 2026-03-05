# -*- mode: python ; coding: utf-8 -*-
# pyinstaller --onefile --collect-data opengeodeweb_back --collect-data vease_back --recursive-copy-metadata vease_back src/vease_back/app.py -n vease-back
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = []
datas += collect_data_files('opengeodeweb_back')
datas += collect_data_files('vease_back')
datas += copy_metadata('vease_back', recursive=True)


a = Analysis(
    ['src/vease_back/app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='vease-back',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
