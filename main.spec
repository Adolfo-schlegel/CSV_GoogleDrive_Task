# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['D:/Proyectos/GoogleDriveClientPython/main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Proyectos/GoogleDriveClientPython/AuthGD.py', '.'), ('D:/Proyectos/GoogleDriveClientPython/bitcoin.csv', '.'), ('D:/Proyectos/GoogleDriveClientPython/bitcoin_history.csv', '.'), ('D:/Proyectos/GoogleDriveClientPython/client_secret_1059549673501-41b5ad42bvc382nd783br7omu004qtts.apps.googleusercontent.com.json', '.'), ('D:/Proyectos/GoogleDriveClientPython/GenerateCSV.py', '.'), ('D:/Proyectos/GoogleDriveClientPython/GoogleDriveClientPython.py', '.'), ('D:/Proyectos/GoogleDriveClientPython/main.py', '.'), ('D:/Proyectos/GoogleDriveClientPython/main.spec', '.'), ('D:/Proyectos/GoogleDriveClientPython/parameters.json', '.'), ('D:/Proyectos/GoogleDriveClientPython/requirements.txt', '.'), ('D:/Proyectos/GoogleDriveClientPython/textpad.png', '.'), ('D:/Proyectos/GoogleDriveClientPython/token.json', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Adolf\\Downloads\\programacion-web.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
