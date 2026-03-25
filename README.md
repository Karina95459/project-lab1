# Arkanoid

A Python implementation of the classic **Arkanoid** arcade game using the `pygame` library. The project was developed by a team of 4 as part of an Object-Oriented Programming lab assignment.

---

## Table of Contents

- [About the Game](#about-the-game)
- [Controls](#controls)
- [Installation & Running](#installation--running)
- [Project Structure](#project-structure)
- [Class Descriptions](#class-descriptions)
- [UML Diagrams](#uml-diagrams)
- [Authors](#authors)

---

## About the Game

The player controls a paddle at the bottom of the screen and bounces a ball to destroy all the bricks at the top. If the ball falls below the paddle — the game is lost. If all bricks are destroyed — the player wins.

---

## Controls

| Key | Action |
|-----|--------|
| `←` / `A` | Move paddle left |
| `→` / `D` | Move paddle right |
| `P` | Pause / Resume |
| `R` | Restart the game |
| `ESC` | Quit |

---

## Installation & Running

**Requirements:** Python 3.10+, pygame

```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

## Project Structure

```
project-lab1/
├── main.py           # Entry point
├── game.py           # Main game loop
├── ball.py           # Ball class
├── platform.py       # Platform (paddle) class
├── brick.py          # Single brick class
├── brick_manager.py  # Brick grid management
└── score_manager.py  # Score management
```

---

## Class Descriptions

### `Game`
The main class responsible for the game loop. Initializes all game objects, handles keyboard events, updates game state, and renders each frame. Manages the following states: `is_running`, `is_paused`, `is_game_over`, `is_win`.

### `Ball`
The ball that moves around the screen. Stores current position, radius, and velocity vector (`dx`, `dy`). Handles its own movement, bouncing off walls and the paddle, and detecting when it goes out of bounds.

### `Platform`
The paddle controlled by the player. Moves horizontally and is constrained within screen boundaries via the `clamp()` method. Used to reflect the ball back upward.

### `Brick`
A single brick in the grid. Has coordinates, dimensions, and an `is_destroyed` flag. Renders itself only when not destroyed.

### `BrickManager`
Manages the entire brick grid: creates the level (`create_level`), draws all bricks, checks ball-brick collisions (`check_collision`), and determines whether the player has won (`all_destroyed`).

### `ScoreManager`
Handles the player's score. Tracks both the current score and the high score (`high_score`). Renders the score on screen during gameplay.

---

## UML Diagrams

### Use Case Diagram

![Use Case](docs/usecase_diagram.png)

The player can: start the game, pause, restart, quit, and control the paddle. Controlling the paddle includes reflecting the ball, which in turn leads to breaking bricks and earning points.

### Class Diagram

![Class Diagram](docs/class_diagram.png)

`Game` aggregates `Ball`, `Platform`, and `BrickManager`. `BrickManager` holds a list of `Brick` objects. `ScoreManager` is responsible for tracking and displaying the score.

### Activity Diagram

![Activity Diagram](docs/activity_diagram.png)

After object initialization, the game enters the main loop: handle events → move paddle and ball → check collisions → check win condition → render frame. The loop continues as long as the game is active.

---

## Authors

| Name | GitHub | Contribution |
|------|--------|--------------|
| Karina Lukiianova | [@Karina95459](https://github.com/Karina95459) | Game, class skeletons for all classes, class diagram |
| Polina Onipchuk | [@jewrlly](https://github.com/jewrlly) | BrickManager, Brick, skeletons for changes, use case diagram |
| Kateryna Pavlenko | [@katepvlnk](https://github.com/katepvlnk) | Platform, ScoreManager, README |
| Artem Semeniuk | [@Bio5648](https://github.com/Bio5648)| Ball, activity diagram |