# Chess Game  ♔ 

### Demo Videos


https://github.com/user-attachments/assets/ded53088-ee85-40ea-b038-87047f0a9757


https://github.com/user-attachments/assets/c6df4633-202e-4b52-ac97-cd58df10263d


https://github.com/user-attachments/assets/b0185b0b-3d55-4ff0-bf15-21cd4d78879b



https://github.com/user-attachments/assets/09e1e7f8-4bd2-4077-a23e-ea9370f8459c


## Overview

A Python implementation of chess using Pygame with all standard rules including castling, pawn promotion,
check/checkmate detection, and move validation.

## Features

- **Complete chess rules**:
    - Castling (both kingside and queenside)
    - Pawn promotion
    - Check/checkmate detection
    - Legal move validation
- **Visual feedback**:
    - Move highlighting
    - Check indicators
    - Promotion menu
- **Audio feedback**:
    - Different sounds for moves, captures, and checks
- **Game management**:
    - Turn tracking
    - Captured pieces display
    - Game reset after checkmate

## Installation

1. Ensure you have Python installed on your system. You can download it
   from [python.org](https://www.python.org/downloads/).


2. Install Pygame globally using pip:
   ```bash
   pip install pygame
   ```

3. Clone the repository:
    ```bash
    git clone https://github.com/draganovdimitar2/pygame.git
    ```
4. Navigate to the project directory:
    ```bash
    cd pygame/chess
    ```
5. Run the game:
   ```bash
   python main.py
   ```

## Future Improvements

### Multiplayer & Networking
- [ ] **Online multiplayer support**  
  Plan to implement a client-server architecture using WebSockets or TCP sockets to enable online play.

### AI Enhancements
- [ ] **AI opponent with Minimax algorithm**  
  Future version will include an AI opponent using Minimax with Alpha-Beta pruning for optimal move selection.
- [ ] **Difficulty levels**  
  Configurable search depths to adjust AI difficulty (beginner to expert)

### Current Limitations
- Currently limited to local two-player gameplay
- No computer opponent available yet
   
