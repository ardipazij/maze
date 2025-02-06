from interface.model.maze_generator import MazeGenerator
from typing import List


class MazeInterface:
    def __init__(self):
        self.maze = MazeGenerator()

    def generate_maze(self, rows, cols):
        return self.maze.generate_maze(rows, cols)
