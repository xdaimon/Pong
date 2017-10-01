import pygame, sys

"""
Returns these values

-1 : move left
 0 : stop
 1 : move right
"""

LEFT = -1
STOP = 0
RIGHT = 1

keys_down = 0
previous_input = STOP

def keyDown(e):
    """
    Switch through movement keys to see which is pressed
    """
    global keys_down

    if e.key == pygame.K_LEFT:
        keys_down += 1
        return RIGHT
    elif e.key == pygame.K_RIGHT:
        keys_down += 1
        return LEFT
    else:
        return previous_input


def keyUp(e):
    """
    Switch through movement keys to see which is released
    """
    global keys_down

    if e.key == pygame.K_LEFT:
        keys_down -= 1
        if keys_down == 0:
            return STOP
        else:
            return LEFT
    elif e.key == pygame.K_RIGHT:
        keys_down -= 1
        if keys_down == 0:
            return STOP
        else:
            return RIGHT
    else:
        return previous_input


def getInput():
    """
    Return int representing input for human player

    -1 : move left
     0 : stop
     1 : move right
    """

    global previous_input
    global keys_down

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            previous_input = keyDown(event)
        elif event.type == pygame.KEYUP:
            previous_input = keyUp(event)
        elif event.type == pygame.QUIT:
            sys.exit()

    return previous_input
