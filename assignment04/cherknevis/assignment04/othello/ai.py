import random
import sys
import time

from othello_shared import find_lines, get_possible_moves, get_score, play_move

my_dictionary = {1: {}, 2: {}}

def compute_utility(board, color):
    score = get_score(board)
    if (color == 1):
        return score[0] - score[1]
    else:
        return score[1] - score[0]


############ MINIMAX ###############################

def minimax_min_node(board, color):
    pass


def minimax_max_node(board, color):
    pass


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    pass


############ ALPHA-BETA PRUNING #####################


def alphabeta_min_node(board, color, alpha, beta):
    value = (10000, (None, None))
    if (len(get_possible_moves(board, 2)) == 0):
        return (compute_utility(board, 1), (None, None))
    else:
        #############
        if (board in my_dictionary[2]):
            return my_dictionary[2][board]
        for successor in get_possible_moves(board, 2):
            new_board = play_move(board, 2, successor[0], successor[1])
            new_value = alphabeta_max_node(new_board, 1, alpha, beta)
            if (new_value[0] < value[0]):
                value = (new_value[0], (successor[0], successor[1]))
                beta = min(value[0], beta)
                if (alpha >= beta):
                    break
        ###########
        my_dictionary[2][board] = value
        return value


def alphabeta_max_node(board, color, alpha, beta):
    i=-1000
    j=-1000
    value = -10000
    if (len(get_possible_moves(board, 1)) == 0):
        return compute_utility(board, 1)
    else:
        ########
        if (board in my_dictionary[1]):
            return my_dictionary[1][board]
        for successor in get_possible_moves(board, 1):
            new_board = play_move(board, 1, successor[0], successor[1])
            new_value = alphabeta_min_node(new_board, 2, alpha, beta)
            if (new_value > value):
                i=successor[0]
                j=successor[1]
                value = new_value
                alpha = max(value, alpha)
                if (alpha >= beta):
                    break
        #########
        my_dictionary[1][board] = value
        return value


def select_move_alphabeta(board, color):
    alpha = -1000
    beta = +1000
    final = []
    for row in board:
        final.append(tuple(row))
    final = tuple(final)
    if (color == 1):  # if black
        value = alphabeta_max_node(final, 1, alpha, beta)
        return value
    else:  # if white
        value = alphabeta_min_node(final, 2, alpha, beta)
        return value


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
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
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
