# CLI-Engine

A very simple game engine designed to run in the terminal. It works using tables.

## Example Usage

```python
import cliEngine

# Initialize the game with a 9x9 board
game = cliEngine.Game(9, 9)  # Width and Height.
game.printBoard()  # Prints the board.
```

## As I am still writing the docs, here is a full game with movement.
```python
import cliEngine # change this in readme.md
import os

game = cliEngine.Game(9, 9)
player = cliEngine.Player(game, "1", 5, 5) # game class, player sprite, and pos x and y
borderCoordinates = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (0, 1), (8, 1), (0, 2), (8, 2), (0, 3), (8, 3), (0, 4), (8, 4), (0, 5), (8, 5), (0, 6), (8, 6), (0, 7), (8, 7), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
# very long useless line for the coordinates, sadly it is how it is

def gameLoop():
    os.system("clear") # UNIX SYSTEMS ONLY COMMAND
    game.drawBorders(borderCoordinates, "2")
    player.draw()
    game.printBoard()
    userInput = cliEngine.getInput()
    if player.detectCollision("2", userInput):
        pass
    else:
        player.move(userInput)

if __name__ == "__main__":
    while True:
        gameLoop()
```

# Changelog 0.0.5
- So umm, I broke the entire code so I reestructured it with DeepSeek.
- I hope everything works, so I finally added something to __init__.py