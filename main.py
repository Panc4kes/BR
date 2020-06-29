import pygame, os, math
# import random
import auth

# Constants
WIDTH = 800
HEIGHT = 600

FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
pygame.display.set_caption("Bruh Battle Royale")
sprite_list = []

# Sprites
char = pygame.image.load('images/player.png')
gun = pygame.image.load('images/gun.png')
bg = pygame.image.load('images/bg1.png')

# Game loop
def main():
    global sprite_list

    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        events()
        # Update
        drawWindow()
# events
def events():
    # Process input (events)
    keys = pygame.key.get_pressed()

    # movements

    if (keys[pygame.K_w] and (keys[pygame.K_a] or keys[pygame.K_d])) or (keys[pygame.K_s] and (keys[pygame.K_a] or keys[pygame.K_d])):
        sprite_list[0].vel = sprite_list[0].origvel*0.8
    else:
        sprite_list[0].vel = sprite_list[0].origvel

    if keys[pygame.K_a]:
        sprite_list[0].x -= sprite_list[0].vel

    if keys[pygame.K_d]:
        sprite_list[0].x += sprite_list[0].vel

    if keys[pygame.K_w]:
        sprite_list[0].y -= sprite_list[0].vel

    if keys[pygame.K_s]:
        sprite_list[0].y += sprite_list[0].vel


# Drawing
def drawWindow():
    pygame.display.update()
    drawbg()
    for sprite in sprite_list:
        sprite.draw(screen)

def drawbg():
    # print(sprite_list[0].x,sprite_list[0].y)
    bg_rect = bg.get_rect()
    H_scale = math.floor((sprite_list[0].x)/(bg_rect.size[0]))
    x_move_adj = bg_rect[0]-sprite_list[0].x
    y_move_adj = bg_rect[1]-sprite_list[0].y
    print(H_scale)

    screen.fill([255, 0, 0])
    screen.blit(bg,(x_move_adj+H_scale*(bg_rect.size[0]), y_move_adj))

    screen.blit(bg,(x_move_adj-(H_scale+2)*(bg_rect.size[0])+5, y_move_adj))
    screen.blit(bg,(x_move_adj+(H_scale+1)*(bg_rect.size[0])-5, y_move_adj))
    screen.blit(bg,(x_move_adj+(H_scale+2)*(bg_rect.size[0])-5, y_move_adj))
    
def init():
    global sprite_list
    # initialize pygame
    # auth.run()
    pygame.init()
    pygame.mixer.init()
    sprite_list.append(Player(char, 0, 0))
    sprite_list.append(Object(gun, 500, 350))

class Player:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image
        self.vel = 6
        self.origvel = self.vel
        self.angle = 0
        self.center = (WIDTH/2,HEIGHT/2)
        self.rect = self.image.get_rect()

    def rotate(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        self.rot_angle = (math.degrees(math.atan2(self.center[0]-mouseX, self.center[1]-mouseY))+90)%360
        old_center = self.rect.center
        self.newimage = pygame.transform.rotate(self.image, self.rot_angle)
        self.rect = self.newimage.get_rect()
        self.rect.center = old_center

    def draw(self, screen):
        self.rotate()
        screen.blit(self.newimage, (self.center[0]+self.rect[0]-self.image.get_rect().size[0]/2, self.center[1]+self.rect[1]-self.image.get_rect().size[1]/2))

class Object:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.image = image
        self.center = (WIDTH/2,HEIGHT/2)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, (self.x-sprite_list[0].x, self.y-sprite_list[0].y))


if __name__ == "__main__":
    init()
    main()
