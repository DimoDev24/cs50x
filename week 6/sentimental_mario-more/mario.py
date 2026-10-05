from cs50 import get_int

# Ask the user until give 1-8 height
while True:
    height = get_int("Choose the height of the pyramid (1-8): ")
    if height >= 1 and height <= 8:
        break

# Brick that we want to increase
brick = 1

while (height > 0):
    # Spaces before the first brick
    for space in range(height-1):
        print(" ", end="")

    # First column of bricks
    for i in range(brick):
        print("#", end="")

    # Space between
    print("  ", end="")

    # Second column of bricks
    for j in range(brick):
        print("#", end="")

    print()
    height -= 1
    brick += 1
