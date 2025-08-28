haystack = [87, 45, 72, 100, 25]
needle = 72
n = len(haystack)
found_index = -1
i = 0
searching = 1 # Flag to control the loop
while i < n and searching == 1:
  if haystack[i] == needle:
    found_index = i
    searching = 0 # Stop searching
  i = i + 1
print(found_index)
