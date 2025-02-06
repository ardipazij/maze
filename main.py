from PySide6.QtWidgets import (
    QApplication
)
from datetime import datetime
import sys
import logging
from frontend.mainwindow import MainWindow, logger

def init():
    logging.basicConfig(filename=f"log_{datetime.strftime(datetime.now(), "%y-%m-%d_%H:%M:%S")}.log", level=logging.INFO)
    app = QApplication([])
    logger.info("initializing mainwindow")
    mainwindow = MainWindow()
    return app, mainwindow

def main():
    app, mainwindow = init()
    mainwindow.show()
    logger.info("start application")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
