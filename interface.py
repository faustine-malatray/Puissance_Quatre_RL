import pygame
import numpy as np


def game_user_player(opponent):
    # Define constants
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    SQUARE_SIZE = 100
    RADIUS = int(SQUARE_SIZE/2 - 5)
    WIDTH = COLUMN_COUNT * SQUARE_SIZE
    HEIGHT = (ROW_COUNT+1) * SQUARE_SIZE
    SIZE = (WIDTH, HEIGHT)
    SCREEN_TITLE = "Connect 4 Game"

    # Define colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)

    # Initialize Pygame
    pygame.init()

    # Create the game window
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(SCREEN_TITLE)

    # Define functions

    def create_board():
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

    def drop_piece(board, row, col, piece):
        board[row][col] = piece

    def is_valid_move(board, col):
        return board[0][col] == 0

    def get_next_row(board, col):
        # print({r: board[r][col] for r in range(ROW_COUNT)})
        for r in range(ROW_COUNT-1, -1, -1):
            if board[r][col] == 0:
                return r

    def is_win(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

        return False

    def draw_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE,
                                                (r)*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(
                        c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(
                        c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, BLACK, (int(
                        c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)

        pygame.display.update()

    # Create the game board
    board = create_board()

    # Draw the initial board
    draw_board(board)

    # Initialize variables
    game_over = False
    turn = 0

    # Game loop
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    # Get the column that the user clicked
                    posx = event.pos[0]
                    col = int(posx // SQUARE_SIZE)
                    # print(col)

                    # Make the move if it's valid
                    if is_valid_move(board, col):
                        row = get_next_row(board, col)
                        # print(row)
                        drop_piece(board, row, col, 1)

                        # Check for a win
                        if is_win(board, 1):
                            print("Player 1 wins!")
                            game_over = True

                        # Switch turns
                        turn = 1

                else:
                    # TODO: Add RL agent code here

                    # Switch turns
                    # Get the column that the user clicked
                    posx = event.pos[0]
                    col = int(posx // SQUARE_SIZE)
                    # print(col)

                    # Make the move if it's valid
                    if is_valid_move(board, col):
                        row = get_next_row(board, col)
                        # print(row)
                        drop_piece(board, row, col, 2)

                        # Check for a win
                        if is_win(board, 2):
                            print("Player 2 wins!")
                            game_over = True
                    turn = 0

                # Draw the updated board
                draw_board(board)

    # Quit Pygame
    pygame.quit()
