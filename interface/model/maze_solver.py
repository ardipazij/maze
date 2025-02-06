from collections import deque
from typing import List, Any, Tuple

from interface.model.maze_generator import MazeGenerator
from interface.model.base_classes.point import Point


class MazeSolver:
    def __init__(self):
        self.maze: List[List[Point]] = []
        self.rows: int = 0
        self.cols: int = 0
        self.length_map: List[List[int]] = []
        self.old_wave = deque()
        self.wave_step: int = 0

    def is_good(self) -> bool:
        return self.rows > 0 and self.cols > 0

    def step_wave(self, to:Point) -> bool:
        self.wave_step += 1
        wave = deque()
        for row, col in self.old_wave:
            # Down
            if row + 1 < self.rows and self.maze[row][col].bottom == 0:
                if self.length_map[row + 1][col] == -1:
                    wave.append((row + 1, col))
                    self.length_map[row + 1][col] = self.wave_step
                if row + 1 == to.x and col == to.y:
                    return True
            # Up
            if row > 0 and self.maze[row - 1][col].bottom == 0:
                if self.length_map[row - 1][col] == -1:
                    wave.append((row - 1, col))
                    self.length_map[row - 1][col] = self.wave_step
                if row - 1 == to.x and col == to.y:
                    return True
            # Right
            if col + 1 < self.cols and self.maze[row][col].right == 0:
                if self.length_map[row][col + 1] == -1:
                    wave.append((row, col + 1))
                    self.length_map[row][col + 1] = self.wave_step
                if row == to.x and col + 1 == to.y:
                    return True
            # Left
            if col > 0 and self.maze[row][col - 1].right == 0:
                if self.length_map[row][col - 1] == -1:
                    wave.append((row, col - 1))
                    self.length_map[row][col - 1] = self.wave_step
                if row == to.x and col - 1 == to.y:
                    return True
        self.old_wave = wave
        return False

    def make_path(self, from_: Point, to: Point) -> List[Tuple[int, int]]:
        path = [(to.x, to.y)]
        row, col = to.x, to.y
        while self.length_map[row][col] != 0:
            if (col > 0 and self.length_map[row][col - 1] + 1 == self.length_map[row][col] and
                    self.maze[row][col - 1].right == 0):
                col -= 1
            elif col + 1 < self.cols and self.length_map[row][col + 1] + 1 == self.length_map[row][col] and \
                    self.maze[row][col].right == 0:
                col += 1
            elif row > 0 and self.length_map[row - 1][col] + 1 == self.length_map[row][col] and \
                    self.maze[row - 1][col].bottom == 0:
                row -= 1
            elif row + 1 < self.rows and self.length_map[row + 1][col] + 1 == self.length_map[row][col] and \
                    self.maze[row][col].bottom == 0:
                row += 1
            else:
                return []
            path.append((row, col))
        path[-1] = (from_.x, from_.y)
        return path

    def solve(self, from_: Point, to: Point,  maze: List[List[Point]]) -> List[Tuple[int, int]] | None:
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.length_map = [[-1] * self.cols for _ in range(self.rows)]
        self.old_wave = deque()
        self.wave_step = 0
        if not self.is_good():
            return None
        self.old_wave.append((from_.x, from_.y))
        self.length_map[from_.x][from_.y] = 0

        while self.old_wave:
            if self.step_wave(to):
                break

        return self.make_path(from_, to)
