import random
from Constants import *

def getP2Position(state):
    return state[PADDLE_POSITION_INDX][1]


def getBallPosition(state):
    return state[BALL_POSITION_INDX]


def getAction(state):
    ball_y = getBallPosition(state)[1]
    ball_x = getBallPosition(state)[0]
    agent_y = getP2Position(state)[1]
    action = 0

    if ball_y > agent_y + PADDLE_HEIGHT//2:
        action = -1
    elif ball_y < agent_y - PADDLE_HEIGHT//2:
        action = 1

    if random.random() < .07:
        action = 0

    return action

