import random

ROWS = 50
COLS = 50

def generate_maze(rows, cols):
    right_walls = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
    bottom_walls = [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]
    return right_walls, bottom_walls

def print_maze(rows, cols, right_walls, bottom_walls):
    print(f"{rows} {cols}")
    
    for row in right_walls:
        print(" ".join(map(str, row)))
    
    print("\n")

    for row in bottom_walls:
        print(" ".join(map(str, row)))

if __name__ == "__main__":
    rows, cols = ROWS, COLS
    right_walls, bottom_walls = generate_maze(rows, cols)
    print_maze(rows, cols, right_walls, bottom_walls)
