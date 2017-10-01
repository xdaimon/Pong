import pygame, sys

def keyDown(e):
    """
    Switch through movement keys to see which is pressed
    """
    pass

def keyUp(e):
    """
    Switch through movement keys to see which is released
    """
    pass

def getInput():
    """
    Return int representing input for human player

    -1 : move left
     0 : stop
     1 : move right
    """
    for event in pygame.event.get():
        if event.type == pygame.key.KEYDOWN:
            keyDown(event)
        elif event.type == pygame.key.KEYUP:
            keyUp(event)
        elif event.type == pygame.key.QUIT:
            sys.exit()
    pass
