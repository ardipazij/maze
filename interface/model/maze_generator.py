import random
from typing import List

from interface.model.base_classes.point import Point


class MazeGenerator:

    def __init__(self):
        self.counter = 0

    def create_first_row(self, cols: int, current_row=0) -> List['Point']:
        result = [Point(0, 0, i, current_row, i) for i in range(cols)]
        self.counter = cols
        return result

    @staticmethod
    def merge_sets(row: List['Point'], index: int, element: int):
        mutable_set = row[index + 1].tag
        for point in row:
            if point.tag == mutable_set:
                point.tag = element

    def process_right_wall(self, row: List['Point']) -> List['Point']:
        for i in range(len(row) - 1):
            if row[i].tag == row[i + 1].tag:
                row[i].right = 1
            else:
                if random.choice([True, False]):
                    row[i].right = 1
                else:
                    self.merge_sets(row, i, row[i].tag)
        row[-1].right = 1
        return row

    def process_bottom_wall(self, row: List['Point']) -> List['Point']:
        for i in range(len(row)):
            if (random.choice([True, False])
                    and self.count_of_elements_in_unique_tag_without_bottom_wall(row, row[i].tag) > 1):
                row[i].bottom = 1
            else:
                row[i].bottom = 0
        return row

    @staticmethod
    def count_of_elements_in_unique_tag(row: List['Point'], tag: int) -> int:
        return sum(1 for point in row if point.tag == tag)

    @staticmethod
    def count_of_elements_in_unique_tag_without_bottom_wall(row: List['Point'], tag: int) -> int:
        return sum(1 for point in row if point.tag == tag and point.bottom == 0)

    def create_new_row(self, row: List['Point'], current_row: int) -> List['Point']:
        new_row = [Point(point.right, point.bottom, point.tag, current_row, point.y) for point in row]
        for i in range(len(new_row)):
            new_row[i].right = 0
            if new_row[i].bottom:
                self.counter += 1
                new_row[i].bottom = 0
                new_row[i].tag = self.counter
        return new_row

    def build_last_row(self, maze: List[List['Point']], maze_rows: int, maze_cols: int):
        self.process_right_wall(maze[maze_rows - 1])

        for i in range(maze_cols - 1):
            maze[maze_rows - 1][i].bottom = 1
            if maze[maze_rows - 1][i].tag != maze[maze_rows - 1][i + 1].tag and maze[maze_rows - 1][i].right == 1:
                maze[maze_rows - 1][i].right = 0  # Remove right wall
                self.merge_sets(maze[maze_rows - 1], i, maze[maze_rows - 1][i].tag)
        maze[maze_rows - 1][maze_cols - 1].bottom = 1

    def generate_maze(self, rows: int, cols: int) -> List[List['Point']]:
        self.counter = 0
        maze = []
        first_row = self.process_bottom_wall(self.process_right_wall(self.create_first_row(cols)))
        maze.append(first_row)
        for i in range(1, rows - 1):
            new_row = self.process_bottom_wall(self.process_right_wall(self.create_new_row(maze[-1], i)))
            maze.append(new_row)

        maze.append(self.create_new_row(maze[-1], rows - 1))
        self.build_last_row(maze, rows, cols)
        return maze
