input_indx = 0
ball_velocity_indx = 1
ball_position_indx = 2
paddle_position_indx = 3
paddle_velocity_indx = 4
paused_timer_indx = 5
current_state_indx = 6

state = []

def resetStateList():
    pass

# State list accessors
# inputs = 0
# ball_velocity = 1
# ball_position = 2
# ...

def setInputs(players_input):
    """
    players_input is a list of ints that indicate which action the nth player 
    wants to take

    -1 : move left
    0  : stop
    1  : move right

    if the nth player wants to move right then
    players_input[n] == 1

    """
    pass

def updatePlayState():
    pass

def updateScoreState():
    pass

def updateEndState():
    pass

def updateState():

    ####### State #######

    # score

    # ball velocity
    # ball position

    # paddle positions
    # paddle velocities

    # pause game timer

    ####### Update #######

    # if in play_state
    #     Update velocities
    #     Update positions
    #     Check for collisions
    #     If collisions, then change velocities
    #     Check if ball entered score zone
    #     If ball entered score zone, then enter score_state
    # elif in score_state
    #     if entering state
    #         reset ball to center 
    #         update scores
    #         check end game
    #         if end game
    #             enter end_state
    #         else
    #             start ball launch timer
    #     elif game_pause_timer done
    #         launch ball 
    #         enter play_state
    # elif in end_state
    #     if user is moving paddle
    #         resetStateList()
    #         set ball initial velocity
    #         enter play_state
    #       

    pass

def getState():
    return state
