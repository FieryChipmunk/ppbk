#init stuff
import pygame

pygame.init()

#makes a class!
class Camera:

    #this method is always called when a new instance of a class is created
    def __init__(self, follow_object):
        
        self.x_offset = 0

        self.y_offset = 0
        
        self.calculated_x_offset = 0

        self.calculated_y_offset = 0

        self.follow_object = follow_object

    #updates the camera
    def update(self, screen_width, screen_height):

        self.calculated_x_offset += ((self.follow_object.x - (screen_width / 2)) - self.calculated_x_offset) / 10
        self.calculated_y_offset += ((self.follow_object.y - (screen_height / 2)) - self.calculated_y_offset) / 10
        
        self.x_offset = int(self.calculated_x_offset)
        self.y_offset = int(self.calculated_y_offset)