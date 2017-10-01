import numpy

import pygame, sys
from pygame.locals import *
import pygame.surfarray as surfarray

# for controlling loop rate
fps = None
window = None

# State list accessors
PLAYER_INPUT_INDX = 0
BALL_VELOCITY_INDX = 1
BALL_POSITION_INDX = 2
PADDLE_VELOCITY_INDX = 3
PADDLE_POSITION_INDX = 4
SCORE_PAUSE_TIMER_INDX = 5
CURRENT_STATE_INDX = 6
CURRENT_SCORE_INDX = 7

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40
BALL_RADIUS = PADDLE_WIDTH

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

CENTER_POINT = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
CENTER_VERTICAL = WINDOW_HEIGHT//2
CENTER_HORIZONTAL = WINDOW_WIDTH//2

WHITE = (255,255,255)
BLACK = (0,0,0)

def initGraphics():
    global window, fps
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')
    fps = pygame.time.Clock()
    pass

def drawBoard():
    # Center line
    pygame.draw.line(window, WHITE, [CENTER_HORIZONTAL, 0],[CENTER_HORIZONTAL, WINDOW_HEIGHT], 1)
    pass

def drawScores(state):
    pass

def drawCenteredRect(center, width, height):
    left = center[0] - width//2
    top = center[1] - height//2
    pygame.draw.rect(window, WHITE, pygame.Rect((left, top),(width, height)))
    pass

def drawBall(state):
    """
    Draws a square with edge length BALL_RADIUS centered at the ball's coordinates
    """

    center = state[BALL_POSITION_INDX]
    width = BALL_RADIUS
    height = BALL_RADIUS
    drawCenteredRect(center, width, height)
    pass

def drawPaddles(state):
    """
    Draws a rectangle centered at the paddle's coordinates
    """

    # Player 1's paddle
    center = state[PADDLE_POSITION_INDX][0]
    width = PADDLE_WIDTH
    height = PADDLE_HEIGHT
    drawCenteredRect(center, width, height)

    # Player 2's paddle
    center = state[PADDLE_POSITION_INDX][1]
    width = PADDLE_WIDTH
    height = PADDLE_HEIGHT
    drawCenteredRect(center, width, height)
    pass

def updateGraphics(state):
    """
    Takes game state and updates the graphics accordingly
    Limits framerate
    """

    # Draw stuff
    window.fill(BLACK)
    drawBoard()
    drawBall(state)
    drawPaddles(state)

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
