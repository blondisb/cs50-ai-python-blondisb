
a = not(True)
# print(a)

c = 1
matrix = [[5, 2], [3, 4], [1, 1]]
b = not(any(c in row for row in matrix))
# print(b)

matrix = [[1, 1, 1], [1, 1, 1], [1, 1, 2]]
counter = sum(row.count(1) for row in matrix)
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
    print({(0,0)})
print(moves)