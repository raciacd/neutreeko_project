import random
import pygame
import sys
import os
from .board import Board
from .piece import Piece

# --------- Graph ----------#
SIZE =  5
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
GREEN = (78,255,93)
GREEN_1 = (88, 154, 141) 
GREEN_2 = (143, 193, 181)
GREEN_3 = (23,101,81)
CELL_SIZE = 100
BOARD_EDGE = 10
BOARD_SIZE = SIZE * CELL_SIZE
SPACE_SCREEN_BOARD = 100
SCREEN_SIZE = BOARD_SIZE + SPACE_SCREEN_BOARD
WIDTH_BUTTON = 250
HEIGHT_BUTTON = 80
WIDTH_BOX = 300
HEIGHT_BOX = 100
TIME = 300
PIECE_COLORS = (BLACK, WHITE)
FONT_PATH = os.path.join("assets", "font", "Bungee_Poppins", "Bungee", "Bungee-Regular.ttf")

class NeutreekoGame:
    def __init__(self, ai1 = None, ai2 = None):
        self.initial_position = [(4, 1),(1, 2), (4, 3)], [(0,1), (3, 2), (0,3)]
        self.board = Board(self.initial_position)
        self.player =[ ai1, ai2]
        self.button_clicked = False
        self.screen_update = False
        self.mouse_over_button = False
        self.game_pieces = [[], []]
        self.players_moved = False
        self.available_pieces = []
        
    def create_board_surface(self, screen):
        pygame.draw.rect(screen, BLACK, (SPACE_SCREEN_BOARD/2-BOARD_EDGE,SPACE_SCREEN_BOARD/2-BOARD_EDGE, BOARD_SIZE+BOARD_EDGE*2, BOARD_SIZE+BOARD_EDGE*2))
        for row in range(SIZE):
            for col in range(SIZE):
                color =  GREEN_1 if (row + col) % 2 == 0 else GREEN_2
                pygame.draw.rect(screen, color, (SPACE_SCREEN_BOARD/2+col * CELL_SIZE, SPACE_SCREEN_BOARD/2+row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def create_piece_surface(self, pieces, screen, clicked_piece):
        for i in range(len(pieces)):
            if len(self.game_pieces[i]) == 0:
                self.game_pieces[i] = [self.create_piece(p, i+1, PIECE_COLORS[i], screen) for p in pieces[i]]
            else:
                self.draw_piece(self.game_pieces[i], screen)
                      
        if clicked_piece:
            self.available_pieces = [self.create_piece(p, self.board.current_player, GREEN, screen, clicked_piece) for p in clicked_piece.piece_moves]
            return
        
        if len(self.available_pieces) > 0:
            self.draw_piece(self.available_pieces, screen)

    def draw_piece(self, pieces, screen):
        for p in pieces:
            p.draw(screen)
    
    def create_piece(self, piece, player, color, screen, father = None):
        piece = Piece(self.board, piece, player, color, CELL_SIZE, SPACE_SCREEN_BOARD/2, father)
        piece.draw(screen)
        return piece
            
    def update_board_screen(self, screen, clicked_piece = None):
        self.create_board_surface(screen)
        self.create_piece_surface(self.board.pieces, screen, clicked_piece)
        pygame.display.flip()

    def update_home_screen(self, screen):
        pygame.draw.rect(screen, GREEN_1, (0, 0, SCREEN_SIZE, SCREEN_SIZE))
    
    def check_click(self, screen, pos):
        for piece in self.game_pieces[self.board.current_player-1]:
            if piece.is_clicked(pos):
                self.update_board_screen(screen, piece) 
                return
    
        for piece in self.available_pieces:
            if piece.is_clicked(pos):
                self.board.move((piece.father.row, piece.father.col), (piece.row, piece.col))
                self.available_pieces = []
                self.game_pieces = [[],[]]
                self.players_moved = True
                return

        
    def run_game(self):
        self.board = Board(self.initial_position)
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        pygame.display.set_caption("Neutreeko")
        font_1 = pygame.font.Font(FONT_PATH, 30)
        font_2 = pygame.font.Font(FONT_PATH, 60)
        start_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 200, WIDTH_BUTTON, HEIGHT_BUTTON)
        rules_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 300, WIDTH_BUTTON, HEIGHT_BUTTON)
        obs_button_rect = pygame.Rect((SCREEN_SIZE - WIDTH_BUTTON)/2, 400, WIDTH_BUTTON, HEIGHT_BUTTON)

        while True: 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:   
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.button_clicked and start_button_rect.collidepoint(event.pos):
                        self.button_clicked = True
                        self.update_board_screen(screen)
                    elif self.button_clicked and self.player[self.board.current_player-1] is None:
                        mouse_pos = pygame.mouse.get_pos()
                        self.check_click(screen, mouse_pos)

            if self.button_clicked:
                if self.player[self.board.current_player-1]:

                    if self.board.current_player == 1:
                        self.player[0](self)
                    else:
                        self.player[1](self)   
                    pygame.time.wait(TIME)
                    self.players_moved = True
                self.update_board_screen(screen)

                if self.players_moved: 
                    if self.board.winner != -1:
                        text = f"Player {self.board.winner} wins!" if self.board.winner != 0 else "Draw!"
                        self.create_text(screen, text, font_1, WHITE, ((SCREEN_SIZE - WIDTH_BOX)/2, (SCREEN_SIZE - HEIGHT_BOX )/2), True)
                        pygame.time.wait(2000)
                        pygame.quit()
                        return  
                    self.board.current_player = 3 - self.board.current_player
                    self.players_moved = False
            
            if not self.screen_update:
                self.update_home_screen(screen)
                self.create_text(screen, "NEUTREEKO", font_2, WHITE, 100)
                self.draw_button(screen, 'Start Game', font_1, start_button_rect,(SCREEN_SIZE/2, start_button_rect.y))
                self.draw_button(screen, 'Rules', font_1, rules_button_rect,((SCREEN_SIZE/2, rules_button_rect.y)))
                self.draw_button(screen, 'Information', font_1, obs_button_rect,((SCREEN_SIZE/2, obs_button_rect.y)))
                self.screen_update = True

    def create_text(self, screen, text, font, color_text, position, box=False):
        #text_rect = text_surface.get_rect()
        text_surface = font.render(text, True, color_text)
        text_width, text_height = text_surface.get_size()
        if box:
            text_rect = pygame.Rect(position[0], position[1], WIDTH_BOX, HEIGHT_BOX)
            pygame.draw.rect(screen, BLACK, text_rect)
            screen.blit(text_surface, ((SCREEN_SIZE - text_width)/2, (SCREEN_SIZE - text_height )/2))
        else:
            screen.blit(text_surface, ((SCREEN_SIZE - text_width)/2, position))
        pygame.display.flip()

    def draw_button(self, screen, text, font, button_rect, position):   
        pygame.draw.rect(screen, GREEN_3, button_rect, 0, 10)
        button_surface = font.render(text, True, WHITE)
        text_width, text_height = button_surface.get_size()
        screen.blit(button_surface, (position[0]-text_width/2, position[1]+ (HEIGHT_BUTTON - text_height)/2))
        pygame.display.flip()

def execute_random_move(game):
    new_pieces = random.choice(game.board.available_moves())

    game.board.move(new_pieces[0], new_pieces[1])
