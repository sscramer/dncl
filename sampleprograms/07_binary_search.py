haystack = [25, 45, 72, 87, 100]
needle = 72
n = len(haystack)
found_index = -1
low = 0
high = n - 1
searching = 1

while low <= high and searching == 1:
  mid = (low + high) // 2
  if haystack[mid] == needle:
    found_index = mid
    searching = 0
  else:
    if haystack[mid] < needle:
      low = mid + 1
    else:
      high = mid - 1

print(found_index)
