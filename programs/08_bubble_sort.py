data = [87, 45, 72, 100, 25]
n = len(data)
for i in range(n):
  for j in range(0, n - i - 1):
    if data[j] > data[j+1]:
      # Swap elements
      temp = data[j]
      data[j] = data[j+1]
      data[j+1] = temp
# The default print output for a list is acceptable for testing.
print(data)
