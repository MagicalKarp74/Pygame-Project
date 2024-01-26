import math
import random
import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

# Initialize Pygame and give access to all the methods in the package
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super(Character,self).__init__()
        self.image = pygame.Surface((100,100), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill("Green")
        self.rect = self.image.get_rect(center = (100, 100))

    def animate(self):
        pass
        

player = Character()

character_list = pygame.sprite.Group()

character_list.add(player)

running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    screen.fill("light blue")


    character_list.draw(screen)












    

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
