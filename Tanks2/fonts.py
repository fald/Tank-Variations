# Basic fonts
# Needs pygame imported in whatever module uses this.
# Additionally needs pygame initialized with the options
# from options.py

# Augh, why is this needed if I'm importing this file in another file
# which already has this shit. Fauck.
import pygame.font

def load_default_fonts():
    defaultFont = pygame.font.SysFont("umeuigothic", 32, bold=True)
    tinyFont    = pygame.font.SysFont("umeuigothic", 18, bold=True)
    largeFont   = pygame.font.SysFont("umeuigothic", 64, bold=True)
    return (tinyFont, defaultFont, largeFont)

def set_fonts((tinyName, tinySize, tinyBold),
              (medName, medSize, medBold),
              (largeName, largeSize, largeBold)):
    tinyFont    = pygame.font.SysFont(tinyName, tinySize, tinyBold)
    defaultFont = pygame.font.SysFont(medName, medSize, medBold)
    largeFont   = pygame.font.SysFont(largeName, largeSize, largeBold)
    return (tinyFont, defaultFont, largeFont)
    

