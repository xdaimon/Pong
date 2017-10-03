import numpy

import pygame, sys
from pygame.locals import *
import pygame.surfarray as surfarray

from Constants import *

# for controlling loop rate
fps = None
window = None


def getP1Score(state):
    return state[CURRENT_SCORE_INDX][0]


def getP2Score(state):
    return state[CURRENT_SCORE_INDX][1]


def initGraphics():
    global window, fps
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')
    fps = pygame.time.Clock()


def drawBoard():
    # Center line
    pygame.draw.line(window, BLACK, [CENTER_HORIZONTAL, 0],[CENTER_HORIZONTAL, WINDOW_HEIGHT], 1)


def rect(left, top, w, h):
    pygame.draw.rect(window, BLACK, [[left, top],[w, h]], 0)


def rectDel(left, top, w, h):
    pygame.draw.rect(window, WHITE, [[left, top],[w, h]], 0)


def drawZero(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left + FONT_STROKE, top + FONT_STROKE, FONT_WIDTH-FONT_STROKE*2, FONT_HEIGHT-FONT_STROKE*2)


def drawOne(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left, top, FONT_WIDTH-FONT_STROKE, FONT_HEIGHT)


def drawTwo(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left, top + FONT_STROKE, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)
    rectDel(left+FONT_STROKE, top + FONT_STROKE*4, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)


def drawThree(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left, top + FONT_STROKE, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)
    rectDel(left, top + FONT_STROKE*4, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)


def drawFour(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left+FONT_STROKE, top, FONT_WIDTH-FONT_STROKE*2, FONT_STROKE*3)
    rectDel(left, top+FONT_STROKE*4, FONT_WIDTH-FONT_STROKE, FONT_STROKE*4)


def drawFive(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left+FONT_STROKE, top + FONT_STROKE, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)
    rectDel(left, top + FONT_STROKE*4, FONT_WIDTH-FONT_STROKE, FONT_STROKE*2)


def drawSix(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left+FONT_STROKE, top, FONT_WIDTH-FONT_STROKE, FONT_STROKE*3.3)
    rectDel(left+FONT_STROKE, top + FONT_STROKE*4.3, FONT_WIDTH-FONT_STROKE*2, FONT_STROKE*2)


def drawSeven(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left, top+FONT_STROKE, FONT_WIDTH-FONT_STROKE, FONT_STROKE*7)


def drawEight(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left+FONT_STROKE, top+FONT_STROKE, FONT_WIDTH-FONT_STROKE*2, FONT_STROKE*1.8)
    rectDel(left+FONT_STROKE, top+FONT_STROKE*3.7, FONT_WIDTH-FONT_STROKE*2, FONT_STROKE*2.7)


def drawNine(left, top):
    rect(left, top, FONT_WIDTH, FONT_HEIGHT)
    rectDel(left+FONT_STROKE, top+FONT_STROKE, FONT_WIDTH-FONT_STROKE*2, FONT_STROKE*2)
    rectDel(left, top+FONT_STROKE*4, FONT_WIDTH-FONT_STROKE, FONT_STROKE*4)


def drawScores(state):
    p1_score = getP1Score(state)
    if p1_score == 0:
        drawZero(FONT_P1_X, FONT_Y)
    elif p1_score == 1:
        drawOne(FONT_P1_X, FONT_Y)
    elif p1_score == 2:
        drawTwo(FONT_P1_X, FONT_Y)
    elif p1_score == 3:
        drawThree(FONT_P1_X, FONT_Y)
    elif p1_score == 4:
        drawFour(FONT_P1_X, FONT_Y)
    elif p1_score == 5:
        drawFive(FONT_P1_X, FONT_Y)
    elif p1_score == 6:
        drawSix(FONT_P1_X, FONT_Y)
    elif p1_score == 7:
        drawSeven(FONT_P1_X, FONT_Y)
    elif p1_score == 8:
        drawEight(FONT_P1_X, FONT_Y)
    elif p1_score == 9:
        drawNine(FONT_P1_X, FONT_Y)

    p2_score = getP2Score(state)
    if p2_score == 0:
        drawZero(FONT_P2_X, FONT_Y)
    elif p2_score == 1:
        drawOne(FONT_P2_X, FONT_Y)
    elif p2_score == 2:
        drawTwo(FONT_P2_X, FONT_Y)
    elif p2_score == 3:
        drawThree(FONT_P2_X, FONT_Y)
    elif p2_score == 4:
        drawFour(FONT_P2_X, FONT_Y)
    elif p2_score == 5:
        drawFive(FONT_P2_X, FONT_Y)
    elif p2_score == 6:
        drawSix(FONT_P2_X, FONT_Y)
    elif p2_score == 7:
        drawSeven(FONT_P2_X, FONT_Y)
    elif p2_score == 8:
        drawEight(FONT_P2_X, FONT_Y)
    elif p2_score == 9:
        drawNine(FONT_P2_X, FONT_Y)


def drawCenteredRect(center, width, height):
    left = center[0] - width//2
    top = center[1] - height//2
    pygame.draw.rect(window, BLACK, pygame.Rect((left, top),(width, height)))


def drawBall(state):
    """
    Draws a square with edge length BALL_RADIUS centered at the ball's coordinates
    """

    center = state[BALL_POSITION_INDX]
    width = BALL_RADIUS
    height = BALL_RADIUS
    drawCenteredRect(center, width, height)


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


def updateGraphics(state):
    """
    Takes game state and updates the graphics accordingly
    Limits framerate
    """

    # Draw stuff
    window.fill(WHITE)
    drawBoard()
    drawPaddles(state)
    drawScores(state)
    drawBall(state)

    pygame.display.update()
    fps.tick(60)


def getPixelArray():
    """
    Returns a numpy array containing pixel values being either 0 or 1
    """

    # Just take all the red values, the agent only needs black and white images
    return surfarray.pixels3d(window)[:,:,0] // 255

