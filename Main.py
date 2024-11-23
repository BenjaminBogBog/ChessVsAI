# importing required library
import pygame
from stockfish import Stockfish
 
# ACTIVE THE LIBRARY ----------------------------------------------------------
pygame.init()
screen_size = (800, 800)
screen_X = screen_size[0]
screen_Y = screen_size[1]

pygame.font.init()

pieces_layout_ref = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

text_x = ["a", "b", "c", "d", "e", "f", "g", "h"]
text_y = ["1", "2", "3", "4", "5", "6", "7", "8"]

grid_increment = (screen_size[0] / 8, screen_size[1] / 8)

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((screen_X, screen_Y))

piecesOnBoard = []

pieceMovesShown = None
availableSlots = []
availableAttacks = []

whiteKingIsInCheck = False
blackKingIsInCheck = False

colorInTurn = "w"

stockfish = Stockfish('D:\\Game Development\\pygame\\Chess\\stockfish\\stockfish-windows-x86-64-avx2.exe')

def get_chess_position_by_grid(x, y):
    # reverse y
    return text_x[x] + text_y[(len(text_y) - 1) - y]

# PIECE CLASS ---------------------------------------------------

class Piece:
    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.image = None
        self.piece_rect = None
        self.should_render = True
        self.pawnMoved = False


        if(color == "black"):
            self.forward = 1
        else:
            self.forward = -1

        if(color == "black"):
            self.drawPieceBlack()
        else:
            self.drawPieceWhite()
    
    def drawPieceWhite(self):
        self.image = w_pawn

        if self.name == "rook":
            self.image = w_rook
        elif self.name == "knight":
            self.image = w_knight
        elif self.name == "bishop":
            self.image = w_bishop
        elif self.name == "queen":
            self.image = w_queen
        elif self.name == "king":
            self.image = w_king

        self.image = pygame.transform.scale(self.image, (70, 70))
        self.piece_rect = self.image.get_rect(center=(self.x, self.y))

    def drawPieceBlack(self):
        self.image = b_pawn

        if self.name == "rook":
            self.image = b_rook
        elif self.name == "knight":
            self.image = b_knight
        elif self.name == "bishop":
            self.image = b_bishop
        elif self.name == "queen":
            self.image = b_queen
        elif self.name == "king":
            self.image = b_king

        self.image = pygame.transform.scale(self.image, (70, 70))
        self.piece_rect = self.image.get_rect(center=(self.x, self.y))
    
    
    def movePiece(self, x, y):
        
        previousGridPos = get_grid_by_mouse_position((self.x, self.y))
        newGridPos = get_grid_by_mouse_position((x, y))
        
        print("Moving piece from " + str(previousGridPos) + " to " + str(newGridPos))

        chessMoveStr = get_chess_position_by_grid(previousGridPos[0], previousGridPos[1]) + get_chess_position_by_grid(newGridPos[0], newGridPos[1])

        print("Playing move: " + str(chessMoveStr))

        stockfish.make_moves_from_current_position([chessMoveStr])

        self.x = x
        self.y = y
        self.piece_rect = self.image.get_rect(center=(self.x, self.y))
        
        drawBoard()
        drawPositions()

# ---------------------------------------------------

# GET PIECE AT GRID POSITION ---------------------------------------------------
def getPieceAtGridPosition(x, y):
    for piece in piecesOnBoard:
        if piece.x == get_centered_position(x, y)[0] and piece.y == get_centered_position(x, y)[1]:
            return piece

    return None

def getPositionByGrid(x, y):
    return (pos_grid_x[x], pos_grid_y[y])

# ---------------------------------------------------

# SETTING VARIABLES ---------------------------------------------------

pos_grid_x = []
pos_grid_y = []

for i in range(8):
    pos_grid_x.append((grid_increment[0] * i))
    pos_grid_y.append((grid_increment[1] * i))

# Helper Functions
def get_grid_position(x, y):
    return (pos_grid_x[x], pos_grid_y[y])

def get_centered_position(x, y):
    return (pos_grid_x[x] + grid_increment[0] / 2, pos_grid_y[y] + grid_increment[1] / 2)

def get_grid_by_mouse_position(mouse_position):
    x = 0
    y = 0

    for i in range(8):
        if mouse_position[0] >= pos_grid_x[i] and mouse_position[0] <= pos_grid_x[i] + grid_increment[0]:
            x = i
            break

    for i in range(8):
        if mouse_position[1] >= pos_grid_y[i] and mouse_position[1] <= pos_grid_y[i] + grid_increment[1]:
            y = i
            break

    return (x, y)

# ---------------------------------------------------
 
def drawBoard():
    # SETTING BACKGROUND IMAGE ---------------------------------------------------
    
    # set the pygame window name
    pygame.display.set_caption('image')
    
    # create a surface object, image is drawn on it.
    background = pygame.image.load("resources\\chessboardBG.png").convert()
    background = pygame.transform.scale(background, (screen_X, screen_Y))

    # center the image
    background_rect = background.get_rect(center=(screen_X // 2, screen_Y // 2))
    
    # Using blit to copy content from one surface to other
    scrn.blit(background, background_rect)

    # paint screen one time
    pygame.display.flip()

    #---------------------------------------------------

    # SETTING TEXT ON CHESSBOARD ---------------------------------------------------

    monsterrat = pygame.font.SysFont("Arial", 24)

    text_position = []

    # render text
    for i in range(8):
        text = monsterrat.render(text_x[i], True, (0, 0, 0))
        text_rect = text.get_rect(center=(get_grid_position(i, 0)[0] + 12, get_grid_position(i, 0)[1] + 12))
        scrn.blit(text, text_rect)

    for i in range(8):
        text = monsterrat.render(text_y[i], True, (0, 0, 0))
        text_rect = text.get_rect(center=(get_grid_position(7, i)[0] + grid_increment[0] - 10, get_grid_position(7, i)[1] + grid_increment[1] - 15))
        scrn.blit(text, text_rect)

    # ---------------------------------------------------

def drawPositions():
    current_fen = stockfish.get_fen_position()

    print(current_fen)

    fen_separated = current_fen.split(" ")

    fen_position = fen_separated[0]

    colorInTurn = fen_separated[1]

    fen_position_lines = fen_position.split("/")

    if(colorInTurn == "b"):
        # AI TURN
        # get best move
        best_move = stockfish.get_best_move()
        print("AI Best move: " + str(best_move))
        stockfish.make_moves_from_current_position([best_move])
        drawBoard()
        drawPositions()
        return

    piecesOnBoard.clear()

    # #iterate over the fen string
    for i in range(len(fen_position_lines)):

        position_index = 0

        for j in range(len(fen_position_lines[i])):

            if fen_position_lines[i][j].isdigit():
                position_index += int(fen_position_lines[i][j])
                continue

            # if the character is a piece
            if fen_position_lines[i][j] == "p":
                piecesOnBoard.append(Piece("pawn", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "r":
                piecesOnBoard.append(Piece("rook", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "n":
                piecesOnBoard.append(Piece("knight", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "b":
                piecesOnBoard.append(Piece("bishop", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "q":
                piecesOnBoard.append(Piece("queen", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "k":
                piecesOnBoard.append(Piece("king", "black", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "P":
                piecesOnBoard.append(Piece("pawn", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "R":
                piecesOnBoard.append(Piece("rook", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "N":
                piecesOnBoard.append(Piece("knight", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "B":
                piecesOnBoard.append(Piece("bishop", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "Q":
                piecesOnBoard.append(Piece("queen", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))
            elif fen_position_lines[i][j] == "K":
                piecesOnBoard.append(Piece("king", "white", get_centered_position(position_index, i)[0], get_centered_position(position_index, i)[1]))

            position_index += 1
                
    # Draw pieces on board
    for piece in piecesOnBoard:
        if piece.should_render:
            scrn.blit(piece.image, piece.piece_rect)


# PLACE PIECES ON BOARD ---------------------------------------------------

# Black pieces
b_pawn = pygame.image.load("resources\\pieces\\b_pawn_png_shadow_256px.png").convert_alpha()
b_rook = pygame.image.load("resources\\pieces\\b_rook_png_shadow_256px.png").convert_alpha()
b_knight = pygame.image.load("resources\\pieces\\b_knight_png_shadow_256px.png").convert_alpha()
b_bishop = pygame.image.load("resources\\pieces\\b_bishop_png_shadow_256px.png").convert_alpha()
b_queen = pygame.image.load("resources\\pieces\\b_queen_png_shadow_256px.png").convert_alpha()
b_king = pygame.image.load("resources\\pieces\\b_king_png_shadow_256px.png").convert_alpha()

w_pawn = pygame.image.load("resources\\pieces\\w_pawn_png_shadow_256px.png").convert_alpha()
w_rook = pygame.image.load("resources\\pieces\\w_rook_png_shadow_256px.png").convert_alpha()
w_knight = pygame.image.load("resources\\pieces\\w_knight_png_shadow_256px.png").convert_alpha()
w_bishop = pygame.image.load("resources\\pieces\\w_bishop_png_shadow_256px.png").convert_alpha()
w_queen = pygame.image.load("resources\\pieces\\w_queen_png_shadow_256px.png").convert_alpha()
w_king = pygame.image.load("resources\\pieces\\w_king_png_shadow_256px.png").convert_alpha()

# # place black pawns
# for i in range(8):
#     piecesOnBoard.append(Piece("pawn", "black", get_centered_position(i, 1)[0], get_centered_position(i, 1)[1]))

# # place black pieces
# for i in range(8):
#     piecesOnBoard.append(Piece(pieces_layout_ref[i], "black", get_centered_position(i, 0)[0], get_centered_position(i, 0)[1]))

# # place white pawns
# for i in range(8):
#     piecesOnBoard.append(Piece("pawn", "white", get_centered_position(i, 6)[0], get_centered_position(i, 6)[1]))

# # place white pieces
# for i in range(8):
#     piecesOnBoard.append(Piece(pieces_layout_ref[i], "white", get_centered_position(i, 7)[0], get_centered_position(i, 7)[1]))
    
# ---------------------------------------------------

# DRAW BOARD ---------------------------------------------------
drawBoard()
drawPositions()
# ---------------------------------------------------

status = True

holding_mouse = False
holding_piece = None

while (status):
 
  # iterate over the list of Event objects
  # that was returned by pygame.event.get() method.
    for i in pygame.event.get():
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if i.type == pygame.QUIT:
            status = False

        # check mouse click
        if i.type == pygame.MOUSEBUTTONDOWN:
            interacted_grid = get_grid_by_mouse_position(i.pos)
            print(interacted_grid)
            recentlyMoved = False
            holding_mouse = True
            holding_piece = getPieceAtGridPosition(interacted_grid[0], interacted_grid[1])

        if i.type == pygame.MOUSEBUTTONUP:
            print("release mouse")
            holding_mouse = False
            interacted_grid = get_grid_by_mouse_position(i.pos)
            if(holding_piece != None):
                holding_piece.movePiece(get_centered_position(interacted_grid[0], interacted_grid[1])[0], get_centered_position(interacted_grid[0], interacted_grid[1])[1])
            
    
    if holding_mouse and holding_piece != None:
        # draw circle on starting position
        pygame.draw.circle(scrn, (255, 0, 0), (holding_piece.x, holding_piece.y), 35, 5)

    pygame.display.update()


 
# deactivates the pygame library
pygame.quit()