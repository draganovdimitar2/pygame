# 🐍 Snake Game - Pygame Edition

Welcome to the Snake Game built using Python and Pygame! 🎮

## 🚀 Features

- Classic snake gameplay 🐍
- Smooth movement with arrow keys ⬆️⬇️⬅️➡️
- Randomized apple placement 🍏
- Score tracking 📊
- Pixel-perfect retro-style graphics 🎨
- Sound effects 🎵

## Installation

1. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. Install Pygame globally using pip:
   ```bash
   pip install pygame

3. Clone the repository:
    ```bash
    git clone https://github.com/draganovdimitar2/pygame.git
    ```
4. Navigate to the project directory:
    ```bash
    cd pygame
    ```
5. Run the game:
   ```bash
   python main.py
   ```

## 🎮 How to Play

- Use arrow keys (↑ ↓ ← →) to control the snake
- Collect apples to grow and increase score
- Avoid walls and self-collisions
- Game restarts automatically after collision

## 🛠️ Customization

Modify game parameters through these files:

- `settings.py`:
  ```python
  GRID_SIZE = 20
  GAME_SPEED = 10
  SCREEN_WIDTH = 640
  SCREEN_HEIGHT = 480

* Replace assets in /images folder
* Edit sound/crunch.wav for new eating sound

## 📜 Dependencies
* Python 3.7+
* Pygame 2.0+
* Random (Python built-in)
