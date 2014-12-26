# -*- mode: python -*-
a = Analysis(['/Users/Brian/Desktop/Brian-Craft/prototype_1.py', ' --clean'],
             pathex=['/Users/Brian/Desktop/Brian-Craft'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='prototype_1',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='prototype_1')
app = BUNDLE(coll,
             name='prototype_1.app',
             icon=None)
