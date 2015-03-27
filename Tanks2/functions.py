# Basic functions that'll be used by most things.
# Not a fan of having to import pygame more than once :/
import pygame, sys
import colors, fonts

################
##### TODO #####
################
# Have button text returned so if a button moves it'll be easy
# to deal with.
#
#
################

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



def quit_game():
    pygame.display.quit()
    sys.exit(0)

def check_quit(event):
    # Assume you always want to quit on this event.
    if (event.type == pygame.QUIT) or \
       (event.type == pygame.KEYUP and \
        event.key == pygame.K_ESCAPE):
        quit_game()
        return True

def msg_to_screen(surface, message, font,
                  color, location, antialias=True):
    ''' Put a message on the screen at a given location.
    '''
    textSurface = font.render(message, antialias, color)
    textRect    = textSurface.get_rect()
    textRect.center = location
    surface.blit(textSurface, textRect)
    

def text_to_button(surface, button, message,
                  font, txt_col=colors.BLACK, antialias=True):
    ''' Adds text to a given button (provided by its rect).
        There's no default font because pygame needs to be
        initialized for that, and fuck that.
    '''
    textSurf = font.render(message, antialias, txt_color)
    textRect = textSurf.get_rect()
    textRect.center = button.center
    surface.blit(textSurf, textRect)
    

def make_button(surface, rect, color, radius=0.4):
    ''' Create a button that can go from rectangular to
        mostly circular depending on the radius. Draws it
        to the given surface.
    '''
    button = AAfilledRoundedRect(surface, rect, color, radius)
    return button

def button_with_text(surface, but_rect, but_col, but_rad,
                     txt_mes, txt_font, txt_col=colors.BLACK,
                     antialias=True):
    ''' Combine make_button and text_to_buton.
    '''
    button = make_button(surface, but_rect, but_col, but_rad)
    text_to_button(surface, button, txt_mes, txt_font, txt_col, antialias)
    return button


















































