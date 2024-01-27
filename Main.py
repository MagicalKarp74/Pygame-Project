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

class Thing(pygame.sprite.Sprite):
    def __init__(self,color,xsize,ysize,x,y): # This class just gives us a shortcut for initalizing our classes, since all our classes are rectangles
        super(Thing,self).__init__()
        self.color = color
        self.xsize = xsize
        self.ysize = ysize
        self.x = x
        self.y = y
        self.image = pygame.Surface((xsize,ysize), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center = (self.x,self.y))
    

class Terrain(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Terrain,self).__init__(color,xsize,ysize,x,y)

    def collision(self,char):

        global num_not_collides

        def reset_ground(self):
            char.rect.bottom = self.rect.top
            char.jumping = False
            char.y_speed = 0
            char.double_jump_ready = 2

        def bonk_head(self):
            char.y_speed = 2 #make the player immediately fall
            char.rect.top = self.rect.bottom




        if char.rect.colliderect(self.rect):


            if char.y_speed > 0: # if player falls in/on the block


                if char.walk_speed > 0: # if player moving right

                    if char.rect.right - char.walk_speed >= self.rect.left: # if player land ontop of platform
                        reset_ground(self)

                    else:
                        char.rect.centerx -= char.walk_speed #if player hit the side of platform

                else: # if player moving left or not a all (doesn't matter)
  
                    if char.rect.left - char.walk_speed <= self.rect.right: # if player land ontop of platform
                        reset_ground(self)

                    else:
                            char.rect.centerx -= char.walk_speed # if player hit the side of platform

                               
            elif not char.jumping: # if player walks into the block

                char.rect.centerx -= char.walk_speed

            else: # if player jumps into the block or bonks his head on it

                if char.walk_speed > 0: # if player moving right

                    if char.rect.right - char.walk_speed >= self.rect.left:
                        bonk_head(self)

                    else:
                        char.rect.centerx -= char.walk_speed # if player hit he side of platform


                else: # if player moving left or not a all (doesn't matter)
                    if char.rect.left - char.walk_speed <= self.rect.right:
                        bonk_head(self)

                    else:
                        char.rect.centerx -= char.walk_speed # if player hit he side of platform
                                     

        elif char.rect.bottom == self.rect.top and char.rect.left > self.rect.left and char.rect.right < self.rect.right: #if player ontop of platform (being on top doesn't count as colliding for some reason)
            pass
        else:
            num_not_collides += 1

        
    
class Player(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Player,self).__init__(color,xsize,ysize,x,y)
        self.jumping = True
        self.y_speed = 0
        self.walk_speed = 0
        self.double_jump_ready = 2

        # jump ready 2 = on ground
        # jump ready 1 = in air and hasn't used it yet
        # jump ready 0 = means in air and already used it (I should really use a enum for this)

    def control(self):
        if key[pygame.K_LEFT]:
            self.rect.centerx -= 2 # MAGIC NUMBERS WOMP WOMP GO CRY ABOUT IT SKILL ISSUE 
            self.walk_speed = -2 # this keeps track of how fast we're going, we'll need this later for collision
            
            
        if key[pygame.K_RIGHT]:
            self.rect.centerx += 2 # MAGIC NUMBERS WOMP WOMP GO CRY ABOUT IT SKILL ISSUE 
            self.walk_speed = 2 # this keeps track of how fast we're going, we'll need this later for collision

            ## ALL DOUBLE JUMP AND JUMP STUFF


        if self.jumping and not key[pygame.K_z] and self.double_jump_ready != 0:
            self.double_jump_ready = 1

        if key[pygame.K_z] and not self.jumping: # and self.double_jump_ready == 2:
            self.y_speed = -10
            self.jumping = True
            self.double_jump_ready = 2

        elif key[pygame.K_z] and self.jumping and self.double_jump_ready == 1:
            self.y_speed = -10
            self.double_jump_ready = 0

        if key[pygame.K_x]:
            print("hello")

        



        if self.jumping:
            self.y_speed +=.6

        self.rect.centery += self.y_speed



    
    
lv_index = 0   

player = Player("Green",30,30,300,100)

platform = Terrain("Gray",100,30,400,330)
platform2 = Terrain("Gray",80,50,200,380)
platform3 = Terrain("Gray",60,150,550,320)
ground = Terrain("Gray",600,100,400,500)

character_list = pygame.sprite.Group()
lv_1_terrain = pygame.sprite.Group()
lv_2_terrain = pygame.sprite.Group()
lv_3_terrain = pygame.sprite.Group()

lv_1_terrain.add(ground)
lv_1_terrain.add(platform)
lv_1_terrain.add(platform2)
lv_1_terrain.add(platform3)

character_list.add(player)

levels = [lv_1_terrain,lv_2_terrain,lv_3_terrain]

num_not_collides = 0


running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    screen.fill("light blue")
    num_not_collides = 0

    character_list.draw(screen)

    levels[lv_index].draw(screen)

    for block in levels[lv_index]:
        block.collision(player)

    if num_not_collides == len(levels[lv_index]):
        player.jumping = True





    player.control()



    

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)

# Quit Pygame properly
pygame.quit()
sys.exit()
