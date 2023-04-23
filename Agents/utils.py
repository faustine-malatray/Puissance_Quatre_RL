import numpy as np 

def get_pts_up(board, l, c):
    '''
    Compte le nombre de pions alignés vers le haut,
    Les pionts sont ajoutés au score s'il y a une case vide au dessus du pion le plus haut
    '''
    if l <= 2:
        return 0
    lined_up = 1
    while board[l - lined_up, c ] == board[l, c]:
        lined_up += 1
        if lined_up == 4:
            return 1000
    if board[l - lined_up, c ] == 0:
        return lined_up
    return 0

def get_pts_right(board, l, c):
    '''
    Compte le nombre de pions alignés horizontlement,
    Les pionts sont ajoutés au score s'il y a une case vide à droite du pion le plus à droie ou a gauche du pion le plus à gauche
    '''
    if c >= 4:
        return 0
    right_possibility = 0
    left_possibility = 0
    lined_up = 1
    while board[l, c + lined_up] == board[l, c]:
        lined_up += 1
        if lined_up == 4:
            return 1000
    if board[l, c + lined_up] == 0:
        right_possibility = 1
    if c != 0 :
        if board[l, c - 1] == 0:
            left_possibility = 1
    return lined_up * (left_possibility + right_possibility)

def get_pts_right_down(board, l, c):
    '''
    Compte le nombre de pions alignés en diagonale vert la droite et le bas,
    Les pionts sont ajoutés au score s'il y a une case vide pour agrandir la ligne
    '''
    if l >= 3 or c >= 4:
        return 0
    right_possibility = 0
    left_possibility = 0
    lined_up = 1
    while board[l + lined_up, c + lined_up] == board[l, c]:
        lined_up += 1
        if lined_up == 4:
            return 1000
    if board[l + lined_up, c + lined_up] == 0:
        right_possibility = 1
    if c != 0 and l != 0 :
        if board[l - 1, c - 1] == 0:
            left_possibility = 1
    return lined_up * (left_possibility + right_possibility)

def get_pts_right_up(board, l, c):
    '''
    Compte le nombre de pions alignés en diagonale vert la droite et le haut,
    Les pionts sont ajoutés au score s'il y a une case vide pour agrandir la ligne
    '''
    if l <= 2 or c >= 4:
        return 0
    right_possibility = 0
    left_possibility = 0
    lined_up = 1
    while board[l - lined_up, c + lined_up] == board[l, c]:
        lined_up += 1
        if lined_up == 4:
            return 1000
    if board[l - lined_up, c + lined_up] == 0 :
        right_possibility = 1
    if c != 0 and l != 5 :
        if board[l + 1, c - 1] == 0:
            left_possibility = 1
    return lined_up * (left_possibility + right_possibility)

def evaluate_position(board):
    ''' 
    Cette fonction  prend une grille de puissance 4 en entrée
    La fonction retourne un score
    Plus le score est élevé, plus le joueur 1 est en bonne position
    '''
    score_1 = 0
    score_2 = 0
    for l in range(6):
        for c in range(7):
            if board[l,c] == 1:
                score_1 = score_1 + get_pts_up(board, l, c) + get_pts_right(board, l, c) + get_pts_right_down(board, l, c) + get_pts_right_up(board, l, c)
            if board[l,c] == -1:
                score_2 = score_2 + get_pts_up(board, l, c) + get_pts_right(board, l, c) + get_pts_right_down(board, l, c) + get_pts_right_up(board, l, c)
    #print('Score de 1 :', score_1)
    #print('Score de 2 :', score_2)
    return score_1 - score_2

def new_move(board, i):
    layer = 5
    bottom = board[layer,i]
    while bottom !=0 and layer>0 :
        #print(i,"on monte d'un cran")
        layer-=1
        bottom = board[layer,i]
    if layer == 0 and bottom !=0:
        print("on est tout en haut y a pas de place")
    else :
        new_board = board.copy()
        new_board[layer,i] = 1
    return new_board

def get_move_score(board, i):
    board_after_i = new_move(board, i)
    a = evaluate_position(board_after_i)
    return a

if __name__ == '__main__':
    board = np.array([[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0]])
    print(evaluate_position(board))