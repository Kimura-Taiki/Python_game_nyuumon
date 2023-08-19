import pygame
import sys
import math

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GOLD  = (255, 216,   0)
SILVER= (192, 192, 192)
COPPER= (192, 112,  48)

def main():
    pygame.init()
    pygame.display.set_caption("初めてのPygame 図形")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    tmr = 0

    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
    
    