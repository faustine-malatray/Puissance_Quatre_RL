import pygame
import numpy as np


class Board():
    def __init__(self):
        # Define constants
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.SQUARE_SIZE = 100
        self.RADIUS = int(self.SQUARE_SIZE/2 - 5)
        self.WIDTH = self.COLUMN_COUNT * self.SQUARE_SIZE
        self.HEIGHT = (self.ROW_COUNT+1) * self.SQUARE_SIZE
        self.SIZE = (self.WIDTH, self.HEIGHT)
        self.SCREEN_TITLE = "Connect 4 Game"

        # Define colors
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        # Initialize Pygame
        pygame.init()

        # Create the game window
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption(self.SCREEN_TITLE)

        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        self.draw_board()

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_move(self, board, col):
        return board[0][col] == 0

    def get_next_row(self, board, col):
        # print({r: board[r][col] for r in range(ROW_COUNT)})
        for r in range(self.ROW_COUNT-1, -1, -1):
            if board[r][col] == 0:
                return r

    def is_win(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

        return False

    def draw_board(self):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARE_SIZE,
                                                          r*self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(
                        c*self.SQUARE_SIZE+self.SQUARE_SIZE/2), int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.YELLOW, (int(
                        c*self.SQUARE_SIZE+self.SQUARE_SIZE/2), int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)), self.RADIUS)
                else:
                    pygame.draw.circle(self.screen, self.BLACK, (int(
                        c*self.SQUARE_SIZE+self.SQUARE_SIZE/2), int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)), self.RADIUS)

        pygame.display.update()
