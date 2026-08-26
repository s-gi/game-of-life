#!/usr/bin/env python3
"""A modernized implementation of Conway's Game of Life using curses."""

import curses
import random
import time


class GameEngine:
    """Handles the pure game mechanics and state calculation."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = self.initialize_grid()
        self.generations = 0

    def initialize_grid(self) -> list[list[bool]]:
        """Creates an empty grid initialized to False."""
        return [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def seed_grid(self) -> None:
        """Randomly populates the grid with alive cells (25% chance)."""
        self.grid = [
            [random.random() < 0.25 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.generations = 0

    def count_neighbors(self, r: int, c: int) -> int:
        """Counts alive adjacent neighbors for a given cell coordinate."""
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc]:
                        count += 1
        return count

    def step(self) -> int:
        """Ticks the game board forward one generation. Returns alive count."""
        next_grid = self.initialize_grid()
        alive_count = 0

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)
                is_alive = self.grid[r][c]

                if is_alive and (2 <= neighbors <= 3):
                    next_grid[r][c] = True
                elif not is_alive and neighbors == 3:
                    next_grid[r][c] = True

                if next_grid[r][c]:
                    alive_count += 1

        self.grid = next_grid
        self.generations += 1
        return alive_count


class GameOfLifeUI:
    """Handles curses terminal rendering and keyboard inputs."""

    def __init__(self, stdscr: curses.window):
        self.stdscr = stdscr
        self.speed = 0.2
        self._init_curses()

        height, width = self.stdscr.getmaxyx()
        self.engine = GameEngine(height - 3, width)
        self.engine.seed_grid()

    def _init_curses(self) -> None:
        """Sets up colors and basic terminal attributes."""
        self.stdscr.clear()
        self.stdscr.nodelay(True)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def handle_resize(self) -> None:
        """Adjusts the engine matrix size if terminal size changes."""
        height, width = self.stdscr.getmaxyx()
        if self.engine.rows != height - 3 or self.engine.cols != width:
            self.engine = GameEngine(height - 3, width)
            self.engine.seed_grid()

    def draw(self, alive_count: int) -> None:
        """Renders the board matrix and UI elements onto the terminal frame."""
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Render matrix cells
        self.stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        for r in range(self.engine.rows):
            for c in range(self.engine.cols):
                if self.engine.grid[r][c]:
                    self.stdscr.addstr(r, c, chr(0x2B1A))
        self.stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # Render bottom layout labels
        title, credits_str = "Game Of Life", "By @zeal2end"
        status_str = (
            f"Exit: 'q' | Seed: 'r' | Fast: 'f' | Slow: 's' | "
            f"Generation: {self.engine.generations} | Alive Cells: {alive_count}"
        )

        label_row = height - 2
        self.stdscr.attron(curses.color_pair(3))
        self.stdscr.addstr(height - 1, 0, status_str[:width - 1])
        self.stdscr.attroff(curses.color_pair(3))

        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(label_row, 0, title)
        if width > len(credits_str) + len(title):
            self.stdscr.addstr(label_row, width - len(credits_str) - 1, credits_str)
        self.stdscr.attroff(curses.color_pair(2))

        self.stdscr.refresh()

    def run_loop(self) -> None:
        """Primary application frame tick lifecycle runner."""
        while True:
            self.handle_resize()
            alive_count = self.engine.step()
            self.draw(alive_count)

            time.sleep(self.speed)

            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.engine.seed_grid()
            elif key == ord('f'):
                self.speed = 0.1
            elif key == ord('s'):
                self.speed = 1.0


def main() -> None:
    curses.wrapper(lambda stdscr: GameOfLifeUI(stdscr).run_loop())


if __name__ == "__main__":
    main()
