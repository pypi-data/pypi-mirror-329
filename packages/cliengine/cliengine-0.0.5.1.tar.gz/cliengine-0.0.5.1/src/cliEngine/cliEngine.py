import sys
import platform
system = platform.system()
if system == "Linux" or system == "Darwin":
    import termios
    import tty
import time
import os
import select
if system == "Windows":
    import msvcrt

def getInput():
    if system == "Linux" or system == "Darwin":
        """

        Returns the input from a user,
        only a letter that it will auto-enter

        :returns a letter:
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
        Returns the input from a user, only a letter that it will auto-enter.

        :returns: a letter
        """

        return msvcrt.getch().decode()

def inputReceiver(timeout):
    """
    
    Allows the user to make an input in a certain amount of
    time.

    :returns: a letter
    
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

def typewriter(text, delay=0.1):
    """
    Prints text with a typewriter effect.

    Parameters:
        text (str): The text to display.
        delay (float): The delay between each character in seconds. Default is 0.1.
    """
    for char in text:
        sys.stdout.write(char)  # Write each character without adding a newline
        sys.stdout.flush()  # Flush the output to display characters immediately
        time.sleep(delay)  # Wait for the specified delay
    print()  # Print a newline at the end

class Game():
    """
    Initializes the main object that will
    allow the player and characters to reside.
    """
    def __init__(self, boardWidth, boardHeight):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.board = [["0" for _ in range(boardWidth)] for _ in range(boardHeight)]

    def printBoard(self):
        """

        Prints the board.

        """
        for line in self.board:
            print(" ".join(line))


    def drawBorders(self, borders, borderSprite):
        for x, y in borders:
            self.board[y][x] = borderSprite

class Player():
    def __init__(self, gameClass, sprite, posX, posY):
        self.game = gameClass
        self.sprite = sprite
        self.posX = posX
        self.posY = posY

    def draw(self):
        self.game.board[self.posY][self.posX] = self.sprite

    def move(self, dir):
        if (dir == "w" or dir == "W") and self.posY > 0:  # Fixed condition for "w"
            self.game.board[self.posY][self.posX] = "0"
            self.posY -= 1
            self.game.board[self.posY][self.posX] = self.sprite

        elif (dir == "s" or dir == "S") and self.posY < len(self.game.board) - 1:  # Restrict "s" to bottom boundary
            self.game.board[self.posY][self.posX] = "0"
            self.posY += 1
            self.game.board[self.posY][self.posX] = self.sprite

        elif (dir == "a" or dir == "A") and self.posX > 0:  # Restrict "a" to left boundary
            self.game.board[self.posY][self.posX] = "0"
            self.posX -= 1
            self.game.board[self.posY][self.posX] = self.sprite

        elif (dir == "d" or dir == "D") and self.posX < len(self.game.board[0]) - 1:  # Restrict "d" to right boundary
            self.game.board[self.posY][self.posX] = "0"
            self.posX += 1
            self.game.board[self.posY][self.posX] = self.sprite

    def detectCollision(self, sprite, newDir):
        if newDir == "w" or newDir == "W":
            if self.game.board[self.posY - 1][self.posX] == sprite:
                return True

        elif newDir == "s" or newDir == "S":
            if self.game.board[self.posY + 1][self.posX] == sprite:
                return True

        elif newDir == "a" or newDir == "A":
            if self.game.board[self.posY][self.posX - 1] == sprite:
                return True

        elif newDir == "d" or newDir == "D":
            if self.game.board[self.posY][self.posX + 1] == sprite:
                return True
            
class Specials():
    def __init__(self, gameClass, sprite, posX, posY, type, playerClass):
        self.game = gameClass
        self.sprite = sprite
        self.posX = posX
        self.posY = posY
        self.type = type
        self.playerClass = playerClass

    def draw(self):
        self.game.board[self.posY][self.posX] = self.sprite

    def changeSprite(self):
        newIntS = int(self.sprite)
        newIntP = int(self.playerClass.sprite)

        return str(newIntS + newIntP)

    def dialogue(self, dial):
        typewriter(dial)

    def teleport(self, func):
        os.system("clear")
        func()