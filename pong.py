import Graphics
import Game
import Agent
import Input

# Initialize stuff
Graphics.initGraphics()
Game.initGame()

while True:
    Graphics.updateGraphics(None)
    Graphics.getPixelArray()
    Input.getInput()
    pass
