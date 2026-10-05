from cs50 import get_float

while True:
    change = get_float("How much change? ")
    if change > 0:
        break

# Round to eliminate de decimal part
change = round(change * 100)
coins = 0

while (change > 0):
    if change >= 25:
        change -= 25
        coins += 1
    elif change >= 10:
        change -= 10
        coins += 1
    elif change >= 5:
        change -= 5
        coins += 1
    else:
        change -= 1
        coins += 1

print(f"{coins}")
