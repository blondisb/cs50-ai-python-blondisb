aa = [   [41, 42, 43, 44]
        ,[11, 12, 13, 14]
        ,[21, 22, 23, 24]
        ,[31, 32, 33, 34]
		,[51, 52, 53, 54]
	]

pair = (4,3)
total_rows = len(aa)
total_cols = len(aa[0])
print(total_cols, total_rows)

print(aa[4][3])
print()
	
a = pair[0]-1
b = pair[0]+2
c = pair[1]-1
d = pair[1]+2

if a < 0:           a = 0
if b > total_rows:  b = total_rows
if c < 0:           c = 0
if d > total_cols:  d = total_cols

for i in range(a, b):
	for y in range(c, d):
	    print(aa[i][y])