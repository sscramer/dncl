n = 15
if n == 0:
  result = 0
elif n == 1:
  result = 1
else:
  a = 0
  b = 1
  for i in range(n - 1):
    next_b = a + b
    a = b
    b = next_b
  result = b
print(result)
