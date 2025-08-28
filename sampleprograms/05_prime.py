n = 97
is_prime = 1 # Using 1 for True, 0 for False

if n < 2:
  is_prime = 0
else:
  i = 2
  # Loop while i < n and we haven't found a divisor yet
  while i < n and is_prime == 1:
    if n % i == 0:
      is_prime = 0
    # In Python, you'd write i += 1.
    # To make it more explicit for translation, I'll do i = i + 1
    i = i + 1

if is_prime == 1:
  print("Prime")
else:
  print("Not Prime")
