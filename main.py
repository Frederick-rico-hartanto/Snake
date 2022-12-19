"""Run SnakeGame from program entry point.
"""

from menu_screens.root_window import RootWindow


def main() -> None:
    """Create instance of RootWindow and call its run() method."""
    snake = RootWindow()
    snake.run()


if __name__ == '__main__':
    main()
