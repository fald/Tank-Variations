# Basic options for most things
# No error checking for setters, laziness
# beats assuming I'll fuck up

RESOLUTION  = (800, 600)
CAPTION     = ""
FPS         = 30

def set_resolution(new_x, new_y):
    global RESOLUTION
    RESOLUTION = (new_x, new_y)

def set_resolution(new_res):
    global RESOLUTION
    RESOLUTION = new_res

def set_caption(new_caption):
    global CAPTION
    CAPTION = new_caption

def set_FPS(new_fps):
    global FPS
    FPS = new_fps

def default():
    global RESOLUTION, CAPTION, FPS
    RESOLUTION  = (800, 600)
    CAPTION     = ""
    FPS         = 30
