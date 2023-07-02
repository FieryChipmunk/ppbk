#init stuff
import pygame
from player import Player
from asteroid import Asteroid
from particle_system import Particle_System
from sys import exit
from font_helper import Font_Helper
from camera import Camera
from pickup import Pickup
import random

pygame.init()

#varables so that I can change screen size more easily
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

#creates a screen sized with the variables above
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#imports impact font
impact = pygame.freetype.Font("Assets/impact.ttf", 10)

#sets the name of the window
pygame.display.set_caption("Pew Pew Boom Kablooie")

#imports the backgrounds and icon
game_background = pygame.transform.scale(pygame.image.load("Assets/Game Background.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_overlay = pygame.transform.scale(pygame.image.load("Assets/Menu Overlay.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
game_overlay = pygame.transform.scale(pygame.image.load("Assets/Game Overlay.png").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("Assets/Icon.png").convert_alpha()

pygame.display.set_icon(icon)

#images to import should contain the
#paths to all the images I need in this program as strings, except 
#the backgrounds cause they need a higher res
images_to_import = ["Assets/Fighter.png",
"Assets/Laser.png",
"Assets/Asteroid.png",
"Assets/Explosion.png",
"Assets/Pickup.png"]
#images should be declared empty
images = {}

#this loop takes all the paths from images_to_import and
#turns them into actual images accesable in the image dictionary
for image in images_to_import:

        new_image = pygame.image.load(image).convert_alpha()
        new_image = pygame.transform.scale(new_image, (64,64))
        images.update({image: new_image})

#imports pew, boom, and kablooie sounds and makes channels for them
pew = pygame.mixer.Sound("Assets/Pew.mp3")
pew_channel = pygame.mixer.Channel(0)
boom = pygame.mixer.Sound("Assets/Boom.mp3")
boom_channel = pygame.mixer.Channel(1)
kablooie = pygame.mixer.Sound("Assets/Kablooie.mp3")
kablooie_channel = pygame.mixer.Channel(2)
bloop = pygame.mixer.Sound("Assets/Bloop.mp3")
bloop_channel = pygame.mixer.Channel(3)

def game():

        running = True

        has_run = False

        time_since_death = 0

        score = 0

        while running:

                if not has_run:

                        pygame.mixer.music.load("Assets/Aware.mp3")
                        pygame.mixer.music.play(-1)

                        #creates font helper
                        font_helper = Font_Helper(impact)

                        #creating a player in the middle of the screen
                        player = Player(images["Assets/Fighter.png"], images["Assets/Laser.png"], SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

                        #creates camera
                        camera = Camera(player)

                        #asteroid loop array combo
                        asteroids = [None] * 15

                        for i in range(0, 15):

                                new_asteroid = Asteroid(images["Assets/Asteroid.png"],-301, -301, 0, 0, 0)
                                asteroids[i] = new_asteroid

                        pickup = Pickup(images["Assets/Pickup.png"], random.randint(0, SCREEN_WIDTH * 2), random.randint(0, SCREEN_HEIGHT * 2))

                        player_death_particle_system = Particle_System(10, images["Assets/Explosion.png"], SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        0, 360, 3, 7, 10, 30)

                        score = 0

                        has_run = True

                #this checks the pygame events every frame
                for event in pygame.event.get():

                        #player method for getting user input,
                        player.get_input(event, pew, pew_channel)
                
                        #hardcoded quit function   
                        if event.type == pygame.QUIT:

                                pygame.quit
                                exit()
                        
                        #quits to menu
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                
                                has_run = False
                                running = False

                #moves the player and adds score if it is not dead
                if player.dead == False:
                
                        player.update(SCREEN_WIDTH, SCREEN_HEIGHT)
                        score += 1/60

                #updates player death explosion if player dead and then quits to menu
                if player.dead == True:

                        if time_since_death == 0:

                                kablooie_channel.play(kablooie)

                        player_death_particle_system.x = player.x
                        player_death_particle_system.y = player.y
                        player_death_particle_system.update()
                        time_since_death += 1
                        if time_since_death >= 120:

                                has_run = False
                                running = False

                #does all the asteroid updates
                for asteroid in asteroids:

                        should_reset = False
                        asteroid.update()
                        player.detect_collision(asteroid)
                        if asteroid.position_check(SCREEN_WIDTH, SCREEN_HEIGHT):

                                should_reset = True
                        
                        elif asteroid.detect_collision(player.lasers):


                                should_reset = True
                                if player.dead == False:
                                        
                                        score += 5
                                        boom_channel.play(boom)

                        if should_reset:

                                #generates a random number to see which quadrant the asteroid should generate in
                                rand_num = random.randint(0,3)

                                #this if-elif-else statement places the asteroid at the right place given its seed
                                if rand_num == 0:

                                        asteroid.x = -300
                                        asteroid.y = random.randint(0, SCREEN_HEIGHT * 2)
                                        asteroid.vector = random.randint(225, 315)

                                elif rand_num == 1:

                                        asteroid.x = random.randint(0, SCREEN_WIDTH * 2)
                                        asteroid.y = -300
                                        asteroid.vector = random.randint(135, 225)

                                elif rand_num == 2:

                                        asteroid.x = (SCREEN_WIDTH * 2) + 300
                                        asteroid.y = random.randint(0, SCREEN_HEIGHT * 2)
                                        asteroid.vector = random.randint(45, 135)

                                else:

                                        asteroid.x = random.randint(0, SCREEN_WIDTH * 2)
                                        asteroid.y = (SCREEN_HEIGHT * 2) + 300
                                        asteroid.vector = random.randint(-45, 45)

                                asteroid.rotation_speed = random.randint(-5,5)
                                asteroid.speed = random.randint(3,7)

                #checks if pickup needs to be reset, and resets it if it does
                if pickup.picked_up == True:

                        pickup.x = random.randint(0, SCREEN_WIDTH * 2)
                        pickup.y = random.randint(0, SCREEN_HEIGHT * 2)
                        pickup.picked_up = False

                #collides the pickup
                pickup.collide(player, bloop_channel, bloop)

                #updates camera
                camera.update(SCREEN_WIDTH, SCREEN_HEIGHT)

                #draws the background
                screen.fill((0, 0, 0))
                for i in range(0, 2):

                        for j in range(0, 2):

                                screen.blit(game_background, ((i * SCREEN_WIDTH) - camera.x_offset, (j * SCREEN_HEIGHT) - camera.y_offset))

                #calls the players draw method
                player.draw(screen, camera)

                #draws player particle system if player is dead
                if player.dead == True:

                        player_death_particle_system.draw(screen, camera)

                #draws the asteroids
                for asteroid in asteroids:

                        asteroid.draw(screen, camera)

                #draws the pickup
                pickup.draw(screen, camera)

                #draws the HUD, overlay, and score
                screen.blit(game_overlay, (0,0))
                font_helper.display_text(int(score), 600, 0, screen)
                player.HUD(screen)

                #updates the frame every frame
                #this line needs to be after any and all methods
                #that change something on the screen
                pygame.display.update()
                
                #sets the frames per second, in this instance to 60
                pygame.time.Clock().tick(60)

def menu():

        pygame.mixer.music.load("Assets/Believe.mp3")
        pygame.mixer.music.play(-1)

        while True:

                #this checks the pygame events every frame
                for event in pygame.event.get():
                
                        #hardcoded quit function   
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                
                                pygame.quit
                                exit()

                        #if the user presses any key, it will go to the game
                        elif event.type == pygame.KEYDOWN:

                                game()

                                pygame.mixer.music.load("Assets/Believe.mp3")
                                pygame.mixer.music.play(-1)

                screen.blit(game_background, (0,0))
                screen.blit(menu_overlay, (0,0))

                #updates the frame every frame
                #this line needs to be after any and all methods
                #that change something on the screen
                pygame.display.update()
                
                #sets the frames per second, in this instance to 60
                pygame.time.Clock().tick(60)

menu()