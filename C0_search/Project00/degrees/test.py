

neighbors = [('112384', '200'),
            ('104257', '197'),
            ('112384', '102'),
            ('104257', '129'),
            ('112384', '158'),
            ('104257', '102'),
            ('104257', '193'),
            ('112384', '641')]

# if '200' in neighbors[0]:
#     print(99)
# else:
#     print(98)

# for mov, per in neighbors:
#     print(mov, '-', per)




# print('--------------')
# bb = (1,2)
# print(bb[0])

# cc = neighbors.remove(neighbors[-1])
# print('--------------')
# print(cc)
# print(neighbors[-1])




a = [1, 2, 3]
b = [44, 55, 66]
a.reverse()
b.reverse()
print(a)
c = (a, b)
d = []
print(type(c), '|||', c)

for i in range(len(a)):
    d.append((a[i], b[i]))
print(d)

d = list(zip(a, b))
print(d)



def bfs_gpt():
    from collections import deque
    def bfs(graph, start):
        visited = set()
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                print(vertex, end=" ")  # Process the current vertex (you can modify this part)
                visited.add(vertex)
                queue.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)

    # Example graph represented as an adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F', 'G'],
        'D': ['B'],
        'E': ['B'],
        'F': ['C'],
        'G': ['C']
    }

    # Starting BFS from node 'A'
    print("BFS starting from node 'A':")
    bfs(graph, 'A')

# bfs_gpt()
