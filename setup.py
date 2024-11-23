import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('Main.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "Chess vs AI",
    options = {"build_exe" : 
        {"packages" : ["pygame"]}},
    executables = executables
)