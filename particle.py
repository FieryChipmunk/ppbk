#init stuff
import pygame
import math

pygame.init()

#makes a new class
class Particle:

    #this method is always called when a new instance of a class is created
    def __init__(self, img, x, y, vector, speed, lifetime):
        
        #creating all the values the particle needs
        self.img = img

        self.x = x

        self.y = y

        self.vector = vector

        self.speed = speed

        self.lifetime = lifetime
        
        self.time_expired = 0

        self.dead = False

    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #sizes image based on how old the particle is
        age_fraction = (self.lifetime - self.time_expired) / self.lifetime
        if age_fraction < 0:
            
            age_fraction = 0

        alpha_edit_img = self.img
        alpha_edit_img.set_alpha(255 * age_fraction)

        #displays the rotated image at the player's position
        screen.blit(alpha_edit_img, (self.x - camera.x_offset - int(self.img.get_width() / 2), self.y - camera.y_offset - int(self.img.get_height() / 2)))

    #update method, moves the particle and checks its age
    def update(self):

        #updates particle position by using sum trig
        self.x += self.speed * math.sin(math.radians(self.vector + 180))
        self.y += self.speed * math.cos(math.radians(self.vector + 180))

        #checks to see if particle is too old, and if it is, kills it
        self.time_expired += 1

        if self.time_expired >= self.lifetime:

                self.dead = True