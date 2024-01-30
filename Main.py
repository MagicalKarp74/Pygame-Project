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

# Public variables (yucky IK)

FPS = 60

font=pygame.font.Font(None,30)

lv_index = 0

lv_texts = ["Left and right arrow keys to move :D purple portal takes you to the next level!","Z to jump, and double jump while in the air! Beware, red rectangles kill you ","Press x while moving to dash","Press z on walls to wall jump","Jump immediately after dashing to get a super jump!","Thats all you need to know, good luck!"]

player_level_spawns = ((80,330),(80,330),(80,330),(80,330),(80,430))

num_not_collides = 0

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
    
class Text(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Text,self).__init__(color,xsize,ysize,x,y)

    def set_text(self):
        global num_not_collides
        num_not_collides += 1
        self.text = font.render(lv_texts[lv_index],False,'White')

    def display_text(self):
        screen.blit(self.text,(self.rect.left+10,self.rect.top))


    def all_methods(self,char):
        self.set_text()
        self.display_text()




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
            char.y_speed = 1 #make the player immediately fall
            char.rect.top = self.rect.bottom
            char.on_wall = False
        
        def hit_left_wall(self):
            char.rect.right = self.rect.left
            char.on_wall = True

        def hit_right_wall(self):
            char.rect.left = self.rect.right
            char.on_wall = True




        if char.rect.colliderect(self.rect):

            if char.y_speed > 0: # if player falls in/on the block

                if char.x_speed > 0: # if player moving right

                    if char.rect.right - round(char.x_speed) > self.rect.left: # - if player land ontop of platform
                        reset_ground(self)

                        
                    else:
                        hit_left_wall(self)



                else: # if player moving left or not a all (doesn't matter)
  
                    if char.rect.left - round(char.x_speed)+1 < self.rect.right: # +  if player land ontop of platform
                        reset_ground(self)

                    else:
                        hit_right_wall(self)

                        
            elif not char.jumping: # if player walks into the block

                
                if char.x_speed > 0:
                    char.rect.right = self.rect.left
                else:
                    char.rect.left = self.rect.right



            else: # if player jumps into the block or bonks his head on it

                if char.x_speed > 0: # if player moving right

                    if char.rect.right - round(char.x_speed) > self.rect.left: # -
                        bonk_head(self)

                    else:
                        hit_left_wall(self)


                else: # if player moving left or not a all (doesn't matter)
                    if char.rect.left - round(char.x_speed)+1 < self.rect.right: # IDK WHY THE +1 WORKS BUT IT DOES OK
                        bonk_head(self)

                    else:
                        hit_right_wall(self) 


        elif char.rect.bottom == self.rect.top and char.rect.right > self.rect.left and char.rect.left < self.rect.right: #if player ontop of platform (being on top doesn't count as colliding for some reason)
            pass

        else:
            num_not_collides += 1

    def all_methods(self,char):
        self.collision(char)

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
        num_not_collides += 1
        if char.rect.colliderect(self.rect):
            self.kill_player(char)

    def all_methods(self,char):
        self.collision(char)
        self.move()


class Portal(Thing):
    def __init__(self,color,xsize,ysize,x,y):
        super(Portal,self).__init__(color,xsize,ysize,x,y)

    def reset_player(self,char):
        char.rect.centerx = player_level_spawns[lv_index][0]
        char.rect.centery = player_level_spawns[lv_index][1]

    def collision(self,char):
        global num_not_collides
        num_not_collides += 1
        global lv_index
        if char.rect.colliderect(self.rect):
            lv_index += 1
            self.reset_player(char)


    def all_methods(self,char):
        self.collision(char)
    

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

# player stuff

player = Player("Green",30,30,player_level_spawns[lv_index][0],player_level_spawns[lv_index][1])
character_list = pygame.sprite.Group()
character_list.add(player)

# all level's platforms

lv_0_1_platform = Terrain("Gray",800,300,400,500)
lv_1_1_platform = Terrain("gray",200,200,700,550)
lv_2_1_platform = Terrain("gray",200,300,100,500)
lv_2_2_platform = Terrain("gray",100,250,250,500)
lv_2_3_platform = Terrain("gray",70,275,290,500)
lv_2_4_platform = Terrain("gray",80,15,500,500)

# the singular text box we need

text_box = Text("Blue",800,100,400,100)

# Enemy blocks

lv_1_1_enemy = Enemy("Red",10,30,200,560,0,True,200,500)
lv_1_2_enemy = Enemy("Red",10,70,400,540,0,True,200,500)
lv_1_3_enemy = Enemy("Red",10,110,600,515,0,True,200,500)
lv_2_1_enemy = Enemy("Red",55,20,227,370,0,True,200,500)
lv_2_2_enemy = Enemy("Red",450,20,550,570,0,True,200,500)

#enemy portals

lv_0_to_5_portal = Portal("Purple",30,30,750,325)
lv_6_portal = Portal("Purple",50,50,700,450)
lv_7_portal = Portal("Purple",50,50,700,450)
lv_8_portal = Portal("Purple",50,50,700,450)
lv_9_portal = Portal("Purple",50,50,700,450)

# defining boundaries used in all/most levels

text_block = Terrain("Gray",900,300,400,150)

boundary1 = Terrain("Gray",50,600,0,300)
boundary2 = Terrain("Gray",50,600,800,300)
boundary3 = Terrain("Gray",800,50,400,600)
boundary4 = Terrain("Gray",800,50,400,0)

boundaries = pygame.sprite.Group()

boundaries.add(boundary1)
boundaries.add(boundary2)
boundaries.add(boundary3)
boundaries.add(boundary4)

#all the levels terrains

lv_0_terrain = pygame.sprite.Group()
lv_1_terrain = pygame.sprite.Group() 
lv_2_terrain = pygame.sprite.Group()
lv_3_terrain = pygame.sprite.Group()
lv_4_terrain = pygame.sprite.Group()
lv_5_terrain = pygame.sprite.Group()
lv_6_terrain = pygame.sprite.Group()
lv_7_terrain = pygame.sprite.Group()
lv_8_terrain = pygame.sprite.Group()
lv_9_terrain = pygame.sprite.Group()

# all levels in list

levels = [lv_0_terrain,lv_1_terrain,lv_2_terrain,lv_3_terrain,lv_4_terrain,lv_5_terrain,lv_6_terrain,lv_7_terrain,lv_8_terrain,lv_9_terrain]

#loop for repeat stuff

for i in range(len(levels)):
    if i <= 6 or i == 9:
        levels[i].add(text_box)
        levels[i].add(text_block)
        levels[i].add(lv_0_to_5_portal)
    levels[i].add(boundaries)

# adding all the stuff
    

# lv 0 props
lv_0_terrain.add(lv_0_1_platform)

#lv 1 props
lv_1_terrain.add(lv_1_1_enemy)
lv_1_terrain.add(lv_1_2_enemy)
lv_1_terrain.add(lv_1_3_enemy)
lv_1_terrain.add(lv_1_1_platform)

#lv 2 props
lv_2_terrain.add(lv_2_1_platform)
lv_2_terrain.add(lv_2_2_platform)
lv_2_terrain.add(lv_2_3_platform)
lv_2_terrain.add(lv_2_4_platform)
lv_2_terrain.add(lv_2_1_enemy)
lv_2_terrain.add(lv_2_2_enemy)


running = True
while running:
    # Event handling
    for event in pygame.event.get(): # pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    #screen.fill(lv_colors[lv_index])
    screen.fill("Black")
    num_not_collides = 0

    character_list.draw(screen)

    levels[lv_index].draw(screen)

    for block in levels[lv_index]:
        block.all_methods(player)

    if num_not_collides == len(levels[lv_index]):
        player.jumping = True
        player.on_wall = False

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
