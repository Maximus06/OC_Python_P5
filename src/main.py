"""This module launch the application"""

from .view.terminal import Terminal


def main():
    app = Terminal()
    app.run()

if __name__ == "__main__":
    main()