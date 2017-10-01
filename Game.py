import math

# State list accessors
PLAYER_INPUT_INDX = 0
BALL_VELOCITY_INDX = 1
BALL_POSITION_INDX = 2
PADDLE_VELOCITY_INDX = 3
PADDLE_POSITION_INDX = 4
SCORE_PAUSE_TIMER_INDX = 5
CURRENT_STATE_INDX = 6
CURRENT_SCORE_INDX = 7

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

# Per second speed
BALL_INIT_SPEED = WINDOW_WIDTH//4
VELOCITY_TO_DELTA = 1/60

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
"""

def initGame():
    """
    Constructs the state list
    Puts game into initial state (end state)
    """

    # Must append in this order to preserve INDX constant's correctness

    # player input, no paddle movements
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
    pass


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
    return [v1[0] * s, v2[1] * s]


def checkCollision(rect1, rect2):
    """
    rect1 == (centerx,centery,width,height)
    rect2 is like rect1
    """
    pass


def setCurrentState(new_state):
    state[CURRENT_STATE_INDX] = new_state


def getCurrentState():
    return state[CURRENT_STATE_INDX]


def setBallVelocity(new_vel):
    state[BALL_VELOCITY_INDX] = new_vel


def updatePlayState():
    print("in play state")
    # Update velocities
    # Update positions
    # Check for collisions
    # If collisions, then change velocities
    # Check if ball entered score zone
    # If ball entered score zone, then enter score_state
    pass


def updateScoreState():
    print("in score state")
    # if entering state
    #     reset ball to center
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
    print("in end state")
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

