import random

# State list accessors
PLAYER_INPUT_INDX = 0
PLAYER_PREV_INPUT_INDX = 1
BALL_VELOCITY_INDX = 2
BALL_POSITION_INDX = 3
PADDLE_VELOCITY_INDX = 4
PADDLE_POSITION_INDX = 5
SCORE_PAUSE_TIMER_INDX = 6
CURRENT_STATE_INDX = 7
STATE_SWITCHED_INDX = 8
CURRENT_SCORE_INDX = 9


PADDLE_HEIGHT = 40
WINDOW_WIDTH = 600

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

    if random.random() < .1:
        action = 0

    return action

