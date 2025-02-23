import cliTestEngine as cliEngine
import os
def clear():
    os.system("clear")
class Game():
    def __init__(self):
        self.width = 9
        self.height = 9
        self.root = cliEngine.Game(self.width, self.height)
        self.player = cliEngine.Entity(self.root, "1", 3, 3)
        self.rectangle = cliEngine.Rectangle(3, 3, self.root, "2", "2", 7, 7, fill=True)
        self.borderList = [(1, 1)]
    def loop(self):
        self.rectangle.draw()
        while True:
            clear()
            self.root.drawBorders(self.borderList, "2")
            self.player.draw()
            self.root.printBoard()
            
            userInput = cliEngine.getInput()
            # collision detect.
            if self.player.detectCollision("2", userInput):
                continue
            else:
                pass
            # player movement
            if userInput == "w":
                self.player.moveUp()
            elif userInput == "s":
                self.player.moveDown()
            elif userInput == "a":
                self.player.moveLeft()
            elif userInput == "d":
                self.player.moveRight()
    def main(self):
        self.loop()

game = Game(); game.main()