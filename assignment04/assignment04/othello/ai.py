import random
import sys
import time

from othello_shared import find_lines, get_possible_moves, get_score, play_move

my_dictionary = {1: {}, 2: {}}
for i in range (100):
    my_dictionary[1][i]={}
    my_dictionary[2][i]={}

#my_dictionary = {1: {}, 2: {}}
    #for i in range(100):
    #   my_dictionary[1][i] = {}
    #  my_dictionary[2][i] = {}
def compute_utility(board, color):
    '''
    color_number = 0
    counter_color_number = 0
    for row in board:
        for item in row:
            if (item == color):
                color_number += 1
            elif (item != 0):
                counter_color_number += 1
    return color_number - counter_color_number
    '''
    score=get_score(board)
    if (color==1):
        return score[0]-score[1]
    else:
        return score[1]-score[0]

def zero_number(board):
    number_zero=0
    for row in board:
        for item in row:
            if (item==0):
                number_zero=number_zero+1
    return number_zero


############################################### MINIMAX ####################################################

def minimax_min_node(board, color):
    value = (10000,(None,None))
    if (len(get_possible_moves(board,2))==0):
        return (compute_utility(board,1),(None,None))
    else:
        for successor in get_possible_moves(board,2):
            new_board = play_move(board,2,successor[0],successor[1])
            new_value=minimax_max_node(new_board,1)
            if (new_value[0] < value[0]):
                value = (new_value[0],(successor[0],successor[1]))
        return value


def minimax_max_node(board, color):
    value = (-10000, (None,None))
    if (len(get_possible_moves(board, 1)) == 0):
        return (compute_utility(board, 1),(None,None))
    else:
        for successor in get_possible_moves(board, 1):
            new_board = play_move(board, 1, successor[0], successor[1])
            new_value=minimax_min_node(new_board, 2)
            if (new_value[0] > value[0]):
                value = (new_value[0],(successor[0],successor[1]))
        return value


def select_move_minimax(board, color):

    if (color == 1): #if black
        value = minimax_max_node(board,1)
        return value[1]
    else:            #if white
        value = minimax_min_node(board,2)
        return value[1]

############################################ ALPHA-BETA PRUNING ############################################################


def alphabeta_min_node(board, color, alpha, beta):
    value = (10000, (None, None))
    if (len(get_possible_moves(board, 2)) == 0):
        return (compute_utility(board, 1), (None, None))
    else:
        number_of_zero=zero_number(board)       #dictionary
        if(board in my_dictionary[2][number_of_zero]): #dictionary
           return my_dictionary[2][number_of_zero][board] #dictionary
        for successor in get_possible_moves(board, 2):
            new_board = play_move(board, 2, successor[0], successor[1])
            new_value = alphabeta_max_node(new_board, 1,alpha,beta)
            if (new_value[0] < value[0]):
                value = (new_value[0], (successor[0], successor[1]))
                beta = min(value[0],beta)
                if (alpha >= beta):
                    break
        my_dictionary[2][number_of_zero][board]=value #dictionary
        return value


def alphabeta_max_node(board, color, alpha, beta):
    value = (-10000, (None, None))
    if (len(get_possible_moves(board, 1)) == 0):
        return (compute_utility(board, 1), (None, None))
    else:
        number_of_zero=zero_number(board) #dictionary
        if (board in my_dictionary[1][number_of_zero]): #dictionary
           return my_dictionary[1][number_of_zero][board] #dictionary
        for successor in get_possible_moves(board, 1):
            new_board = play_move(board, 1, successor[0], successor[1])
            new_value = alphabeta_min_node(new_board, 2,alpha,beta)
            if (new_value[0] > value[0]):
                value = (new_value[0], (successor[0], successor[1]))
                alpha = max(value[0],alpha)
                if (alpha >= beta):
                    break
        my_dictionary[1][number_of_zero][board]=value  #dictionary
        return value


def select_move_alphabeta(board, color):
    alpha=-1000
    beta=+1000
    final = []
    for row in board:
        final.append(tuple(row))
    final=tuple(final)
    if (color == 1): #if black
        value = alphabeta_max_node(final,1,alpha,beta)
        return value[1]
    else:            #if white
        value = alphabeta_min_node(final,2,alpha,beta)
        return value[1]

################################################################depth ###################################################
def alphabeta_min_node_deph(board, color, alpha, beta,deph):
    value = (10000, (None, None))
    if (len(get_possible_moves(board, 2)) == 0 or deph==0):
        return (compute_utility(board, 1), (None, None))
    else:
        for successor in get_possible_moves(board, 2):
            new_board = play_move(board, 2, successor[0], successor[1])
            new_value = alphabeta_max_node_deph(new_board, 1,alpha,beta,deph-1)
            if (new_value[0] < value[0]):
                value = (new_value[0], (successor[0], successor[1]))
                beta = min(value[0],beta)
                if (alpha >= beta):
                    break
        return value
def alphabeta_max_node_deph(board, color, alpha, beta,deph):
    value = (-10000, (None, None))
    if (len(get_possible_moves(board, 1)) == 0 or deph==0):
        return (compute_utility(board, 1), (None, None))
    else:
        for successor in get_possible_moves(board, 1):
            new_board = play_move(board, 1, successor[0], successor[1])
            new_value = alphabeta_min_node_deph(new_board, 2,alpha,beta,deph-1)
            if (new_value[0] > value[0]):
                value = (new_value[0], (successor[0], successor[1]))
                alpha = max(value[0],alpha)
                if (alpha >= beta):
                    break
        return value


def select_move_alphabeta_deph(board, color, deph):
    alpha=-1000
    beta=+1000
    final = []
    for row in board:
        final.append(tuple(row))
    final = tuple(final)

    if (color == 1): #if black
        value = alphabeta_max_node_deph(final,1,alpha,beta,deph)

        return value[1]
    else:            #if white
        value = alphabeta_min_node_deph(final,2,alpha,beta,deph)
        return value[1]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AIII")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)4
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)
        if status == "FINAL":  # Game is over.
            print
        else:
            # Read in the input and turn it into a Python
            board = eval(input())
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)
            # Select the move and send it to the manager
            #movei, movej = select_move_minimax(board, color) #just minimax
            #movei, movej = select_move_alphabeta(board, color) # alphabeta and dictionary
            movei, movej = select_move_alphabeta_deph(board, color,4) # with 5 depth minimax and alpha-beta

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
