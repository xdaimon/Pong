import Graphics
import Game
import Agent
import Input

# Initialize stuff
Graphics.initGraphics()

while True:
    Graphics.updateGraphics(None)
    Graphics.getPixelArray()
    Input.getInput()
    pass
