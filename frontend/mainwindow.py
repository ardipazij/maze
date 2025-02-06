from datetime import datetime
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

logger = logging.getLogger(name=__name__)

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QDoubleSpinBox
)

from .config import (
    HEIGHT,
    WIDTH,
    SPACE,
    MAIN_BACKGROUND_COLOR,
    BUTTON_SIZE
)

from .parser.maze_data import read_file
from interface.maze_solver_interface import MazeSolverInterface
from interface.maze_interface import MazeInterface
from .openglwidget import MazeOpenGLWidget, update_dots


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.data = None
        self.solver = MazeSolverInterface()
        self.generator = MazeInterface()
        self.setStyleSheet(f"background-color: {MAIN_BACKGROUND_COLOR};")
        self.setWindowTitle("Python Maze")
        self.setFixedWidth(WIDTH + SPACE)
        self.maze_widget = MazeOpenGLWidget(self)
        self.maze_widget.solver_gl = self.solver
        self.maze_widget.setGeometry(0, 0, HEIGHT, WIDTH)
        self.init_theme()
        self.init_widgets()

    def init_theme(self):
        palette = QApplication.palette()

        is_dark_theme = palette.color(QPalette.Window).lightness() < 128

        if is_dark_theme:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_light_theme(self):
        self.setStyleSheet("""
            background-color: white;
            color: black;
        """)

        self.maze_widget.set_colors(
            GL_BACKGROUND_COLOR=QColor("#ffffff"),
            GL_LINE_COLOR=QColor("#000000"),
            GL_POINT_COLOR_START=QColor("#00ff00"),
            GL_POINT_COLOR_END=QColor("#ff0000")
        )

    def set_dark_theme(self):
        self.setStyleSheet("""
            background-color: #2d2d2d;
            color: white;
        """)

        self.maze_widget.set_colors(
            GL_BACKGROUND_COLOR=QColor("#2d2d2d"),
            GL_LINE_COLOR=QColor("#ffffff"),
            GL_POINT_COLOR_START=QColor("#00ff00"),
            GL_POINT_COLOR_END=QColor("#ff0000")
        )
    def read_file_button_clicked(self):
        update_dots(self.maze_widget)
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text files (*.txt)")
            if fileName:
                logger.info(f"filename is: {fileName}")
                maze_data = read_file(fileName)
                self.data = maze_data

                rows = len(maze_data)
                cols = len(maze_data[0]) if rows > 0 else 0

                logger.info(f"Rows: {rows}, Cols: {cols}")
                logger.info(f"Right Walls: {[[point.right for point in row] for row in maze_data]}")
                logger.info(f"Bottom Walls: {[[point.bottom for point in row] for row in maze_data]}")

                if rows > 0 and cols > 0:
                    self.maze_widget.set_maze_coordinates(
                        rows=rows,
                        cols=cols,
                        maze=self.data
                    )
                    self.maze_widget.file_open_flag = True
                else:
                    logger.error("Parsed data is invalid. Ensure the file format is correct.")
            else:
                logger.error("No file selected. Try again")
        except TypeError as e:
            logger.error(f"Error: {e}. No file selected. Try again.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}. Try again.")
        except Exception as e:
            logger.error(f"Unexpected error: {e}. Try again.")

    def generate(self):
        update_dots(self.maze_widget)
        rows, cols = self.get_params()
        self.data = self.generator.generate_maze(rows, cols)
        self.maze_widget.set_maze_coordinates(
            rows=rows,
            cols=cols,
            maze=self.data
        )
        self.maze_widget.file_open_flag = True
        self.maze_widget.update()

    def get_params(self):
        r = int(self.rows_input.value())
        c = int(self.cols_input.value())
        logger.info(f"Generate maze with rows = {r}, cols = {c}")
        return (r, c)

    def init_widgets(self):
        # OpenGL widget
        self.maze_widget = MazeOpenGLWidget(self)
        self.maze_widget.solver_gl = self.solver
        self.maze_widget.setGeometry(0, 0, HEIGHT, WIDTH)

        # Buttons
        button_open_file = QPushButton("open file", self)
        button_open_file.setFixedSize(BUTTON_SIZE)
        button_open_file.clicked.connect(self.read_file_button_clicked)

        button_generate_maze = QPushButton("generate", self)
        button_generate_maze.setFixedSize(BUTTON_SIZE)
        button_generate_maze.clicked.connect(self.generate)

        button_save_maze = QPushButton("save", self)
        button_save_maze.setFixedSize(BUTTON_SIZE)
        button_save_maze.clicked.connect(self.save_file)

        button_draw_path = QPushButton("find path", self)
        button_draw_path.setFixedSize(BUTTON_SIZE)
        button_draw_path.clicked.connect(self.draw_path)
        # Params for input
        self.rows_input = QDoubleSpinBox(self)
        self.rows_input.setValue(10)
        self.rows_input.setSuffix(" rows")
        self.rows_input.setDecimals(0)
        self.rows_input.setMaximum(50)
        self.rows_input.setMinimum(1)
        self.cols_input = QDoubleSpinBox(self)
        self.cols_input.setValue(10)
        self.cols_input.setSuffix(" cols")
        self.cols_input.setDecimals(0)
        self.cols_input.setMaximum(50)
        self.cols_input.setMinimum(1)

        parameters_layout = QVBoxLayout()
        parameters_layout.addWidget(self.rows_input)
        parameters_layout.addWidget(self.cols_input)

        # Add widgets
        central_widget = QWidget(parent=self)

        controls_layout = QHBoxLayout()
        controls_layout.addLayout(parameters_layout)
        controls_layout.addWidget(button_generate_maze)
        controls_layout.addWidget(button_draw_path)
        controls_layout.addWidget(button_save_maze)
        controls_layout.addWidget(button_open_file)

        layout = QVBoxLayout()
        layout.addWidget(self.maze_widget)
        layout.addLayout(controls_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def save_file(self):
        rows = len(self.data)
        cols = len(self.data[0])

        right = [[point.right for point in row] for row in self.data]
        bottom = [[point.bottom for point in row] for row in self.data]

        with open(f"maze_{datetime.strftime(datetime.now(), "%y-%m-%d_%H:%M:%S")}.txt", "w+") as write_file:
            write_file.write(f"{rows} {cols}\n")

            for row in right:
                write_file.write(" ".join(str(i) for i in row) + "\n")

            write_file.write("\n")

            for row in bottom:
                write_file.write(" ".join(str(j) for j in row) + "\n")

    def draw_path(self):
        if not (self.maze_widget.from_p and  self.maze_widget.to_p):
            return
        path = self.solver.solve(self.maze_widget.from_p, self.maze_widget.to_p, self.maze_widget.maze)
        logger.info(f"{path}")
        update_dots(self.maze_widget)
        self.maze_widget.draw_path(path)
