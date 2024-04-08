import pygame

class Piece:
    def __init__(self, board, piece, player, color, size, space, father):
        self.row = piece[0]
        self.col = piece[1]
        self.color = color
        self.radius = size // 2 - 2
        self.x = self.col * size + size / 2 +space
        self.y = self.row * size + size / 2 + space

        self.piece_moves = board.piece_move(piece, player)
        self.father = (father)

    def __str__(self):
        return f'({self.row}, {self.col})'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def is_clicked(self, pos):
        distance_squared = (pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2
        return distance_squared <= self.radius ** 2
