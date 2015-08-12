import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "matplotlib", "numpy", "pylab"], "excludes": ["tkinter"],
                     "include_files": ["Icons/"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "SAIGViewer",
        version = "0.1",
        description = "Plotter and Viewer for SAIG at the University of Alberta!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("SAIGViewer.py", base=base, icon='Icons/SAIG.ico')])