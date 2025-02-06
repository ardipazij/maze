from typing import List, Tuple, Optional
import logging

gl_logger = logging.getLogger(name=__name__)

from PySide6.QtCore import QPoint
from PySide6.QtGui import (
    QPainter,
    QPen
)

from PySide6.QtOpenGLWidgets import QOpenGLWidget

from interface.model.base_classes.point import Point
from .config import (
    DEFAULT_CELL_SIZE,
    HEIGHT,
    WIDTH,
    GL_BACKGROUND_COLOR,
    GL_LINE_COLOR,
    GL_LINE_THICKNESS,
    GL_POINT_COLOR_START,
    GL_POINT_COLOR_END
)


class MazeOpenGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_open_flag = False
        self.rows = 0
        self.cols = 0
        self.maze: List[List[Point]] = []
        self.start_point: Optional[Point] = None
        self.end_point: Optional[Point] = None
        self.from_p = None
        self.to_p = None
        self.cell_width = DEFAULT_CELL_SIZE
        self.cell_height = DEFAULT_CELL_SIZE
        self.setFixedSize(WIDTH, HEIGHT)

        self.background_color = GL_BACKGROUND_COLOR
        self.line_color = GL_LINE_COLOR
        self.point_color_start = GL_POINT_COLOR_START
        self.point_color_end = GL_POINT_COLOR_END

    def set_colors(self, GL_BACKGROUND_COLOR, GL_LINE_COLOR, GL_POINT_COLOR_START, GL_POINT_COLOR_END):
        self.background_color = GL_BACKGROUND_COLOR
        self.line_color = GL_LINE_COLOR
        self.point_color_start = GL_POINT_COLOR_START
        self.point_color_end = GL_POINT_COLOR_END
        self.update()

    def set_maze_coordinates(self, rows: int, cols: int, maze: List[List[Point]]):
        self.rows = rows
        self.cols = cols
        self.maze = maze

        self.cell_width = WIDTH / self.cols
        self.cell_height = HEIGHT / self.rows

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.background_color)

        pen = QPen(self.line_color, GL_LINE_THICKNESS)
        painter.setPen(pen)

        for r in range(self.rows):
            for c in range(self.cols):
                point = self.maze[r][c]
                x = c * self.cell_width
                y = r * self.cell_height

                if point.right == 1:
                    painter.drawLine(x + self.cell_width, y, x + self.cell_width, y + self.cell_height)

                if point.bottom == 1:
                    painter.drawLine(x, y + self.cell_height, x + self.cell_width, y + self.cell_height)

        painter.drawLine(0, 0, 0, self.rows * self.cell_height)
        painter.drawLine(0, 0, self.cols * self.cell_width, 0)
        painter.drawLine(self.cols * self.cell_width, 0, self.cols * self.cell_width,
                         self.rows * self.cell_height)  # Right border
        painter.drawLine(0, self.rows * self.cell_height, self.cols * self.cell_width,
                         self.rows * self.cell_height)  # Bottom border

        if self.start_point:
            painter.setPen(QPen(GL_POINT_COLOR_START, GL_LINE_THICKNESS))
            painter.setBrush(GL_POINT_COLOR_START)
            radius = min(self.cell_width, self.cell_height) // 4
            painter.drawEllipse(self.start_point, radius, radius)

        if self.end_point:
            painter.setPen(QPen(GL_POINT_COLOR_END, GL_LINE_THICKNESS))
            painter.setBrush(GL_POINT_COLOR_END)
            radius = min(self.cell_width, self.cell_height) // 4
            painter.drawEllipse(self.end_point, radius, radius)

    def mousePressEvent(self, event):
        if self.file_open_flag:
            x = event.position().x()
            y = event.position().y()

            cell_x = int(x // self.cell_width)
            cell_y = int(y // self.cell_height)

            center_x = int(cell_x * self.cell_width + self.cell_width / 2)
            center_y = int(cell_y * self.cell_height + self.cell_height / 2)
            center = QPoint(center_x, center_y)
            gl_logger.info(f"{cell_x=}, {cell_y=}")

            if self.start_point is None:
                self.start_point = center
                self.from_p = self.maze[cell_y][cell_x]
                gl_logger.info(f"start: {self.start_point}")
            elif self.start_point is not None and self.end_point is None:
                self.end_point = center
                self.to_p = self.maze[cell_y][cell_x]
                gl_logger.info(f"end: {self.end_point}")
            else:
                update_dots(self)

            self.update()

    def draw_path(self, path: List[Tuple[int, int]]):
        if not path or len(path) < 2:
            return

        painter = QPainter(self)
        painter.setPen(QPen(GL_POINT_COLOR_END, min(self.cell_width, self.cell_height)))
        painter.setPen(QPen(GL_POINT_COLOR_END, GL_LINE_THICKNESS))
        for i in range(len(path) - 1):
            start_y, start_x = path[i]
            end_y, end_x = path[i + 1]

            painter.drawLine(
                start_x * self.cell_width + self.cell_width / 2,
                start_y * self.cell_height + self.cell_height / 2,
                end_x * self.cell_width + self.cell_width / 2,
                end_y * self.cell_height + self.cell_height / 2
            )
        painter.end()


def update_dots(widget: MazeOpenGLWidget):
    widget.start_point = None
    widget.end_point = None
    widget.from_p = None
    widget.to_p = None
