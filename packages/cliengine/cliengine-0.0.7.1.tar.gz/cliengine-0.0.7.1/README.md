# CLI-Engine

A very simple game engine designed to run in the terminal. It works using tables.

## Example Usage

```python
import cliEngine

# Initialize the game with a 9x9 board
game = cliEngine.Game(9, 9)  # Width and Height.
game.printBoard()  # Prints the board.
```


# Changelog 0.0.7.1
- Minor changes.
- Added some description to the Rectangle.draw() function.
- Fixed a bug involving detectCollision()