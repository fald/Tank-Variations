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
FPS = 15

TANK_DIM = (60, 45)

BLOCK_SIZE = 50

#-----------------------

#-----------------------
# OTHER GLOBALS
#-----------------------
SCORE = 0
player = {'x':RESOLUTION[0] * 0,
          'y':RESOLUTION[1] * 0.9 - TANK_DIM[1],
          'move':0,
          'turn':0,
          # Angle is in radians and assuming facing right as 0 or 2pi
          'angle':0, #2 * math.pi - math.pi * .25,
          'max':0.07,
          'min':-0.77,
          'color':GREEN}
enemy = {'x':RESOLUTION[0] * 1 - TANK_DIM[0],
         'y':RESOLUTION[1] * 0.9 - TANK_DIM[1],
         'move':0,
         'turn':0,
         'angle':math.pi,
         'max':math.pi + 0.77,
         'min':math.pi - 0.07,
         'color':BLUE}
barrier = {'height':RESOLUTION[1] - player['y'] + TANK_DIM[1] + random.randint(0, TANK_DIM[1] * 2),
           'width':random.randint(10, TANK_DIM[0] / 2),
           'x':RESOLUTION[0] / 2 + random.randint(-0.2*RESOLUTION[0],
                                                  0.2*RESOLUTION[0])}

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
        # gameDisplay.fill(BG_COLOR)
        # player['x'] += player['move']
        # player['angle'] = min(max(player['min'], player['angle'] + player['turn']), player['max'])
        # draw_tank(gameDisplay, player)
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
##                    if event.key == pygame.K_RIGHT:
##                        player['move'] = 0
##                    if event.key == pygame.K_LEFT:
##                        player['move'] = 0
##                    if event.key in (pygame.K_UP, pygame.K_DOWN):
##                        player['turn'] = 0
                        
                    pass

            elif event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_RIGHT:
##                    player['move'] = 5
##                if event.key == pygame.K_LEFT:
##                    player['move'] -= 5
##                if event.key == pygame.K_UP:
##                    player['turn'] = -math.pi / 90
##                if event.key == pygame.K_DOWN:
##                    player['turn'] = math.pi / 90
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
    play = True
    stall = False

    while play:
        gameDisplay.fill(BG_COLOR)

        player['x'] += player['move']
        player['x'] = max(min(RESOLUTION[0] - TANK_DIM[0],
                              player['x']), 0)
        player['angle'] = min(max(player['min'],
                                  player['angle'] + player['turn']),
                              player['max'])
        draw_tank(gameDisplay, player)

        enemy['x'] += enemy['move']
        enemy['x'] = max(min(RESOLUTION[0] - TANK_DIM[0],
                              enemy['x']), 0)
        enemy['angle'] = min(max(enemy['min'],
                                 enemy['angle'] - player['turn']),
                             enemy['max'])
        draw_tank(gameDisplay, enemy)

        # Trivial collision, it'll do for V0.01, but its a bit shit.
        if (player['x'] + TANK_DIM[0]) > (enemy['x']):
            player['x'] -=  max(abs(enemy['move']), abs(player['move']))
            enemy['x'] +=  max(abs(enemy['move']), abs(player['move']))
            enemy['move'] = 0
            player['move'] = 0
            stall = True
        if (player['x'] + TANK_DIM[0]) >= \
           (barrier['x'] - 0.5 * barrier['width']):
            player['x'] -= player['move']
            player['move'] = 0
            stall = True
        if enemy['x'] <= (barrier['x'] + 0.5 * barrier['width']):
            enemy['x'] -=  enemy['move']
            enemy['move'] = 0
            stall = True

        draw_barrier(gameDisplay)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                else:
                    if event.key == pygame.K_p:
                        pause()
                    if event.key == pygame.K_RIGHT:
                        player['move'] = 0
                        enemy['move'] = 0
                        stall = False
                    if event.key == pygame.K_LEFT:
                        player['move'] = 0
                        enemy['move'] = 0
                        stall = False
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        player['turn'] = 0
                        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if not stall:
                        player['move'] = 5
                        enemy['move'] = 5
                if event.key == pygame.K_LEFT:
                    if not stall:
                        player['move'] = -5
                        enemy['move'] = -5
                if event.key == pygame.K_UP:
                    player['turn'] = -math.pi / 90
                if event.key == pygame.K_DOWN:
                    player['turn'] = math.pi / 90


        pygame.display.update()
        clock.tick(FPS)


def controls():
    controls = True
    gameDisplay.fill(BG_COLOR)
    msg_to_screen("CONTROLS",
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
    msg_to_screen("Pause: P",
                  defaultFont, BLACK,
                  (RESOLUTION[0] / 2,
                   RESOLUTION[1] / 2 + 4 * defaultFont.get_linesize()))

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


def new_enemy():
    pass


def new_barrier():
    global barrier
    barrier = {'height': player['y'] + random.randint(0, TANK_DIM[1] * 2),
               'width':random.randint(10, TANK_DIM[0] / 2),
               'x':RESOLUTION[0] / 2 + random.randint(0.2*RESOLUTION[0], -0.2*RESOLUTION[0])}
               
    return


def draw_barrier(display):
    # Lines drawn centered on the start pos, unlike rects
    #pygame.draw.line(display, BLACK, (0,0), (0, RESOLUTION[1]), RESOLUTION[0])
    #pygame.draw.line(display, BLACK, (0,0), (0, RESOLUTION[1]), 2)
    pygame.draw.line(display, BLACK,
                     (barrier['x'], RESOLUTION[1]),
                     (barrier['x'], RESOLUTION[1] - barrier['height']),
                      barrier['width'])
    return
    

    
def draw_tank(display, tank,
              tankW=TANK_DIM[0], tankH=TANK_DIM[1], tread_radius=0.8):
    # pos is the circles center
    turret_center = (int(tank['x'] + tankW / 2.0),
                     int(tank['y'] + tankH / 3.0))
    turret_radius = int(tankH / 3.0)
    turret = pygame.draw.circle(display, tank['color'], turret_center, turret_radius)

    gun_length  = turret_radius * 2
    gun_start   = (turret_center[0], int(turret_center[1] - turret_radius * 0.3))
    gun_end     = [gun_start[0] + int(math.cos(tank['angle']) * gun_length),
                   gun_start[1] + int(math.sin(tank['angle']) * gun_length)]
    gun_thick   = int(turret_radius * 0.3)
    gun = pygame.draw.line(display, tank['color'], gun_start, gun_end, gun_thick)

    # Tread is the outer tread - in black to look like tires.
    tread_x, tread_y = tank['x'], int(tank['y'] + tankH / 3.0)
    # Tread 2 is the inner treads - nothing fancy, just so the outer
    # ones kinda look like tires.
    tread2_x, tread2_y = tread_x + int(tankW / 10), tread_y + int(tankW / 10)
    
    tread_w, tread_h = tankW, int(tankH * 2 / 3.0)
    tread2_w, tread2_h = tread_w - int(tankW / 5), tread_h - int(tankW / 5)

    outerTread = AAfilledRoundedRect(display, (tread_x, tread_y, tread_w, tread_h),
                                     BLACK, tread_radius)
    innerTread = AAfilledRoundedRect(display, (tread2_x, tread2_y, tread2_w, tread2_h),
                                     tank['color'], tread_radius)

    wheel_radius = int(tread2_h / 4)
    top_wheels = int(float(tread2_w) / (2 * wheel_radius))
    bot_wheels = top_wheels - 1
    top_spacing = (tread2_w - top_wheels * 2 * wheel_radius) / (top_wheels - 1)
    bot_spacing = (tread2_w - wheel_radius - bot_wheels * 2 * wheel_radius) / (bot_wheels - 1)
    cur_position = [tread2_x + wheel_radius, tread2_y + wheel_radius]
    for i in range(top_wheels):
        pygame.draw.circle(gameDisplay, BLACK, cur_position, wheel_radius)
        cur_position = [cur_position[0] + 2 * wheel_radius + top_spacing, cur_position[1]]
    cur_position = [tread2_x + int((3 / 2.0) * wheel_radius), tread2_y + 3 * wheel_radius]
    for i in range(bot_wheels):
        pygame.draw.circle(gameDisplay, BLACK, cur_position, wheel_radius)
        cur_position = [cur_position[0] + 2 * wheel_radius + bot_spacing, cur_position[1]]
    
    


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

