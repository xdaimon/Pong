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

previous_input = STOP

def keyDown(e):
    """
    Switch through movement keys to see which is pressed
    """
    if e.key == pygame.K_UP:
        return RIGHT
    elif e.key == pygame.K_DOWN:
        return LEFT
    else:
        return previous_input


def keyUp(e):
    """
    Switch through movement keys to see which is released
    """
    if e.key == pygame.K_UP:
        return STOP
    elif e.key == pygame.K_DOWN:
        return STOP
    else:
        return previous_input


def getInput():
    global previous_input
    """
    Return int representing input for human player

    -1 : move left
     0 : stop
     1 : move right
    """
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            previous_input = keyDown(event)
        elif event.type == pygame.KEYUP:
            previous_input = keyUp(event)
        elif event.type == pygame.QUIT:
            sys.exit()

    return previous_input
