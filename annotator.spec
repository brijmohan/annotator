# -*- mode: python -*-

block_cipher = None


a = Analysis(['annotator.py'],
             pathex=['/media/brij/SAARTHI/IIIT/SpeechLab/Projects/medical_data_tagging/annotation_tool'],
             binaries=None,
             datas=None,
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
          name='annotator',
          debug=False,
          strip=False,
          upx=True,
          console=True )
