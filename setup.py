from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {"packages": ["pygame", "stockfish"], "include_files": ['resources/', 'stockfish/']}

base = 'console'

executables = [
    Executable('Main.py', base=base, target_name = 'ChessAI')
]

setup(name='ChessVSAI',
      version = '0.1.0',
      description = 'A chess app to play against stockfish AI',
      options = {'build_exe': build_options},
      executables = executables)
