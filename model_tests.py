import pytest
from interface.model.base_classes.point import Point
from interface.model.maze_generator import MazeGenerator
from interface.model.maze_solver import MazeSolver
from collections import deque


@pytest.fixture
def maze_generator():
    return MazeGenerator()


@pytest.fixture
def maze_solver():
    return MazeSolver()


def test_create_first_row(maze_generator):
    cols = 5
    row = maze_generator.create_first_row(cols)
    assert len(row) == cols
    for i in range(cols):
        assert row[i].x == 0
        assert row[i].y == i
        assert row[i].tag == i
        assert row[i].right == 0
        assert row[i].bottom == 0


def test_merge_sets(maze_generator):
    row = [Point(0, 0, 2, 0, i) for i in range(5)]
    row[0].tag = 1
    row[1].tag = 1
    row[2].tag = 2
    maze_generator.merge_sets(row, 1, row[1].tag)
    assert all(point.tag == 1 for point in row)


def test_process_right_wall(maze_generator):
    row = maze_generator.create_first_row(5)
    row = maze_generator.process_right_wall(row)
    assert len(row) == 5
    assert row[-1].right == 1


def test_process_bottom_wall(maze_generator):
    row = maze_generator.create_first_row(5)
    row = maze_generator.process_bottom_wall(row)
    assert len(row) == 5


def test_create_new_row(maze_generator):
    row = maze_generator.create_first_row(5)
    row = maze_generator.process_right_wall(row)
    row = maze_generator.process_bottom_wall(row)
    new_row = maze_generator.create_new_row(row, 1)
    assert len(new_row) == 5
    assert all(point.right == 0 for point in new_row)


def test_build_last_row(maze_generator):
    cols = 5
    maze = [maze_generator.create_first_row(cols)]
    maze.append(maze_generator.process_right_wall(maze_generator.create_new_row(maze[0], 1)))
    maze_generator.build_last_row(maze, 2, cols)
    last_row = maze[-1]
    assert len(last_row) == cols
    assert last_row[-1].bottom == 1


def test_generate_maze(maze_generator):
    rows, cols = 4, 5
    maze = maze_generator.generate_maze(rows, cols)
    assert len(maze) == rows
    for row in maze:
        assert len(row) == cols


@pytest.mark.parametrize("rows, cols", [(6, 6), (6, 10), (10, 6)])
def test_all_paths_connected(maze_generator, maze_solver, rows, cols):
    maze = maze_generator.generate_maze(rows, cols)

    for x1 in range(rows):
        for y1 in range(cols):
            from_point = Point(0, 0, 0, x1, y1)
            for x2 in range(rows):
                for y2 in range(cols):
                    to_point = Point(0, 0, 0, x2, y2)
                    path = maze_solver.solve(from_point, to_point, maze)
                    assert path is not None, f"No path found between {from_point} and {to_point}"
                    assert path[0] == (x2, y2), f"Path does not start at the correct point {from_point}"
                    assert path[-1] == (x1, y1), f"Path does not end at the correct point {to_point}"


def test_solver_initial_state(maze_solver):
    assert maze_solver.rows == 0
    assert maze_solver.cols == 0
    assert maze_solver.maze == []
    assert maze_solver.length_map == []
    assert maze_solver.old_wave == deque()
    assert maze_solver.wave_step == 0
    assert not maze_solver.is_good()


def test_solver_simple_path(maze_generator, maze_solver):
    maze = maze_generator.generate_maze(2, 2)
    from_point = Point(0, 0, 0, 0, 0)
    to_point = Point(0, 0, 0, 1, 1)

    path = maze_solver.solve(from_point, to_point, maze)
    assert path is not None
    assert path[0] == (1, 1)
    assert path[-1] == (0, 0)


def test_solver_no_path(maze_generator, maze_solver):
    maze = maze_generator.generate_maze(3, 3)

    # Принудительно создаем стену вокруг нижнего правого угла
    maze[1][2].bottom = 1
    maze[2][1].right = 1

    from_point = Point(0, 0, 0, 0, 0)
    to_point = Point(0, 0, 0, 2, 2)

    path = maze_solver.solve(from_point, to_point, maze)
    assert path == []


def test_solver_full_maze(maze_generator, maze_solver):
    maze = maze_generator.generate_maze(5, 5)

    from_point = Point(0, 0, 0, 0, 0)
    to_point = Point(0, 0, 0, 4, 4)
    path = maze_solver.solve(from_point, to_point, maze)
    assert path is not None
    assert path[0] == (4, 4)
    assert path[-1] == (0, 0)

    for x, y in path:
        assert 0 <= x < 5
        assert 0 <= y < 5


def test_solver_path_validity(maze_generator, maze_solver):
    maze = maze_generator.generate_maze(4, 4)

    from_point = Point(0, 0, 0, 0, 0)
    to_point = Point(0, 0, 0, 3, 3)
    path = maze_solver.solve(from_point, to_point, maze)

    assert path is not None

    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        assert abs(x1 - x2) + abs(y1 - y2) == 1

        if x1 == x2:
            if y1 < y2:  # Вправо
                assert maze[x1][y1].right == 0
            else:  # Влево
                assert maze[x2][y2].right == 0
        elif y1 == y2:
            if x1 < x2:  # Вниз
                assert maze[x1][y1].bottom == 0
            else:  # Вверх
                assert maze[x2][y2].bottom == 0
