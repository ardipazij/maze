from dataclasses import dataclass, field
from typing import List

from interface.model.base_classes.point import Point

def read_matrix(file, rows) -> List[List[int]]:
    result = []
    for _ in range(rows):
        result.append([int(x) for x in file.readline().strip().split()])
    return result

def read_file(filename) -> List[List[Point]]:
    maze = []
    with open(filename, "r") as f:
        rows, cols = tuple(int(x) for x in f.readline().split())
        right = read_matrix(f, rows)
        _ = f.readline()  # Skip empty line
        bottom = read_matrix(f, rows)
        for i in range(rows):
            row = []
            for j in range(cols):
                temp_point = Point(right[i][j], bottom[i][j], f"{i},{j}", i, j)
                row.append(temp_point)
            maze.append(row)
    return maze
