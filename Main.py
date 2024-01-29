import math
import random
import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

# Initialize Pygame and give access to all the methods in the package
pygame.init()



# Set up the screen dimensions
FPS = 60
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

        char.x_speed = char.dash_speed + char.walk_speed

        def reset_ground(self):
            char.rect.bottom = self.rect.top
            char.jumping = False
            char.y_speed = 0
            char.double_jump_ready = 2
            char.have_dash = True

        def bonk_head(self):
            char.y_speed = 2 #make the player immediately fall
            char.rect.top = self.rect.bottom


        if char.rect.colliderect(self.rect):

            if char.y_speed > 0: # if player falls in/on the block

                if char.x_speed > 0: # if player moving right

                    if char.rect.right - round(char.x_speed) > self.rect.left: # - if player land ontop of platform
                        reset_ground(self)

                        
                    else:
                        char.rect.right = self.rect.left
                        char.on_wall = True
                        print("wall jump true!")



                else: # if player moving left or not a all (doesn't matter)
  
                    if char.rect.left - round(char.x_speed)+1 < self.rect.right: # +  if player land ontop of platform
                        reset_ground(self)

                    else:
                        char.rect.left = self.rect.right
                        char.on_wall = True
                        print("wall jump true!")


                        
            elif not char.jumping: # if player walks into the block

                char.rect.centerx -= char.x_speed



            else: # if player jumps into the block or bonks his head on it

                if char.x_speed > 0: # if player moving right

                    if char.rect.right - round(char.x_speed) > self.rect.left: # -
                        bonk_head(self)

                    else:
                        char.rect.right = self.rect.left
                        char.on_wall = True
                        print("wall jump true!")



                else: # if player moving left or not a all (doesn't matter)
                    if char.rect.left - round(char.x_speed)+1 < self.rect.right: # IDK WHY THE +1 WORKS BUT IT DOES OK
                        bonk_head(self)

                    else:
                        char.rect.left = self.rect.right
                        char.on_wall = True
                        print("wall jump true!")                           

        elif char.rect.bottom == self.rect.top and char.rect.right > self.rect.left and char.rect.left < self.rect.right: #if player ontop of platform (being on top doesn't count as colliding for some reason)
            pass

        else:
            num_not_collides += 1

class Enemy(Thing):
    def __init__(self,color,xsize,ysize,x,y,speed,on_x_axis,point1,point2):
        super(Enemy,self).__init__(color,xsize,ysize,x,y)
        self.speed = speed
        self.on_x_axis = on_x_axis
        self.point1 = point1
        self.point2 = point2

    def move(self):
        if self.on_x_axis:
            self.rect.centerx += self.speed
            if self.rect.x > self.point2 or self.rect.x < self.point1:
                self.speed *= -1
        else:
            self.rect.centery += self.speed
            if self.rect.y > self.point2 or self.rect.y < self.point1:
                self.speed *= -1


    def kill_player(self,char):
        char.rect.centerx = player_level_spawns[lv_index][0]
        char.rect.centery = player_level_spawns[lv_index][1]

    def collision(self,char):
        global num_not_collides
        if char.rect.colliderect(self.rect):
            self.kill_player(char)
        else:
            num_not_collides += 1

        self.move()

class Portal(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Portal,self).__init__(color,xsize,ysize,x,y)

    def reset_player(self,char):
        char.rect.centerx = player_level_spawns[lv_index][0]
        char.rect.centery = player_level_spawns[lv_index][1]


    def collision(self,char):
        global num_not_collides
        global lv_index
        if char.rect.colliderect(self.rect):
            lv_index += 1
            self.reset_player(char)
        else:
            num_not_collides += 1
    

class Player(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Player,self).__init__(color,xsize,ysize,x,y)
        self.ground_speed = 2
        self.jumping = True
        self.y_speed = 0
        self.walk_speed = 0 # walk and ground speed are stupid names IK, its to late to change them now
        self.double_jump_ready = 2
        self.have_dash = True
        self.dash_speed = 0 
        self.on_wall = False

        # jump ready 2 = on ground
        # jump ready 1 = in air and hasn't used it yet
        # jump ready 0 = means in air and already used it (I should really use a enum for this)


    def dash_color(self):
        if player.have_dash:
            player.color = "Green"
        else:
            player.color = "Blue"

        player.image.fill(player.color)

    def walk(self):
        if key[pygame.K_LEFT]:
            self.rect.centerx -= self.ground_speed
            self.walk_speed = -2 # this keeps track of how fast we're going, we'll need this later for collision
            
            
        elif key[pygame.K_RIGHT]:
            self.rect.centerx += self.ground_speed
            self.walk_speed = 2 # this keeps track of how fast we're going, we'll need this later for collision

        else:
            self.walk_speed = 0

    def jump(self):
        if self.jumping and not key[pygame.K_z] and self.double_jump_ready != 0:
            self.double_jump_ready = 1

        if key[pygame.K_z] and not self.jumping: # and self.double_jump_ready == 2:
            if not self.have_dash:
                self.dash_speed += (self.walk_speed * 4)
                self.have_dash = True

            self.y_speed = -10
            self.double_jump_ready = 2
            self.jumping = True
            #if abs(self.dash_speed) >0:
                #self.dash_speed += 12

        elif key[pygame.K_z] and self.jumping and self.double_jump_ready == 1:
            self.y_speed = -10
            self.double_jump_ready = 0

        if self.jumping:
            self.y_speed +=.6

    def wall_jump(self):
        if key[pygame.K_z] and self.on_wall:
            self.dash_speed = self.walk_speed * -4
            self.y_speed = -8
            self.double_jump_ready = 2

    def dash(self):
        if key[pygame.K_x] and self.have_dash:
            self.have_dash = False
            self.dash_speed = self.walk_speed * 8.5
            self.y_speed = 0
            #self.rect.centery -= 1
            
    def update_dash(self):
        self.dash_speed *= .9
        if abs(self.dash_speed) < .7:
            self.dash_speed = 0

        if not self.jumping and self.dash_speed == 0:
            self.have_dash = True

    def update_move(self):
        self.rect.centery += self.y_speed
        self.rect.centerx += self.dash_speed

    def all_player_methods(self):
        self.walk()
        self.jump()
        self.wall_jump()
        self.dash()
        self.update_dash()
        self.update_move()
        self.dash_color()



    
    
lv_index = 0   

player_level_spawns = ((100,100),(400,100))

player = Player("Green",30,30,300,100)

platform = Terrain("Gray",200,150,130,350)
platform2 = Terrain("Gray",200,150,680,350)
ground = Terrain("Gray",600,100,400,500)

enemy = Enemy("Red",50,50,400,300,2,True,200,400)

lv_1_portal = Portal("Purple",50,50,700,150)

character_list = pygame.sprite.Group()


lv_1_terrain = pygame.sprite.Group()
lv_2_terrain = pygame.sprite.Group() 
lv_3_terrain = pygame.sprite.Group()

lv_1_terrain.add(ground)
lv_1_terrain.add(platform)
lv_1_terrain.add(platform2)
lv_1_terrain.add(enemy)
lv_1_terrain.add(lv_1_portal)

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
        player.on_wall = False
        print("yeah")

    player.all_player_methods()



    

    # Update the display
    pygame.display.flip()

    # Set a frame rate to 60 frames per second
    clock.tick(60)
    #dt = clock.tick(FPS)/1000
    #print(dt)

# Quit Pygame properly
pygame.quit()
sys.exit()
