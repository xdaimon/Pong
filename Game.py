import math
import random
import pygame

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
PAUSE_DURATION = 0

# Per second speeds
SECOND_TO_FRAME = 1/60
BALL_INIT_SPEED = WINDOW_WIDTH/2
PADDLE_MAX_SPEED = WINDOW_WIDTH/50
PADDLE_BASE_SPEED = WINDOW_WIDTH/80
PADDLE_ACCEL = (PADDLE_MAX_SPEED-PADDLE_BASE_SPEED)

MAX_SCORE = 9


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
    # did we just switch states?
    state.append(False)
    # player's score
    state.append([0,0])


def resetStateList():
    del state[:]
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


def vectorDot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]


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


def getStateSwitched():
    return state[STATE_SWITCHED_INDX]


def setStateSwitched(new):
    state[STATE_SWITCHED_INDX] = new


def getP1PrevInput():
    return state[PLAYER_PREV_INPUT_INDX][0]


def getP2PrevInput():
    return state[PLAYER_PREV_INPUT_INDX][1]


def setCurrentState(new):
    setStateSwitched(True)
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


def getBallVelocity():
    return state[BALL_VELOCITY_INDX]


def getBallPosition():
    return state[BALL_POSITION_INDX]


def setBallPosition(new):
    state[BALL_POSITION_INDX] = new


def incrementP1Score():
    state[CURRENT_SCORE_INDX][0] += 1


def incrementP2Score():
    state[CURRENT_SCORE_INDX][1] += 1


def getP1Score():
    return state[CURRENT_SCORE_INDX][0]


def getP2Score():
    return state[CURRENT_SCORE_INDX][1]


def setPausedTime(new):
    state[SCORE_PAUSE_TIMER_INDX] = new


def getPausedTime():
    return state[SCORE_PAUSE_TIMER_INDX]


def pyRectForCenterAndSize(c, s):
    top = c[1] - s[1]/2
    left = c[0] - s[0]/2
    return pygame.Rect([ (left, top), s ])


# TODO the paddle changes the velocity of the ball


def updateBall():
    vel = getBallVelocity()
    pos = getBallPosition()
    pos = vectorAdd(pos, vel)
    miny = 0
    maxy = WINDOW_HEIGHT
    minx = 0
    maxx = WINDOW_WIDTH
    pos = vectorClamp(pos, [minx, miny], [maxx, maxy])

    # Check for ball/paddle collisions
    rect1 = pyRectForCenterAndSize(pos, (BALL_RADIUS,BALL_RADIUS))
    rect2 = pyRectForCenterAndSize(getP1Position(), (PADDLE_WIDTH, PADDLE_HEIGHT))
    # If collision, then change ball velocity
    if rect1.colliderect(rect2):
        vel = getBallVelocity()
        vel = [-vel[0], vel[1]]
        setBallVelocity(vel)
        # Move the ball away from the paddle a bit
        pos = vectorAdd(pos, [4,0])

    rect2 = pyRectForCenterAndSize(getP2Position(), (PADDLE_WIDTH, PADDLE_HEIGHT))
    if rect1.colliderect(rect2):
        vel = getBallVelocity()
        setBallVelocity([-vel[0], vel[1]])
        pos = vectorAdd(pos, [-4,0])

    # Check for ball/wall collisions
    if pos[1] == 0 or pos[1] == WINDOW_HEIGHT:
        vel = getBallVelocity()
        setBallVelocity([vel[0], -vel[1]])

    # Check if ball entered score zone
    # If ball entered score zone, then enter score_state
    if didScore(pos[0]):
        setCurrentState(SCORE_STATE)

    setBallPosition(pos)


def updatePaddles():

    p1_velocity = getP1Velocity()
    p1_input = getP1Input()
    # Is the identity, stops, or negates vel direction cooresponding to user input
    p2_velocity = getP2Velocity()
    p2_input = getP2Input()

    # If velocities changed we need to either zero them or negate them
    # if p1_input != getP1PrevInput():
    #     p1_velocity = vectorScalMul(p1_velocity, p1_input)
    # if p2_input != getP2PrevInput():
    #     p2_velocity = vectorScalMul(p2_velocity, p2_input)

    # Apply acceleration
    # Because window coords are silly we have to accel in the oppossite direction
    speed_increment = 0
    if p1_input > 0:
        speed_increment = -PADDLE_ACCEL * SECOND_TO_FRAME
        if p1_velocity[1] > 0:
            p1_velocity[1] *= -1
    elif p1_input < 0:
        speed_increment = PADDLE_ACCEL * SECOND_TO_FRAME
        if p1_velocity[1] < 0:
            p1_velocity[1] *= -1
    else:
        p1_velocity = [0,0]
    p1_velocity[1] += p1_velocity[1]+speed_increment
    speed_increment = 0
    if p2_input > 0:
        speed_increment = -PADDLE_ACCEL * SECOND_TO_FRAME
        if p2_velocity[1] > 0:
            p2_velocity[1] *= -1
    elif p2_input < 0:
        speed_increment = PADDLE_ACCEL * SECOND_TO_FRAME
        if p2_velocity[1] < 0:
            p2_velocity[1] *= -1
    else:
        p2_velocity = [0,0]
    p2_velocity[1] += p2_velocity[1]+speed_increment

    # Clamp velocities to max speeds
    p1_velocity = vectorMagClamp(p1_velocity, PADDLE_MAX_SPEED)
    p2_velocity = vectorMagClamp(p2_velocity, PADDLE_MAX_SPEED)

    # Update positions for velocities
    p1_position = getP1Position()
    p1_position = vectorAdd(p1_position, p1_velocity)
    p2_position = getP2Position()
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


def didScore(x):
    if x < 0.1:
        return True
    elif x > WINDOW_WIDTH-.1:
        return True
    return False


def updatePlayState():
    if getStateSwitched():
        print("PlayState")
        # restrict theta to +-pi/4 or pi +- pi/4
        rand = random.random()
        theta = math.pi/4 * (rand*2-1) + math.pi
        if rand > .5:
            theta += math.pi
        new_vel = directionForTheta(theta)
        new_vel = vectorScalMul(new_vel, SECOND_TO_FRAME*BALL_INIT_SPEED)
        setBallVelocity(new_vel)
        setStateSwitched(False)

    updatePaddles()
    updateBall()


def updateScoreState():
    if getStateSwitched():
        print("ScoreState")
        pos = getBallPosition()
        if pos[0] < WINDOW_WIDTH//2:
            # Score agains P1
            incrementP2Score()
        else:
            # Score agains P2
            incrementP1Score()
        setBallPosition(CENTER_POINT)
        setBallVelocity([0,0])
        if getP1Score() == MAX_SCORE or getP2Score() == MAX_SCORE:
            setCurrentState(END_STATE)
        else:
            setPausedTime(pygame.time.get_ticks())
            setStateSwitched(False)
        print(getP1Score(), " ", getP2Score())
    elif pygame.time.get_ticks() - getPausedTime() > PAUSE_DURATION:
        setCurrentState(PLAY_STATE)

    # We still let the user move the paddles
    updatePaddles()


def updateEndState():
    if getStateSwitched():
        print("EndState")
        resetStateList()
        setStateSwitched(False)

    p1_input = getP1Input()
    if p1_input != 0:
        setCurrentState(PLAY_STATE)


def updateState():
    if getCurrentState() == PLAY_STATE:
        updatePlayState()
    elif getCurrentState() == SCORE_STATE:
        updateScoreState()
    elif getCurrentState() == END_STATE:
        updateEndState()


def getState():
    return state

