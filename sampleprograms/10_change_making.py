amount = 93
coins = [25, 10, 5, 1]
num_coin_types = len(coins)
total_coin_count = 0

for i in range(num_coin_types):
  coin_value = coins[i]
  # Number of this coin to use
  count = amount // coin_value
  total_coin_count = total_coin_count + count
  # Remaining amount
  amount = amount % coin_value

print(total_coin_count)
