# maze
implementation of generating perfect maze  according to Eller's algorithm and inpl of solving perfect maze according  Lee algorithm 

# Maze Generator and Solver

## Overview

This project provides a comprehensive solution for generating and solving mazes using a graphical user interface (GUI) built with PySide6. The application allows users to generate random mazes, visualize them, and find paths between specified points. The maze generation and solving algorithms are implemented in Python, and the GUI provides an intuitive interface for interacting with these features.

## Features

- **Maze Generation**: Generate random mazes of specified dimensions.
- **Maze Visualization**: Visualize the generated maze using a custom OpenGL widget.
- **Pathfinding**: Find and visualize the shortest path between two points in the maze.
- **File Operations**: Save the generated maze to a file and load mazes from files.
- **Customizable Parameters**: Adjust maze dimensions and visualization settings.

## Installation

To run this project, you need to have Python installed on your system. Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ardipazij/maze.git
   cd maze
   ```
2. **Create a Virtual Environment**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**:
   ```bash
     pip install -r requirements.txt
   ```
## Usage

1. **Run the Application**:
   ```bash
     python main.py
   ```
2. **Generate a Maze**:
   - Enter the desired number of rows and columns.
   - Click the "Generate" button to create a new maze
3. **Visualize the Maze** :
   -  The generated maze will be displayed in the main window.
   - Use the mouse to select the start and end points for pathfinding.
4. **Find a Path**:
   - Click the "Find Path" button to visualize the shortest path between the selected points.
5. **Save and Load Mazes**:
   - Use the "Save" button to save the current maze to a file.
   - Use the "Open File" button to load a maze from a file.

## Screenshots
<img src="img/1.png?" alt="Start position" width="500" />
<img src="img/2.png?" alt="The start point(green) and the end point(red)" width="500" />
<img src="img/3.png?" alt="The path" width="500" />

## Project Structure

- **`examples/random_maze.py`**: Script to generate a random maze.
- **`frontend/`**: Contains the GUI components and configuration.
  - **`config.py`**: Configuration settings for the GUI.
  - **`mainwindow.py`**: Main window of the application.
  - **`openglwidget.py`**: Custom OpenGL widget for maze visualization.
  - **`parser/maze_data.py`**: Functions to read maze data from files.
- **`interface/`**: Interfaces for maze generation and solving.
  - **`maze_interface.py`**: Interface for maze generation.
  - **`maze_solver_interface.py`**: Interface for maze solving.
  - **`model/`**: Contains the core algorithms for maze generation and solving.
    - **`maze_generator.py`**: Maze generation algorithm.
    - **`maze_solver.py`**: Maze solving algorithm.
    - **`base_classes/point.py`**: Base class for maze points.
- **`main.py`**: Entry point of the application.
- **`model_test.py`**: Unit tests for the maze generation and solving algorithms.
- **`requirements.txt`**: List of project dependencies.

## Testing

To run the unit tests, use the following command:
```bash
  pytest model_test.py
```

## Contributing

Special thanks to [celestiv](https://github.com/celestiv) for the frontend development.
