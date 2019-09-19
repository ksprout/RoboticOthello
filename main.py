import random
from time import sleep

board = [[0 for i in range(8)] for j in range(8)]

def put_available(user):
    for i in range(8):
        for j in range(8):
            if put_stone_if_available(i, j, user, False):
                return True
    return False

def display_game_result():
    count_me = 0
    count_opponent = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                count_me += 1
            elif board[i][j] == -1:
                count_opponent += 1
    result = '相手の勝ち'
    if count_me > count_opponent:
        result = '自分の勝ち'
    elif count_me == count_opponent:
        result = '引き分け'
    print(f'結果は、● が{count_me}枚、○ が{count_opponent}枚で{result}です')

def display_board():
    print('>>>>>>>>>>')
    for row in board:
        print(' '.join([to_stone(row, i) for i in range(len(row))]))

def to_stone(row, index):
    if row[index] == 0:
        return '-'
    elif row[index] == 1:
        return '●'
    elif row[index] == -1:
        return '○'
    else:
        return '?'

def turn_over_stones_if_available(row, col, slope, color, change):
    '''
    slope: 対象の傾きを表す。
    0: 水平
    1: 右上がり
    -1: 左上がり
    2: 縦    
    '''
    changed = False
    proponent_i = [-1 for i in range(2)]
    opponent_i = [-1 for i in range(2)]
    targets, my_index = get_target_line(row, col, slope)
    for target in targets:
        target[2] = board[target[0]][target[1]]
    for x in range(0, my_index):
        if targets[x][2] == color:
            proponent_i[0] = x
        elif targets[x][2] == -1 * color:
            opponent_i[0] = x
        else:
            proponent_i[0] = -1
            opponent_i[0] = -1
    for x in range(my_index + 1, len(targets))[::-1]:
        if targets[x][2] == color:
            proponent_i[1] = x
        elif targets[x][2] == -1 * color:
            opponent_i[1] = x
        else:
            proponent_i[1] = -1
            opponent_i[1] = -1
    if proponent_i[0] != -1 and opponent_i[0] == my_index - 1:
        for i in range(proponent_i[0] + 1, opponent_i[0] + 1):
            if change:
                board[targets[i][0]][targets[i][1]] = color
            changed = True
    if proponent_i[1] != -1 and opponent_i[1] == my_index + 1:
        for i in range(opponent_i[1], proponent_i[1]):
            if change:
                board[targets[i][0]][targets[i][1]] = color
            changed = True
    return changed

def get_target_line(row, col, slope):
    targets = []
    my_index = -1
    if slope == 0:
        for i in range(8):
            targets.append([row, i, 0])
            if i == col:
                my_index = i
    elif slope == 2:
        for i in range(8):
            targets.append([i, col, 0])
            if i == row:
                my_index = i
    else:
        for i in range(-8, 9):
            new_row = row + i
            new_col = col + i * slope * -1
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                targets.append([new_row, new_col, 0])
            if new_row == row and new_col == col:
                my_index = len(targets) - 1
    return targets, my_index

def put_stone_if_available(row, col, color, change):
    if board[row][col] == 0:
        r0 = turn_over_stones_if_available(row, col, 0, color, change)
        r1 = turn_over_stones_if_available(row, col, 1, color, change)
        r2 = turn_over_stones_if_available(row, col, -1, color, change)
        r3 = turn_over_stones_if_available(row, col, 2, color, change)
        if r0 or r1 or r2 or r3:
            if change:
                board[row][col] = color
            return True
    return False

def main():
    print('あなたは ● を置くことができます')
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1
    display_board()
    current_user = 1
    while True:
        if current_user == 1:
            if put_available(1):
                print('● のターンです')
                params = input().split()
                if len(params) == 1 and params[0] == 'q':
                    print('終了します')
                    break
                elif len(params) != 2:
                    print('入力形式が正しくありません')
                    continue
                if put_stone_if_available(int(params[1]), int(params[0]), current_user, True):
                    display_board()
                    current_user *= -1
                else:
                    print('そこには置けません')
            elif put_available(-1):
                print('置ける場所がないのでスキップします')
                current_user *= -1
            else:
                print('ゲーム終了です')
                display_game_result()
                break
        else:
            sleep(1)
            if put_available(-1):
                candidates = [[r, c] for r in range(8) for c in range(8)]
                random.shuffle(candidates)
                for candidate in candidates:
                    if put_stone_if_available(candidate[0], candidate[1], current_user, True):
                        display_board()
                        current_user *= -1
                        break
            else:
                print('置ける場所がないのでスキップします')
                current_user *= -1

if __name__ == '__main__':
    main()
