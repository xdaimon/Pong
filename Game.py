import math
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
CURRENT_SCORE_INDX = 8

# game states
END_STATE = 0
PLAY_STATE = 1
SCORE_STATE = 2

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40
BALL_RADIUS = PADDLE_WIDTH

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

CENTER_POINT = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
CENTER_VERTICAL = WINDOW_HEIGHT//2
CENTER_HORIZONTAL = WINDOW_WIDTH//2

# Bounds for the paddle, they are set such that when the paddle is at the
# BOARD_TOP|BOTTOM_EDGE then the edge of the paddle touches the edge of the window.
# Therefore it is safe to set the paddle's position to one of these values
BOARD_WIDTH = WINDOW_WIDTH - 8*PADDLE_WIDTH
BOARD_HEIGHT = WINDOW_HEIGHT - PADDLE_HEIGHT

BOARD_LEFT_EDGE = (WINDOW_WIDTH - BOARD_WIDTH)//2
BOARD_RIGHT_EDGE = BOARD_LEFT_EDGE + BOARD_WIDTH
BOARD_TOP_EDGE = (WINDOW_HEIGHT - BOARD_HEIGHT)//2
BOARD_BOTTOM_EDGE = BOARD_TOP_EDGE + BOARD_HEIGHT

# Pause for two second after each score
PAUSE_DURATION = 2000

# Per second speeds
SECOND_TO_FRAME = 1/60
BALL_INIT_SPEED = WINDOW_WIDTH/4
PADDLE_MAX_SPEED = BALL_INIT_SPEED/8
PADDLE_BASE_SPEED = BALL_INIT_SPEED/16
PADDLE_ACCEL = (PADDLE_MAX_SPEED-PADDLE_BASE_SPEED)/.8


state = []

"""
Details/Notes

Rect positions.
Let the position of the paddles be at the center point of the paddle
Same for the ball

Timers.
I will need a timer to create a short pause after each score.
During this pause the game will be in SCORE_STATE where the ball is stationary
at the center of the screen.
So I will need to set the timer in the state list to be a millisecond value. I
will watch for when a certain amount of time has passed relative to the
millisecond value in the state list.

Velocities.
Velocity variables in state are deltas to be used to update positions per frame
(assuming 60fps)

Paddle Movements
Paddles move at PADDLE_BASE_SPEED
but they also accellerate in each frame up until PADDLE_MAX_SPEED
I imagine that a linear interpolation will work fine
Paddles accelerate at a constant (PADDLE_MAX_SPEED-PADDLE_BASE_SPEED) per 800 ms
Paddles deaccelerate instantly, so if player input is zero (i.e. STOP) then the
paddles velocity is set to zero
"""

def initGame():
    """
    Constructs the state list
    Puts game into initial state (end state)
    """

    # Must append in this order to preserve INDX constant's correctness

    # player input, no paddle movements
    state.append([0,0])
    # player prev input, no paddle movements
    state.append([0,0])
    # ball velocity, initially stationary
    state.append([0,0])
    # ball position, initially at origin
    state.append(CENTER_POINT)
    # paddle velocities, no paddle movements
    state.append([[0,0],[0,0]])
    # paddle positions
    state.append([[BOARD_LEFT_EDGE, CENTER_VERTICAL], [BOARD_RIGHT_EDGE, CENTER_VERTICAL]])
    # score pause timer, inital value is arbitrary
    state.append(0)
    # initial state, so that any user input starts the game
    state.append(END_STATE)
    # player's score
    state.append([0,0])
    pass


def resetStateList():
    state = []
    initGame()


def setPrevInputs(new):
    state[PLAYER_PREV_INPUT_INDX] = new


def setInputs(players_input):
    """
    players_input is a list of n ints that indicate which action the nth player
    wants to take

    -1 : move left
     0 : stop
     1 : move right

    if the nth player wants to move right then
    players_input[n] == 1

    """
    state[PLAYER_INPUT_INDX] = players_input
    pass


def directionForTheta(theta):
    return [math.cos(theta), math.sin(theta)]


def vectorAdd(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]


def vectorSub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]


def vectorScalMul(v, s):
    return [v[0] * s, v[1] * s]


def vectorClamp(v, vmin, vmax):
    if v[0] < vmin[0]:
        v[0] = vmin[0]
    if v[1] < vmin[1]:
        v[1] = vmin[1]
    if v[0] > vmax[0]:
        v[0] = vmax[0]
    if v[1] > vmax[1]:
        v[1] = vmax[1]
    return v


def vectorLength(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])


def vectorMagClamp(v, speed_max):
    vlength = vectorLength(v)
    if vlength > speed_max:
        v = vectorScalMul(v, speed_max/vlength)
    return v


def checkCollision(rect1, rect2):
    """
    rect1 == (centerx,centery,width,height)
    rect2 is like rect1
    """
    pass


def getP1PrevInput():
    return state[PLAYER_PREV_INPUT_INDX][0]


def getP2PrevInput():
    return state[PLAYER_PREV_INPUT_INDX][1]


def setCurrentState(new):
    state[CURRENT_STATE_INDX] = new


def getCurrentState():
    return state[CURRENT_STATE_INDX]


def setBallVelocity(new):
    state[BALL_VELOCITY_INDX] = new


def setP1Velocity(new):
    state[PADDLE_VELOCITY_INDX][0] = new


def setP2Velocity(new):
    state[PADDLE_VELOCITY_INDX][1] = new


def setP1Position(new):
    state[PADDLE_POSITION_INDX][0] = new


def setP2Position(new):
    state[PADDLE_POSITION_INDX][1] = new


def getP1Input():
    return state[PLAYER_INPUT_INDX][0]


def getP2Input():
    return state[PLAYER_INPUT_INDX][1]


def getP1Velocity():
    return state[PADDLE_VELOCITY_INDX][0]


def getP2Velocity():
    return state[PADDLE_VELOCITY_INDX][1]


def getP1Position():
    return state[PADDLE_POSITION_INDX][0]


def getP2Position():
    return state[PADDLE_POSITION_INDX][1]


def updatePaddles():

    p1_velocity = getP1Velocity()
    p1_input = getP1Input()
    # Is the identity, stops, or negates vel direction cooresponding to user input
    p2_velocity = getP2Velocity()
    p2_input = getP2Input()

    # If velocities changed we need to either zero them or negate them
    if p1_input != getP1PrevInput():
        p1_velocity = vectorScalMul(p1_velocity, p1_input)
    if p2_input != getP2PrevInput():
        p2_velocity = vectorScalMul(p2_velocity, p2_input)

    # Apply acceleration
    # Because window coords are silly we have to accel in the oppossite direction
    speed_increment = -p1_input * PADDLE_ACCEL * SECOND_TO_FRAME
    p1_velocity[1] += p1_velocity[1]+speed_increment
    speed_increment = -p2_input * PADDLE_ACCEL * SECOND_TO_FRAME
    p2_velocity[1] += p2_velocity[1]+speed_increment

    # Clamp velocities to max speeds
    p1_velocity = vectorMagClamp(p1_velocity, PADDLE_MAX_SPEED)
    p2_velocity = vectorMagClamp(p2_velocity, PADDLE_MAX_SPEED)

    # Update positions for velocities
    p1_position = getP1Position()
    # p1_velocity = vectorScalMul(p1_velocity, SECOND_TO_FRAME)
    p1_position = vectorAdd(p1_position, p1_velocity)
    p2_position = getP2Position()
    p2_velocity = vectorScalMul(p2_velocity, SECOND_TO_FRAME)
    p2_position = vectorAdd(p2_position, p2_velocity)

    # Clamp positions
    # remember that window coords are silly
    miny = BOARD_TOP_EDGE
    maxy = BOARD_BOTTOM_EDGE
    minx = BOARD_LEFT_EDGE
    maxx = BOARD_RIGHT_EDGE
    p1_position = vectorClamp(p1_position, [minx, miny], [maxx, maxy])
    p2_position = vectorClamp(p2_position, [minx, miny], [maxx, maxy])

    setP1Position(p1_position)
    setP2Position(p2_position)
    setP1Velocity(p1_velocity)
    setP2Velocity(p2_velocity)

    setPrevInputs([p1_input, p2_input])


def updatePlayState():
    # print("in play state")

    # Update paddle velocities for inputs
    updatePaddles()
    # Check for ball/paddle collisions
    # If collisions, then change ball velocity
    # Check if ball entered score zone
    # If ball entered score zone, then enter score_state

    pass


def updateScoreState():
    print("in score state")
    # if entering score_state
    #     reset ball to center
    #     set ball velocity to zero
    #     update scores
    #     check end game
    #     if end game
    #         enter end_state
    #     else
    #         start score pause timer
    # elif score pause timer
    #     launch ball
    #     enter play_state
    pass


def updateEndState():
    # print("in end state")

    p1_input = state[PLAYER_INPUT_INDX][0]
    if p1_input != 0:
        resetStateList()
        setCurrentState(PLAY_STATE)
        new_vel = directionForTheta(2*math.pi*random.random())
        vectorScalMul(new_vel, BALL_INIT_SPEED)
        setBallVelocity(new_vel)

    pass

def updateState():

    if getCurrentState() == PLAY_STATE:
        updatePlayState()
    elif getCurrentState() == SCORE_STATE:
        updateScoreState()
    elif getCurrentState() == END_STATE:
        updateEndState()

    pass


def getState():
    return state

