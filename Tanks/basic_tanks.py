#!/usr/bin/env python

import pygame, sys, random, time, math
from pygame.locals import *

#----------------------
# CONFIG
# ---------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (175, 20, 20)
RED2 = (200, 50, 50)
L_RED = (255, 0, 0)
GREEN = (20, 175, 20)
L_GREEN = (0, 255, 0)
BLUE = (20, 20, 200)
YELLOW = (175, 175, 50)
L_YELLOW = (255, 255, 0)

BG_COLOR = GRAY

RESOLUTION = (800, 600)
CAPTION = "Fuck you, I'm a TANK!"
FPS = 10

BLOCK_SIZE = 50

#-----------------------


#-----------------------
# OTHER GLOBALS
#-----------------------
SCORE = 0
#-----------------------


#-----------------------
# PYGAME SETUP
#-----------------------

pygame.init()
gameDisplay = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

defaultFont = pygame.font.SysFont("umeuigothic", 32, bold=True)
tinyFont = pygame.font.SysFont("umeuigothic", 18, bold=True)
largeFont = pygame.font.SysFont("umeuigothic", 64)

# Sprites...
# sprite = pygame.image.load(filename)
# scaled = pygame.transform.scale(sprite, (size, size))

# pygame.display.set_icon(...)

#--------------------------


#--------------------------
# BASIC FUNCTIONS
#--------------------------

# Not my function - didn't read it, don't understand it
# but it gives a round-cornered rectangle, so that's good.
# Source: http://pygame.org/project-AAfilledRoundedRect-2349-.html
# I should really put these in a standard library for me to use.
def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = pygame.Rect(rect)
    color        = pygame.Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = pygame.Surface(rect.size,SRCALPHA)

    circle       = pygame.Surface([min(rect.size)*3]*2,SRCALPHA)
    pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)


def game_intro():
    intro = True
    gameDisplay.fill(BG_COLOR)
    timer = 0
    msg_to_screen("TAAAAAAAANKS?!",
                  largeFont, GREEN,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - largeFont.get_linesize()))
    msg_to_screen("Shoot stuff, don't get shot.",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + defaultFont.get_linesize()))
##    msg_to_screen("Press any non-ludicrous button to start...",
##                  defaultFont, BLACK,
##                  (RESOLUTION[0] / 2,
##                   RESOLUTION[1] / 2 + defaultFont.get_linesize() * 3))

    #==========
    # Buttons!
    #==========
    xSpacing    = int(RESOLUTION[0] / 7.0)
    yHeight     = int(RESOLUTION[1] * 3 / 4.0)
    buttonW, buttonH = xSpacing, xSpacing / 2
    radius      = 0.6

    while intro:
        # For button presses and light ups
        # plz make button object in next iteration
        # Also: Ugly way of dealing with button press overlap.
        if timer < 150:
            button("PLAY", xSpacing, yHeight, buttonW, buttonH, L_GREEN, GREEN)
            button("CONTROLS", xSpacing*3, yHeight, buttonW, buttonH, L_YELLOW, YELLOW)
            button("QUIT", xSpacing*5, yHeight, buttonW, buttonH, L_RED, RED)
        else:
            button("PLAY", xSpacing, yHeight, buttonW, buttonH, L_GREEN, GREEN, action=play)
            button("CONTROLS", xSpacing*3, yHeight, buttonW, buttonH, L_YELLOW, YELLOW,
                   action=controls)
            button("QUIT", xSpacing*5, yHeight, buttonW, buttonH, L_RED, RED, action=quit_game)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                else:
                    # intro = False
                    # return
                    pass

        pygame.display.update()
        clock.tick(FPS)
        if timer < 150:
            timer = min(150, timer + clock.get_time())


def pause():
    paused = True
    msg_to_screen("Paused...",
                  largeFont, RED2,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - largeFont.get_linesize()))
    msg_to_screen("Press P to continue or Q to quit...",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + defaultFont.get_linesize()))
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or \
                   event.key == pygame.K_q:
                    pygame.display.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    paused = False
                    return
        clock.tick(FPS)


def play():
    pass


def controls():
    controls = True
    gameDisplay.fill(BG_COLOR)
    msg_to_screen("CONTROL SCREEN",
                  largeFont, GREEN,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 - largeFont.get_linesize()))
    msg_to_screen("Fire: SPACEBAR",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + defaultFont.get_linesize()))
    msg_to_screen("Turret: UP/DOWN ARROWS",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 2 * defaultFont.get_linesize()))
    msg_to_screen("Move: LEFT/RIGHT ARROWS",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 3 * defaultFont.get_linesize()))

    pygame.display.update()

    # Just to keep it the same size as the main window buttons.
    xSpacing    = int(RESOLUTION[0] / 7.0)
    yHeight     = int(RESOLUTION[1] * 3 / 4.0)
    buttonW, buttonH = xSpacing, xSpacing / 2
    x_pos    = int((RESOLUTION[0] / 2.0) - (buttonW / 2.0))
    # x_pos = xSpacing
    radius      = 0.6
    cur_height = RESOLUTION[1]

    # OK so - get_pressed returns if its down or not.
    # This means that for a split second if the mouse is over a button on
    # the same position ("CONTROLS" in game intro), it'll get caught in
    # a horrific loop.
    # This is not ideal.
    # As a temporary fix in this iteration, I'll just try to have it swipe in from
    # below to make it look like I intended it that way.
    # Could just add a timer. Could have just added a fucking timer.
    while controls:
        if cur_height != yHeight:
            gameDisplay.fill(BG_COLOR, (x_pos, cur_height + 10, buttonW, buttonH))
            cur_height = max(yHeight, cur_height - 10)
            button("RETURN", x_pos, cur_height, buttonW, buttonH, L_YELLOW, YELLOW,
                   action=None)
        else:
            button("RETURN", x_pos, cur_height, buttonW, buttonH, L_YELLOW, YELLOW,
                   action=game_intro)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                else:
                    # intro = False
                    # return
                    pass

        pygame.display.update()
        clock.tick(FPS)


def quit_game():
    pygame.display.quit()
    sys.exit()


def draw_score():
    msg_to_screen("SCORE: %s" % SCORE,
                  tinyFont, BLACK,
                  tinyFont.size("SCORE"))


def msg_to_screen(msg, font, color, location, antialias=True):
    text_surface    = font.render(msg, antialias, color)
    text_rect       = text_surface.get_rect() 

    text_rect.center = location
    gameDisplay.blit(text_surface, text_rect)
    
    return


def text_to_button(surface, 
                   but_color, but_location, but_size, radius,
                   msg, txt_col=BLACK, txt_font=defaultFont, antialias=True):
    textSurf = txt_font.render(msg, antialias, txt_col)
    textRect = textSurf.get_rect()
    textRect.center = (but_location[0] + but_size[0] / 2,
                       but_location[1] + but_size[1] / 2)
    button = AAfilledRoundedRect(surface,
                        (but_location[0], but_location[1],
                         but_size[0], but_size[1]),
                        but_color, radius)    

    
    surface.blit(textSurf, textRect)
    
    return button


def button(txt, x_pos, y_pos, wid, hei,
           active_color, inactive_color, action=None,
           radius=0.6, surface=gameDisplay, txt_col=BLACK,
           txt_font=tinyFont, antialias=True):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    buttonRect = Rect(x_pos, y_pos, wid, hei)
    if buttonRect.collidepoint(cur):
        text_to_button(surface, active_color, (x_pos, y_pos), (wid, hei), radius,
                       txt, txt_font=txt_font)
        if click[0] == 1:
            try:
                action()
            except TypeError:
                pass
    else:
        text_to_button(surface, inactive_color, (x_pos, y_pos), (wid, hei), radius,
                       txt, txt_font=txt_font)
    



#----------------------------


#----------------------------
# MAIN LOOP
#----------------------------

def main_loop():
    gameExit = False
    gameOver = False

    while not gameExit:
        while gameOver:
            msg_to_screen("Game Over, Asshole!",
                          largeFont, RED2,
                          (RESOLUTION[0] / 2,
                           RESOLUTION[1] / 2 - largeFont.get_linesize()))
            msg_to_screen("Press Q to quit or C to continue...",
                          defaultFont, BLACK,
                          (RESOLUTION[0] / 2,
                           RESOLUTION[1] / 2 + defaultFont.get_linesize()))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False # To drop the loop
                if event.type == pygame.KEYUP:
                    if event.key == K_ESCAPE:
                        gameOver = False
                        gameExit = True
                    elif event.key == K_c:
                        main_loop()
                    elif event.key == K_q:
                        gameOver = False
                        gameExit = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    gameExit = True
                elif event.key == K_p:
                    pause()
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    pass
                elif event.key == K_UP or event.key == K_DOWN:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass


        gameDisplay.fill(BG_COLOR)

        pygame.display.update()
        clock.tick(FPS)

    pygame.display.quit()
    sys.exit(0)


#----------------------------


if __name__ == "__main__":
    game_intro()
    main_loop()

