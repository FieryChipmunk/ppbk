#init stuff
import pygame
import math

pygame.init()

#makes a class!
class Laser:

    #this method is always called when a new instance of a class is created
    def __init__(self, img, x, y, angle, speed):
        
        #creating all the values the laser will need
        self.img = img

        self.x = x

        self.y = y

        self.angle = angle

        self.speed = speed

        self.age = 0
    
    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #rotates the image to be the correct angle
        rotated_img = pygame.transform.rotate(self.img, self.angle)

        #displays the rotated image at the player's position
        screen.blit(rotated_img, (self.x - camera.x_offset - int(rotated_img.get_width() / 2), self.y - camera.y_offset - int(rotated_img.get_height() / 2)))

    #move method, using some trig to get the angles right for moving
    def update(self):

        #updates laser position
        self.x += self.speed * math.sin(math.radians(self.angle + 180))
        self.y += self.speed * math.cos(math.radians(self.angle + 180))

        #increases age
        self.age += 1