import numpy

import pygame, sys
from pygame.locals import *
import pygame.surfarray as surfarray

# for controlling loop rate
fps = None
window = None

WIDTH = 600
HEIGHT = 400
CENTER = [WIDTH//2, HEIGHT//2]

WHITE = (255,255,255)
BLACK = (0,0,0)

def initGraphics():
    global window, fps
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')
    fps = pygame.time.Clock()
    pass

def drawBoard():
    pygame.draw.line(window, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pass

def drawScores(state):
    pass

def drawBall(state):
    pygame.draw.circle(window, WHITE, CENTER, 20, 0)
    pass

def drawPaddles(state):
    pass

def updateGraphics(state):
    """
    Takes game state and updates the graphics accordingly
    Limits framerate
    """

    # Draw stuff
    window.fill(BLACK)
    drawBall(state)

    pygame.display.update()
    fps.tick(60)
    pass

def getPixelArray():
    """
    Returns a numpy array containing pixel values being either 0 or 1
    """

    # Just take all the red values, the agent only needs black and white images
    # arr = surfarray.pixels3d(window)[:,:,0]

    pass
