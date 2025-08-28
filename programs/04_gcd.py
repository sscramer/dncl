a = 54
b = 24
while b != 0:
    temp = b
    b = a % b
    a = temp
print(a)
