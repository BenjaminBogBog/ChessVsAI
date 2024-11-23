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

grid_increment = (screen_size[0] / 8, screen_size[1] / 8)

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((screen_X, screen_Y))

piecesOnBoard = []

pieceMovesShown = None
availableSlots = []
availableAttacks = []

colorInTurn = "white"

whiteKingIsInCheck = False
blackKingIsInCheck = False

stockfish = Stockfish('D:\\Game Development\\pygame\\Chess\\stockfish\\stockfish-windows-x86-64-avx2.exe')

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
        self.canEnpassant = False
        self.pinned = False

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

    def showAvailableMoves(self):
        drawBoard()
        available_moves = self.getAvailableMoves()
        available_attacks = self.getAttackingMoves()

        for move in available_moves:
            pygame.draw.circle(scrn, (0, 0, 255), (self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward), 10)

        for move in available_attacks:
            pygame.draw.circle(scrn, (255, 0, 0), (self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward), 10)

    def getAttackingMoves(self, ignoreKing = False):
        availableMoves = []

        if self.name == "pawn":
            if(self.checkIfAttackIsValid(1, 1, ignoreKing) == True):
                availableMoves.append((1, 1))

            if(self.checkIfAttackIsValid(-1, 1, ignoreKing) == True):
                availableMoves.append((-1, 1))

            # check if enpassant is possible
            if(self.canEnpassant == True):
                # check if the piece is at the right position
                rightPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[1])
                leftPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[1])

                if(rightPiece != None and rightPiece.name == "pawn" and rightPiece.color != self.color):
                    # check move valid
                    if(self.color == "black"):
                        if(self.checkIfMoveIsValid(1, 1) != False):
                            availableMoves.append((1, 1))

                    if(self.color == "white"):
                        if(self.checkIfMoveIsValid(-1, 1) != False):
                            availableMoves.append((-1, 1))

                if(leftPiece != None and leftPiece.name == "pawn" and leftPiece.color != self.color):
                    # check move valid
                    if(self.color == "black"):
                        if(self.checkIfMoveIsValid(-1, 1) != False):
                            availableMoves.append((-1, 1))

                    if(self.color == "white"):
                        if(self.checkIfMoveIsValid(1, 1) != False):
                            availableMoves.append((1, 1))

        elif self.name == "rook":
            for i in range(9):
                if i != 0:
                    # check if the move is valid
                    if(self.checkBlock(0, i) == True):
                        break

                    if self.checkIfAttackIsValid(0, i, ignoreKing) == True:
                        availableMoves.append((0, i))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(0, -i) == True):
                        break

                    if self.checkIfAttackIsValid(0, -i, ignoreKing) == True:
                        availableMoves.append((0, -i))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(i, 0) == True):
                        break

                    if self.checkIfAttackIsValid(i, 0, ignoreKing) == True:
                        availableMoves.append((i, 0))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(-i, 0) == True):
                        break

                    if self.checkIfAttackIsValid(-i, 0, ignoreKing) == True:
                        availableMoves.append((-i, 0))
                        break

        elif self.name == "knight":
                
                if(self.checkIfAttackIsValid(2, 1, ignoreKing) == True):
                    availableMoves.append((2, 1))
    
                if(self.checkIfAttackIsValid(2, -1, ignoreKing) == True):
                    availableMoves.append((2, -1))
    
                if(self.checkIfAttackIsValid(-2, 1, ignoreKing) == True):
                    availableMoves.append((-2, 1))
    
                if(self.checkIfAttackIsValid(-2, -1, ignoreKing) == True):
                    availableMoves.append((-2, -1))
    
                if(self.checkIfAttackIsValid(1, 2, ignoreKing) == True):
                    availableMoves.append((1, 2))
    
                if(self.checkIfAttackIsValid(1, -2, ignoreKing) == True):
                    availableMoves.append((1, -2))
    
                if(self.checkIfAttackIsValid(-1, 2, ignoreKing) == True):
                    availableMoves.append((-1, 2))
    
                if(self.checkIfAttackIsValid(-1, -2, ignoreKing) == True):
                    availableMoves.append((-1, -2))

        elif self.name == "bishop":

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(i, i) == True):
                        break

                    if self.checkIfAttackIsValid(i, i, ignoreKing) == True:
                        availableMoves.append((i, i))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(i, -i) == True):
                        break

                    if self.checkIfAttackIsValid(i, -i, ignoreKing) == True:
                        availableMoves.append((i, -i))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(-i, i) == True):
                        break

                    if self.checkIfAttackIsValid(-i, i, ignoreKing) == True:
                        availableMoves.append((-i, i))
                        break

            for i in range(8): 
                if i != 0:
                    if(self.checkBlock(-i, -i) == True):
                        break

                    if self.checkIfAttackIsValid(-i, -i, ignoreKing) == True:
                        availableMoves.append((-i, -i))
                        break

        elif self.name == "queen":

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(0, i) == True):
                        break

                    if self.checkIfAttackIsValid(0, i, ignoreKing) == True:
                        availableMoves.append((0, i))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(0, -i) == True):
                        break

                    if self.checkIfAttackIsValid(0, -i, ignoreKing) == True:
                        availableMoves.append((0, -i))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(i, 0) == True):
                        break

                    if self.checkIfAttackIsValid(i, 0, ignoreKing) == True:
                        availableMoves.append((i, 0))
                        break

            for i in range(9):
                if i != 0:
                    if(self.checkBlock(-i, 0) == True):
                        break

                    if self.checkIfAttackIsValid(-i, 0, ignoreKing) == True:
                        availableMoves.append((-i, 0))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(i, i) == True):
                        break

                    if self.checkIfAttackIsValid(i, i, ignoreKing) == True:
                        availableMoves.append((i, i))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(i, -i) == True):
                        break

                    if self.checkIfAttackIsValid(i, -i, ignoreKing) == True:
                        availableMoves.append((i, -i))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(-i, i) == True):
                        break

                    if self.checkIfAttackIsValid(-i, i, ignoreKing) == True:
                        availableMoves.append((-i, i))
                        break

            for i in range(8):
                if i != 0:
                    if(self.checkBlock(-i, -i) == True):
                        break

                    if self.checkIfAttackIsValid(-i, -i, ignoreKing) == True:
                        availableMoves.append((-i, -i))
                        break

        elif self.name == "king":
            if(self.checkIfAttackIsValid(0, 1) == True):
                availableMoves.append((0, 1))

            if(self.checkIfAttackIsValid(0, -1) == True):
                availableMoves.append((0, -1))

            if(self.checkIfAttackIsValid(1, 0) == True):
                availableMoves.append((1, 0))

            if(self.checkIfAttackIsValid(-1, 0) == True):
                availableMoves.append((-1, 0))

            if(self.checkIfAttackIsValid(1, 1) == True):
                availableMoves.append((1, 1))

            if(self.checkIfAttackIsValid(1, -1) == True):
                availableMoves.append((1, -1))

            if(self.checkIfAttackIsValid(-1, 1) == True):
                availableMoves.append((-1, 1))

            if(self.checkIfAttackIsValid(-1, -1) == True):
                availableMoves.append((-1, -1))
                    

        for move in availableMoves:
            # check if the move is valid
            position = (get_grid_by_mouse_position((self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward)))
            availableSlots.append(position)

        return availableMoves
        

    def getAvailableMoves(self):

        # add all available moves then check if they are valid
        availableMoves = []

        if self.name == "pawn":
            if self.pawnMoved == False:
                if(self.checkIfMoveIsValid(0, 2 ) == True):
                    availableMoves.append((0, 2))

            if(self.checkIfMoveIsValid(0, 1) == True):
                availableMoves.append((0, 1))

        elif self.name == "rook":
            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(0, i) == False:
                        break
                    availableMoves.append((0, i))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(0, -i) == False:
                        break
                    availableMoves.append((0, -i))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(i, 0) == False:
                        break
                    availableMoves.append((i, 0))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(-i, 0) == False:
                        break
                    availableMoves.append((-i, 0))


        elif self.name == "knight":
            
            if(self.checkIfMoveIsValid(2, 1) != False):
                availableMoves.append((2, 1))

            if(self.checkIfMoveIsValid(2, -1) != False):
                availableMoves.append((2, -1))

            if(self.checkIfMoveIsValid(-2, 1) != False):
                availableMoves.append((-2, 1))

            if(self.checkIfMoveIsValid(-2, -1) != False):
                availableMoves.append((-2, -1))

            if(self.checkIfMoveIsValid(1, 2) != False):
                availableMoves.append((1, 2))

            if(self.checkIfMoveIsValid(1, -2) != False):
                availableMoves.append((1, -2))

            if(self.checkIfMoveIsValid(-1, 2) != False):
                availableMoves.append((-1, 2))

            if(self.checkIfMoveIsValid(-1, -2) != False):
                availableMoves.append((-1, -2))

        elif self.name == "bishop":
            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(i, i) == False:
                        break
                    availableMoves.append((i, i))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(i, -i) == False:
                        break
                    availableMoves.append((i, -i))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(-i, i) == False:
                        break
                    availableMoves.append((-i, i))

            for i in range(8): 
                if i != 0:
                    if self.checkIfMoveIsValid(-i, -i) == False:
                        break
                    availableMoves.append((-i, -i))


        elif self.name == "queen":
            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(0, i) == False:
                        break
                    availableMoves.append((0, i))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(0, -i) == False:
                        break
                    availableMoves.append((0, -i))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(i, 0) == False:
                        break
                    availableMoves.append((i, 0))

            for i in range(9):
                if i != 0:
                    if self.checkIfMoveIsValid(-i, 0) == False:
                        break
                    availableMoves.append((-i, 0))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(i, i) == False:
                        break
                    availableMoves.append((i, i))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(i, -i) == False:
                        break
                    availableMoves.append((i, -i))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(-i, i) == False:
                        break
                    availableMoves.append((-i, i))

            for i in range(8):
                if i != 0:
                    if self.checkIfMoveIsValid(-i, -i) == False:
                        break
                    availableMoves.append((-i, -i))
        elif self.name == "king":
            if(self.checkIfMoveIsValid(0, 1) != False):
                availableMoves.append((0, 1))

            if(self.checkIfMoveIsValid(0, -1) != False):
                availableMoves.append((0, -1))

            if(self.checkIfMoveIsValid(1, 0) != False):
                availableMoves.append((1, 0))

            if(self.checkIfMoveIsValid(-1, 0) != False):
                availableMoves.append((-1, 0))

            if(self.checkIfMoveIsValid(1, 1) != False):
                availableMoves.append((1, 1))

            if(self.checkIfMoveIsValid(1, -1) != False):
                availableMoves.append((1, -1))

            if(self.checkIfMoveIsValid(-1, 1) != False):
                availableMoves.append((-1, 1))

            if(self.checkIfMoveIsValid(-1, -1) != False):
                availableMoves.append((-1, -1))

        availableSlots.clear()

        for move in availableMoves:
            # check if the move is valid
            position = (get_grid_by_mouse_position((self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward)))
            availableSlots.append(position)

        return availableMoves
    
    def checkIfMoveIsValid(self, x, y, checkForwards = True):
        position = get_grid_by_mouse_position((self.x + x * grid_increment[0] * self.forward, self.y + y * grid_increment[1] * self.forward))
        piece = getPieceAtGridPosition(position[0], position[1])
        if piece != None:
            return False
        
        return True
    
    def checkIfAttackIsValid(self, x, y, ignoreKing = False):
        position = get_grid_by_mouse_position((self.x + x * grid_increment[0] * self.forward, self.y + y * grid_increment[1] * self.forward))
        piece = getPieceAtGridPosition(position[0], position[1])

        if(ignoreKing == False):
            if piece != None and piece.color != self.color and piece.name != "king":
                return True
        else:
            if piece != None and piece.color != self.color:
                return True
        
        return False
    
    def checkBlock(self, x, y):
        position = get_grid_by_mouse_position((self.x + x * grid_increment[0] * self.forward, self.y + y * grid_increment[1] * self.forward))
        piece = getPieceAtGridPosition(position[0], position[1])
        if piece != None and piece.color == self.color:
            return True
        
        return False   
    
    def checkIfKingIsInCheck(self):
        attackingMoves = self.getAttackingMoves(True)

        for move in attackingMoves:
            gridPosition = get_grid_by_mouse_position((self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward))
            pieceAtPosition = getPieceAtGridPosition(get_grid_by_mouse_position((self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward))[0], get_grid_by_mouse_position((self.x + move[0] * grid_increment[0] * self.forward, self.y + move[1] * grid_increment[1] * self.forward))[1])

            if(pieceAtPosition != None and pieceAtPosition.name == "king" and pieceAtPosition.color != self.color):
                return True
                    
        return False
    
    def movePiece(self, x, y):

        # check if a piece is at the position
        piece = getPieceAtGridPosition(get_grid_by_mouse_position((x, y))[0], get_grid_by_mouse_position((x, y))[1])

        if(piece != None):
            if(piece.color != self.color):
                piecesOnBoard.remove(piece)
            else:
                return
            
        if self.canEnpassant == True:
            if(x < self.x):
                leftPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[1])
                if(leftPiece != None and leftPiece.name == "pawn" and leftPiece.color != self.color):
                    piecesOnBoard.remove(leftPiece)

            if(x > self.x):
                rightPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[1])
                if(rightPiece != None and rightPiece.name == "pawn" and rightPiece.color != self.color):
                    piecesOnBoard.remove(rightPiece)

        self.x = x
        self.y = y
        self.piece_rect = self.image.get_rect(center=(self.x, self.y))

        if(self.pawnMoved == False and self.name == "pawn"):
            self.pawnMoved = True
            
            # check if enpassant is possible by checking side pieces
            leftPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x - grid_increment[0], self.y))[1])
            rightPiece = getPieceAtGridPosition(get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[0], get_grid_by_mouse_position((self.x + grid_increment[0], self.y))[1])

            if(leftPiece != None and leftPiece.name == "pawn" and leftPiece.color != self.color):
                leftPiece.canEnpassant = True
                print ("Enpassant possible")

            if(rightPiece != None and rightPiece.name == "pawn" and rightPiece.color != self.color):
                rightPiece.canEnpassant = True
                print ("Enpassant possible")
        

        if(self.checkIfKingIsInCheck() == True):
            if(self.color == "white"):
                blackKingIsInCheck = True
                print("Black king is in check")
            else:
                whiteKingIsInCheck = True
                print("White king is in check")
        drawBoard()


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

    text_x = ["a", "b", "c", "d", "e", "f", "g", "h"]
    text_y = ["1", "2", "3", "4", "5", "6", "7", "8"]

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

# place black pawns
for i in range(8):
    piecesOnBoard.append(Piece("pawn", "black", get_centered_position(i, 1)[0], get_centered_position(i, 1)[1]))

# place black pieces
for i in range(8):
    piecesOnBoard.append(Piece(pieces_layout_ref[i], "black", get_centered_position(i, 0)[0], get_centered_position(i, 0)[1]))


# place white pawns
for i in range(8):
    piecesOnBoard.append(Piece("pawn", "white", get_centered_position(i, 6)[0], get_centered_position(i, 6)[1]))

# place white pieces
for i in range(8):
    piecesOnBoard.append(Piece(pieces_layout_ref[i], "white", get_centered_position(i, 7)[0], get_centered_position(i, 7)[1]))
    
# ---------------------------------------------------

# DRAW BOARD ---------------------------------------------------
drawBoard()
# ---------------------------------------------------

status = True
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

            for slot in availableSlots:
                    if(slot[0] == interacted_grid[0] and slot[1] == interacted_grid[1] and pieceMovesShown != None):
                        print("Move piece")
                        pieceMovesShown.movePiece(get_centered_position(slot[0], slot[1])[0], get_centered_position(slot[0], slot[1])[1]) 
                        pieceMovesShown = None
                        availableSlots = []
                        recentlyMoved = True

                        if(colorInTurn == "white"):
                            colorInTurn = "black"
                        else:
                            colorInTurn = "white"
                            
                        break


            if(recentlyMoved == False):
                piece = getPieceAtGridPosition(interacted_grid[0], interacted_grid[1])
                if(piece != None and piece.color == colorInTurn):
                    print(piece.name)
                    piece.showAvailableMoves()
                    pieceMovesShown = piece
            

        pygame.display.update()
 
# deactivates the pygame library
pygame.quit()