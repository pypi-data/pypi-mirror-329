import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

bdist_dmg_options = {'volume_label': 'K'}

setup(
    name="wiflip",
    version="0.1",
    description="My wiflip application!",
    options={"build_exe": build_exe_options, 'bdist_dmg': bdist_dmg_options},
    executables=[Executable("bibou2.py", base=base)],
)