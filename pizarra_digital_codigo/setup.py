import sys
from cx_Freeze import setup, Executable

# Reemplaza 'tu_script.py' con el nombre de tu script
script = 'pizarra_digidedos.py'

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable(script, base=base,
    icon="pizarra.ico")]

setup(
    name='Pizarra Digital',
    version='1.0',
    description='Aplicacion para dibujar con las yemas de los dedos y movimiento, hecho por josue osores arancel',
    options={'build_exe': {}},
    executables=executables
)
