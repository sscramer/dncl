# Using an array of characters to simulate a string
s_arr = ['h', 'e', 'l', 'l', 'o']
n = len(s_arr)
reversed_s_arr = [''] * n # Pre-sized empty array

for i in range(n):
  reversed_s_arr[i] = s_arr[n - 1 - i]

# The output will be an array, which is testable.
print(reversed_s_arr)
