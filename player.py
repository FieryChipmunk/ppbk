#init stuff
import pygame
import math
from laser import Laser

pygame.init()

#makes a class!
class Player:

    #this method is always called when a new instance of a class is created
    def __init__(self, img, laser_img, x, y):
        
        #creating all the values the player will need
        self.img = img

        self.laser_img = laser_img

        self.x = x

        self.y = y

        self.x_velocity = 0

        self.y_velocity = 0

        self.previous_x_velocity = 0

        self.previous_y_velocity = 0

        self.angle = 0

        self.angle_velocity = 0

        self.angle_friction = 1 / 20

        self.turning_speed = 3

        self.turning_right = False

        self.turning_left = False

        self.moving_forward = False

        self.slowing_down = False

        self.speed = 0

        self.acceleration = 0.07
        
        self.top_speed = 6

        self.current_vector = self.angle

        self.lasers = []

        self.shot_cooldown = 10

        self.laser_timer = 0

        self.dead = False

        self.ammo = 7

    #builds a laser and shoots it
    def shoot(self, sound, channel):

        if self.laser_timer == 0 and self.ammo > 0:

                new_laser = Laser(self.laser_img, self.x, self.y, self.angle, 15)
                self.lasers.append(new_laser)
                self.laser_timer = self.shot_cooldown
                channel.play(sound)
                self.ammo -= 1
        
    #this needs to be stuck into the event checking loop 
    def get_input(self, event, sound, channel):

        #sets boolean values of moving checks for the three different
        #types of movement
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:

                self.turning_right = True
                print("player has begun turning right")

        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:

                self.turning_right = False
                print("player has stopped turning right")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:

                self.turning_left = True
                print("player has begun turning left")

        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:

                self.turning_left = False
                print("player has stopped turning left")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:

                self.moving_forward = True
                print("player has begun moving forward")

        elif event.type == pygame.KEYUP and event.key == pygame.K_UP:

                self.moving_forward = False
                print("player has stopped moving forward")

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:

                self.shoot(sound, channel)

    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #rotates the image to be the correct angle
        rotated_img = pygame.transform.rotate(self.img, self.angle)

        #displays the rotated image at the player's position
        screen.blit(rotated_img, (self.x - camera.x_offset - int(rotated_img.get_width() / 2), self.y - camera.y_offset - int(rotated_img.get_height() / 2)))

        #displays the child lasers if the player is alive
        for laser in self.lasers:

                if self.dead == False:

                        laser.draw(screen, camera)

    #Draws the HUD elements
    def HUD(self, screen):

        #draws ammo bars
        for i in range(0, self.ammo):

                pygame.draw.rect(screen, (104, 233, 255), pygame.Rect(4, 344 + (28 * i), 20, 20))



    #update method, using some trig to get the angles right for movement
    def update(self, screen_width, screen_height):

        #sets angle velocity based on whether or not the player is turning right or left
        if self.turning_right and not self.turning_left:

                self.angle_velocity = -self.turning_speed

        elif self.turning_left and not self.turning_right:

                self.angle_velocity = self.turning_speed

        #adds the angle velocity to the angle value
        self.angle += self.angle_velocity

        #gradually decrease angle velocity
        if self.angle_velocity != 0:

                if self.angle_velocity > 0:

                        if self.angle_velocity - self.angle_friction <= 0:

                                self.angle_velocity = 0
                        
                        else:

                                self.angle_velocity -= self.angle_friction
                
                else:

                        if self.angle_velocity + self.angle_friction >= 0:

                                self.angle_velocity = 0

                        else:

                                self.angle_velocity += self.angle_friction

                if self.angle_velocity > 0:

                        if self.angle_velocity - self.angle_friction < 0:

                                self.angle_velocity = 0
                        
                        else:

                                self.angle_velocity -= self.angle_friction
                
                else:

                        if self.angle_velocity + self.angle_friction > 0:

                                self.angle_velocity = 0

                        else:

                                self.angle_velocity += self.angle_friction

        #accelerates the velocity of the player based on its movement state
        if self.moving_forward == True and self.slowing_down == False:

                self.current_vector = self.angle

                if self.speed < self.top_speed:

                        if self.speed + self.acceleration >= self.top_speed:

                                self.speed = self.top_speed

                        else:

                                self.speed += self.acceleration

        else:

                if self.speed > 0:

                        if self.speed - self.acceleration <= 0:

                                self.speed = 0

                        else:

                                self.speed -= self.acceleration
                
        
        #uses trig to get which way to move given the angle and speed
        self.x_velocity = self.speed * math.sin(math.radians(self.current_vector + 180))
        self.y_velocity = self.speed * math.cos(math.radians(self.current_vector + 180))

        #adds the previous velocity to the current velocity
        self.x_velocity += self.previous_x_velocity
        self.y_velocity += self.previous_y_velocity

        #caps the speed
        if self.speed > 0:

                total_speed = math.sqrt((self.x_velocity ** 2) + (self.y_velocity ** 2))
                if total_speed > self.top_speed:

                        vector = math.atan2(self.y_velocity, self.x_velocity)
                        self.x_velocity = self.top_speed * math.cos(vector)
                        self.y_velocity = self.top_speed * math.sin(vector)


        #stores the current velocity for next frame
        self.previous_x_velocity = self.x_velocity
        self.previous_y_velocity = self.y_velocity

        #updates player position
        self.x += self.x_velocity
        self.y += self.y_velocity

        #keeps player inside the play area
        if self.x >= screen_width * 2:

                self.x = screen_width * 2
                self.previous_x_velocity = 0

        elif self.x <= 0:

                self.x = 0
                self.previous_x_velocity = 0

        if self.y >= screen_height * 2:

                self.y = screen_height * 2
                self.previous_y_velocity = 0

        elif self.y <= 0:

                self.y = 0
                self.previous_y_velocity = 0

        #updates child lasers and checks if they need deletion
        for laser in self.lasers:

                laser.update()
                
                if laser.age >= 50:

                        self.lasers.remove(laser)

        #decreases laser timer
        if self.laser_timer != 0:

                self.laser_timer -= 1

    #method for detecting asteroid collisions
    def detect_collision(self, asteroid):

        player_collider = pygame.Rect(0, 0, 40, 40)
        player_collider.centerx = self.x
        player_collider.centery = self.y

        asteroid_collider = pygame.Rect(0, 0, 40, 40)
        asteroid_collider.centerx = asteroid.x
        asteroid_collider.centery = asteroid.y
        
        if player_collider.colliderect(asteroid_collider):

                print("asteroid has collided with player") 
                self.dead = True