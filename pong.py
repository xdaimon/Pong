import Game
import Graphics
import Agent
import Input

Graphics.initGraphics()
Game.initGame()

while True:
    # Update Game
    Game.setInputs([Input.getInput(), Agent.getAction(Game.getState())])
    Game.updateState()

    # Update Graphics
    Graphics.updateGraphics(Game.getState())

    # Update Agent
    # pixel_array = Graphics.getPixelArray()
    pass
