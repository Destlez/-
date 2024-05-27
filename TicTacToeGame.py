Board = [1,2,3,4,5,6,7,8,9]
board_size=3

def ttt_board():
    '''board'''
    print('_'* 6 * board_size )
    for n in range(board_size):
        print((' '* 5 +'|')*3)
        print(' ', Board[n*3], "",'|','',Board[1+n*3],"",'|', '',Board[2 + n*3],"",'|')
        print(('_' * 5 + '|') * 3)
    pass
def move_step(L,char):
    ''' move '''
    if (L > 9 or L<1 or Board[L-1] in ('X','O')):
        return False
    Board[L-1] = char
    return True

def check_win():
    win = False
    win_comb =(
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    )
    for pos in win_comb:
        if (Board[pos[0]] == Board[pos[1]] and Board[pos[1]]== Board[pos[2]]):
            win = Board[pos[0]]
    return win
def start_play():
    current_player = 'X'
    step = 1
    ttt_board()

    while (step<10) and (check_win() == False):
        L = input('Turn first player ' + current_player + '. Board number (0 - exit);')

        if (L == '0'):
            break

        if (move_step(int(L),current_player)):
            print('Good move')

            if (current_player == 'X'):
                current_player = 'O'
            else:
                current_player = 'X'

            ttt_board()
            step += 1

        else:
            print('Incorrect move')

    if (step == 10 and check_win() == False):
        print('Draw')
    else:
        print('WINNER ' + check_win())

print("Welcome to the game tic tac toe!!!")
start_play()