# Game of Life

A browser implementation of Conway's Game of Life, playable directly on GitHub Pages.

## Background

This project started from a Python implementation of Game of Life written as a single script mixing simulation logic and terminal rendering in one place. I refactored it to separate concerns: a pure `GameEngine` responsible for grid state and rules, and a rendering/input layer responsible for display and controls. This separation makes the simulation logic testable and independent of how it is presented.

To make the project easy to try without any setup, I ported it from a Python/curses terminal application to a static HTML/JS version. This removes the need to clone the repo or run a local environment, and lets it run directly from GitHub Pages.

The original Python/curses version is included in `python/game_of_life.py` for reference.

## Project structure

```
game-of-life/
├── index.html            browser version, served by GitHub Pages
├── python/
│   └── game_of_life.py   original curses TUI version
├── .github/
│   └── workflows/
│       └── ci.yml        lints the Python source and validates the HTML
├── README.md
└── LICENSE
```

## Architecture

- `GameEngine` — grid state, neighbor counting, and the step function implementing Conway's rules. No rendering or input logic.
- `TerminalRenderer` — draws the current grid state to a canvas.
- `App` — owns the timing loop, keyboard and pointer input, and resize handling; wires the engine and renderer together.

## Controls

- `R` — reseed with a random population
- `C` — clear the grid
- `F` / `S` — increase / decrease simulation speed
- `Space` — pause or resume
- Click or drag on the grid while paused to draw cells manually

On-screen buttons provide the same controls for touch devices.

## Running locally

Open `index.html` in a browser. No build step or dependencies required.

## Setting up this repo

The repo was created locally and pushed to an empty GitHub repository:

```
git init
git add .
git commit -m "Initial commit: Game of Life TUI port"
git branch -M main
git remote add origin https://github.com/s-gi/game-of-life.git
git push -u origin main
```

GitHub Pages was then enabled under Settings > Pages, deploying from the `main` branch, root folder.

## License

MIT
