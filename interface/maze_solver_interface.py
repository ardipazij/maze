from typing import List, Tuple

from interface.model.maze_solver import MazeSolver
from interface.model.maze_generator import MazeGenerator
from interface.model.base_classes.point import Point

class MazeSolverInterface:
    def __init__(self):
        self.maze_solver = MazeSolver()

    def solve(self, start_position: Point, end_position: Point,
              maze: List[List[Point]]) -> List[Tuple[int, int]] | None:
        return self.maze_solver.solve(start_position, end_position, maze)
