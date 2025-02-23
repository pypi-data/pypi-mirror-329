import sys # UNIX   
import platform # IDENTIFY PLATFORM
system = platform.system()
if system == "Linux" or system == "Darwin":
    import termios # UNIX
    import tty # UNIX
import time # GLOBAL
import os # GLOBAL
import select # UNIX
from typing import Type
if system == "Windows":
    import msvcrt # WINDOWS

def getInput():
    if system == "Linux" or system == "Darwin":
        """
        Main input getter for the engine.
        Designed principally for movement.
        input() is better for anything else except timeout.

        Returns:
            str: Single letter
        """
        # Save the terminal settings
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            # Change the terminal settings to raw mode (disable line buffering)
            tty.setraw(sys.stdin.fileno())
            # Read a single character from the input
            char = sys.stdin.read(1)
        finally:
            # Restore the original terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        return char
    
    else:
        """
        Main input getter for the engine.
        Designed principally for movement.
        input() is better for anything else except timeout.

        Returns:
            str: Single letter
        """

        return msvcrt.getch().decode()

def inputReceiver(timeout: float):
    """
    Makes the user only able to send a single letter
    in a certain amount of time.

    Args:
        timeout (float): Amount of time before dodging the user input

    Returns:
        str: Single letter user input
    """
    if system == "Linux" or system == "Darwin":
        # Save the original terminal settings
        original_settings = termios.tcgetattr(sys.stdin)
        try:
            # Set the terminal to raw mode to read single characters
            tty.setraw(sys.stdin)

            start_time = time.time()
            while time.time() - start_time < timeout:
                if select.select([sys.stdin], [], [], 0.1)[0]:  # Non-blocking check
                    char = sys.stdin.read(1)  # Read exactly one character
                    return char
        finally:
            # Restore the original terminal settings
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, original_settings)

    else:
        start_time = time.time()
        while time.time() - start_time < timeout:
            if msvcrt.kbhit():
                return msvcrt.getch().decode()

    return None  # Timeout

def typewriter(text: str, delay: int = 0.1):
    """
    Typewriter effect for dialogue.
    Preferably only used for that.
    WARNING, NOT TESTED IN WINDOWS.

    Args:
        text (str): The text you want to be written
        delay (float, optional): The amount of delay in which the letters will be written.. Defaults to 0.1.
    """
    for char in text:
        sys.stdout.write(char)  # Write each character without adding a newline
        sys.stdout.flush()  # Flush the output to display characters immediately
        time.sleep(delay)  # Wait for the specified delay
    print()  # Print a newline at the end

class Game():
    """
    Main class where the Game is gonna reside.
    Contains the board and borders.
    Need to be used for Player.

    Args:
        boardWidth (int): The game board width.
        boardHeight (int): The game board height.
        backgroundSprite (str, optional): The sprite for the background where no tile is placed.

    """
    def __init__(self, boardWidth: float, boardHeight: float, backgroundSprite="0"):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.backgroundSprite = backgroundSprite
        self.board = [[self.backgroundSprite for _ in range(boardWidth)] for _ in range(boardHeight)]


    def printBoard(self):
        """
        Prints the game board of the game in its latest stage.
        """
        for line in self.board:
            print(" ".join(line))


    def drawBorders(self, borders: list, borderSprite: str):
        """
        Used to make the game borders.
        Makes the process easier

        Args:
            borders (list): An array that contains the tuples which contain the positions of the borders.
            borderSprite (str): The sprite that the borders will use.
        """
        for x, y in borders:
            self.board[y][x] = borderSprite

class Entity():
    """

    Entity class that contains a possible movable character.
    Probably needed for almost everything that isn't still.

    Args:
        gameClass (Type): The root game object that is used to interact with the board.
        sprite (str): The entity's sprite.
        posX (int): Entity's x position.
        posY (int): Entity's y position.

    """
    def __init__(self, gameClass: Type, sprite: str, posX: int, posY: int):
        self.game = gameClass
        self.sprite = sprite
        self.posX = posX - 1
        self.posY = posY - 1

    def draw(self):
        """
        Adds the entity to the board.
        """
        self.game.board[self.posY][self.posX] = self.sprite

    #### MOVE DIRECTIONS

    def moveUp(self):
        """
        Moves the entity up into the array if nothing is there to block it.
        """
        if self.posY > 0:
            self.game.board[self.posY][self.posX] = self.game.backgroundSprite
            self.posY -= 1
            self.game.board[self.posY][self.posX] = self.sprite

    def moveDown(self):
        """
        Moves the entity down if nothing is there to block it.
        """
        if self.posY < len(self.game.board) - 1:
            self.game.board[self.posY][self.posX] = self.game.backgroundSprite
            self.posY += 1
            self.game.board[self.posY][self.posX] = self.sprite

    def moveLeft(self):
        """
        Moves the entity to the left if nothing is there to block it.
        """
        if self.posX > 0:
            self.game.board[self.posY][self.posX] = self.game.backgroundSprite
            self.posX -= 1
            self.game.board[self.posY][self.posX] = self.sprite
    
    def moveRight(self):
        """
        Moves the entity to the right if nothing is there to block.
        """
        if self.posX < len(self.game.board[0]) - 1:
            self.game.board[self.posY][self.posX] = self.game.backgroundSprite
            self.posX += 1
            self.game.board[self.posY][self.posX] = self.sprite

    ####! MOVE DIRECTIONS

    def detectCollision(self, sprite: str, newDir: str):
        """
        A collision detecter that checks collision in four different directions.

        Args:
            sprite (str): Is this sprite in the future square?
            newDir (str): Only accepts {w: up, s: down, a: left, d: right}

        Returns:
            _type_: returns True if it is gonna collide.
        """
        newDir = newDir.lower()
        if newDir == "w":
            if self.game.board[self.posY - 1][self.posX] == sprite:
                return True

        elif newDir == "s":
            if self.game.board[self.posY + 1][self.posX] == sprite:
                return True

        elif newDir == "a":
            if self.game.board[self.posY][self.posX - 1] == sprite:
                return True

        elif newDir == "d":
            if self.game.board[self.posY][self.posX + 1] == sprite:
                return True
            
class Rectangle():
    """
    Rectangle object class.

    Args:
        width (int): The width for the rectangle.
        height (int): The height for the game.
        root (Type): Game or root class that contains the Game() class.
        sprite (str): Sprite used for the borders and fill of the rectangle.
        posX (int): The top-left X position of the rectangle.


    """
    def __init__(self, width: int, height: int, root: Type, sprite: str, spriteFill: str, posX: int, posY: int, fill: bool = False):
        self.width = width
        self.height = height
        self.root = root
        self.sprite = sprite
        self.spriteFill = spriteFill
        self.posX = posX
        self.posY = posY
        self.fill = fill

    def draw(self):
        self.posX -= 1
        self.posY -= 1

        for y in range(self.posY, self.posY + self.height):
            for x in range(self.posX, self.posX + self.width):
                # Check if the current position is on the border or if the rectangle should be filled
                if self.fill or x == self.posX or x == self.posX + self.width - 1 or y == self.posY or y == self.posY + self.height - 1:
                    # Ensure the position is within the board boundaries
                    if 0 <= y < self.root.boardHeight and 0 <= x < self.root.boardWidth:
                        self.root.board[y][x] = self.sprite
                # Fill the interior if width and height are greater than 2 and there's a hole
                elif self.width > 2 and self.height > 2 and self.fill:
                    if 0 <= y < self.root.boardHeight and 0 <= x < self.root.boardWidth:
                        self.root.board[y][x] = self.spriteFill

        
