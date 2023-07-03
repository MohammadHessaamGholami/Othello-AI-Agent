board = ((2, 2, 2, 2), (0, 2, 1, 0), (2, 1, 2, 0), (0, 1, 1, 2))
board1 = ((2, 2, 2, 2), (0, 2, 1, 0), (2, 1, 2, 0), (0, 1, 1, 2))
def compute_utility(board, color):
    color_number=0
    counter_color_number=0
    for row in board:
        for item in row:
            if (item == color):
                color_number +=1
            elif (item != 0):
                counter_color_number +=1
    print(color_number-counter_color_number)
    print(color)
    color=1000
    print(color)
    return color_number-counter_color_number
def zero_number(board):
    number_zero=0
    for row in board:
        for item in row:
            if (item==0):
                number_zero=number_zero+1
    return number_zero
print(zero_number(board))
value = (10000,(None,None))
compute_utility(board,1)
my_dict={}
my_dict[board]=20
my_dict[board1]=30
my_dict[((2, 2, 2, 2), (0, 2, 1, 0), (2, 1, 2, 0), (0, 1, 1, 6))]=100
print(my_dict)