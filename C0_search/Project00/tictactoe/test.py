from copy import deepcopy
import tictactoe


def main():
    a = not(True)
    # print(a)

    c = None
    matrix = [[5, 2], [3, 4], [None, None]]
    b = not(any(c in row for row in matrix))
    # print(b)

    matrix = [[None, None, None], [None, None, None], [None, None, 2]]
    counter = sum(row.count(None) for row in matrix)
    # if counter % 2 == 0:
    #     print('Even')
    # else:
    #     print('Odd')


    moves = set()
    for i, row in enumerate(matrix):
        for j, col in enumerate(row):
            # print(j, col)
            if col == 3:
                moves.add((i,j))
    if not moves:
        moves.add((0,0))
    #     print({(0,0)})
    # print(moves)

    a = [1, 2, 3]
    print(a[-1])
    for i in range(len(a)):
        print(i)


def copies():
    # Create a nested list
    original_list = [[None, 2, 3], [4, 5, 6], [7, 8, 9]]
    # Make a deep copy of the original list
    copied_list = copy.deepcopy(original_list)
    # Modify the original list
    original_list[0][0] = 'X'
    # Print both lists to see the difference
    print("Original List:", original_list)
    print("Copied List:", copied_list)


    original_set = {None, None, 2, 3, 4, 5, 2}
    # Shallow copy using copy()
    copied_set = original_set.copy()
    # Modify the original set
    original_set.add(6)
    # Print both sets
    # print("Original Set:", original_set)
    # print("Copied Set:", copied_set)


    copied_matrix = matrix[:]
    matrix[0][0] = None
    # print(copied_matrix)
    # print(matrix)


def transponse():
    board = [[1, None, None], [1, None, None], [1, None, None]]
    trn_board = zip(*board)
    print(trn_board)
    for i in trn_board:
        print(i)
        print(i.count(1))


def all_vs_count(board):
        X = 'X'
        O = 'O'
        for i in range(3):

            # ROWS: ganador por fila, asi que el primero no puede ser None 
            if board[i][0] != None:
                if all(cell == board[i][0] for cell in board[i]):   # Cada elemento de la row (board[i]) debe ser igual al primero de esa row
                    return board[i][0]
                
            # COLS: ganador por columna, asi que el primero no puede ser None 
            if board[i][0] != None:
                if all(row[i] == board[0][i] for row in board):     # Dentro de cada row, comparo el elemento i con el primero de la columna i
                    return board[0][i]



if __name__ == "__main__":

    # board = [[None, None, None], [None, None, None], [None, None, None]]
    # print(tictactoe.actions(board))
    # action = (0,1)
    # board = tictactoe.result(board, action)
    # print(tictactoe.actions(board))

    # transponse()
    # main()

    board = [[None, None, None], [None, None, None], [None, None, None]]
    # print(tictactoe.winner(board))
    # print(tictactoe.terminal(board))
    # print(tictactoe.utility(board))
    print(tictactoe.result(board, (0,1)))

    # print(all_vs_count(board))
    # print(all([1,2,3,2,'l',0]))