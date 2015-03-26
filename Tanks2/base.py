# Put together all the default options.
# Puts all the imports in one place, too.
# Defaults changeable via a config file.

# Some things are kind of ugly, like in files
# which you import this, to get to the options,
# you need to type base.options.OPTNAME

import config
import resources
import options
from colors import *
from fonts import *
from functions import *

import os.path, math, copy, pygame, sys, random, time
from pygame.locals import *



def setup():
    '''
        Basic setup. Sets default options, including resolution,
        FPS, and caption. To change these from the default, use
        a config file.
        Also loads in basic colors (to add more, look at colors.py)
        Also loads in other resources such as images and audio.
        Also loads in default fonts.

        To change any of the defaults, look in the
        corresponding .py files.

        Set up objects are set as global objects in this file.
    '''

    global display, fonts, clock
    global RESOLUTION, FPS, CAPTION
    
    if config.USE_DEFAULT_WINDOW:
        options.default()
    else:
        options.set_resolution(config.RES)
        options.set_caption(config.CAP)
        options.set_FPS(config.FPS)

    # Make it less annoying to call options
    # (no more base.options.NAME)
    # Not going to do the same with resources as
    # there may just be too many to bother with.
    RESOLUTION = options.RESOLUTION
    CAPTION = options.CAPTION
    FPS     = options.FPS
    

    pygame.init()
    display = pygame.display.set_mode(options.RESOLUTION)
    pygame.display.set_caption(options.CAPTION)
    clock = pygame.time.Clock()

    if config.USE_DEFAULT_FONTS:
        fonts = load_default_fonts()
    else:
        fonts = set_fonts(config.tiny,
                          config.default,
                          config.large)
        





    






