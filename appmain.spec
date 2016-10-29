# -*- mode: python -*-

block_cipher = None

a = Analysis(['./src/appmain.py'],
             pathex=['./src/'],
             binaries=None,
             datas=[('./src/logging.conf','.'),],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CardBordAI_Demo_ver010',
          debug=False,
          strip=False,
          upx=False,
          icon='./src/icon.ico',
          console=False )