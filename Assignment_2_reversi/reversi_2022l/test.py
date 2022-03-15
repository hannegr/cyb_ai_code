import numpy as np

a = [[1,2,4,2,5],[5,4,2,3,1]]
b = [[1,4,3,4,5],[5,4,2,1,1]]

print([i == j for i, j in zip(a[0], b[0])])
listde = []
for i in range(len(a)): 
    listde.append([h == j for h, j in zip(a[i], b[i])])
print(listde)
