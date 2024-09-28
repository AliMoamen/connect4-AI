

# Connect4 with Minimax AI

This repository contains a Python implementation of the classic Connect4 game, enhanced with a Minimax AI algorithm with optional Alpha-Beta pruning. The AI opponent can be configured with various difficulty levels, which affects its decision-making process.

## Features

- **Connect4 Game Logic:** The core logic to handle player turns, check for valid moves, detect game outcomes (win/loss/draw), and display the game board.
- **Minimax Algorithm:** Implements the Minimax algorithm for AI move selection, ensuring the AI makes optimal moves.
- **Alpha-Beta Pruning:** Optionally enables Alpha-Beta pruning for faster AI decision-making by reducing the number of nodes evaluated in the Minimax tree.
- **AI Difficulty Levels:** Choose between `Easy`, `Medium`, and `Hard` difficulty levels for the AI, with higher difficulty resulting in more optimal play.

## File Overview

### `connect4.py`
This file contains the main game logic for the Connect4 game, including:
- Game initialization and loop handling player moves.
- AI logic based on the Minimax algorithm with optional Alpha-Beta pruning.
- Functions to check for win conditions, draw, and valid moves.
- Utility functions to handle user input and drawing the game board using Pygame.

### `benchmark.py`
This file seems to include benchmarking functionalities, measuring the performance of different algorithms (such as the time taken for Minimax to evaluate moves). This file likely tracks AI decision times, the number of nodes evaluated, and other relevant metrics.

## Getting Started

### Prerequisites

- **Python 3.7+**
- **Pygame Library**

Install Pygame using the following command:

```bash
pip install pygame
```

### Running the Game

You can start a game by running the following command:

```bash
python connect4.py
```

### Configuring the AI Difficulty

The difficulty of the AI can be changed when initializing the game. The available difficulty levels are `Easy`, `Medium`, and `Hard`. For example:

```python
game = Connect4(aiplayer2_difficulty='Hard')
```

The AI will then make decisions based on the set difficulty level.

## Benchmarking

The `benchmark.py` script allows you to evaluate the performance of the AI with the Minimax algorithm. It measures key metrics such as execution time and the number of nodes evaluated during AI decision-making.

---
