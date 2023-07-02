#init stuff
import pygame
import math

pygame.init()

#makes a class!
class Asteroid:

    #this method is always called when a new instance of a class is created
    def __init__(self, img, x, y, vector, rotation_speed, speed):
        
        #creating all the values the asteroid will need
        self.img = img

        self.x = x

        self.y = y

        self.angle = 0

        self.vector = vector

        self.rotation_speed = rotation_speed

        self.speed = speed

    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #rotates the image to be the correct angle
        rotated_img = pygame.transform.rotate(self.img, self.angle)

        #displays the rotated image at the player's position
        screen.blit(rotated_img, (self.x - camera.x_offset - int(rotated_img.get_width() / 2), self.y - camera.y_offset - int(rotated_img.get_height() / 2)))

    #update method, using some trig to get the angles right for movement
    def update(self):

        #uses trig to get which way to move given the angle and speed
        self.x_velocity = self.speed * math.sin(math.radians(self.vector + 180))
        self.y_velocity = self.speed * math.cos(math.radians(self.vector + 180))

        #updates asteroid position
        self.x += self.x_velocity
        self.y += self.y_velocity

        #rotates asteroid
        self.angle += self.rotation_speed

    #checks to see if the asteroid is out of bounds
    def position_check(self, screen_width, screen_height):

        if self.x > (screen_width * 2) + 300 or self.x < -300 or self.y > (screen_height * 2) + 300 or self.y < -300:

            return True
        
        else:

            return False

    #checks for collisions with lasers
    def detect_collision(self, lasers):

        for laser in lasers:

            asteroid_collider = pygame.Rect(0, 0, 40, 40)
            asteroid_collider.center = (self.x, self.y)

            laser_collider = pygame.Rect(0, 0, 40, 40)
            laser_collider.center = (laser.x, laser.y)
            
            if asteroid_collider.colliderect(laser_collider):

                    print("laser has hit asteroid")
                    return True
                    break