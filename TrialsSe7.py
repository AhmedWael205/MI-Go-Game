import numpy as np

x=np.zeros((5,2),dtype=int)
print(x[0])
print(x[:,0])
print(x)
x[2]=1
print(x)
y=x.reshape(10)
print(y)
print(list(range(1,4)))

print((y==0))

print(np.asarray(np.where(y)))