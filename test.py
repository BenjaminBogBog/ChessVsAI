from stockfish import Stockfish

stockfish = Stockfish('D:\\Game Development\\pygame\\Chess\\stockfish\\stockfish-windows-x86-64-avx2.exe')

print(stockfish.get_fen_position())

print(stockfish.make_moves_from_current_position(["e2e4"]))

print(stockfish.get_fen_position())

