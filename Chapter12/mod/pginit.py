import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption("One hour Dungeon")
screen = pygame.display.set_mode((880, 720))
font = pygame.font.Font(None, 40)
fontS = pygame.font.Font(None, 30)
key = pygame.key.get_pressed()
