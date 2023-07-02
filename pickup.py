#init stuff
import pygame
pygame.init()

#makes a class!
class Pickup:

    #this method is always called when a new instance of a class is created
    def __init__(self, img, x, y):
        
        #creating all the values the laser will need
        self.img = img

        self.x = x

        self.y = y

        self.picked_up = False

    #draw method, must be placed after background is drawn but before display is updated
    def draw(self, screen, camera):

        #displays the  image at the correct position
        screen.blit(self.img, (self.x - camera.x_offset - int(self.img.get_width() / 2), self.y - camera.y_offset - int(self.img.get_height() / 2)))

    #move method, using some trig to get the angles right for moving
    def collide(self, player, channel, sound):

        #checks if rects of player and pickup collide
        player_rect = pygame.Rect(0, 0, 40, 40)
        player_rect.center = (player.x, player.y)

        pickup_rect = pygame.Rect(0, 0, 40, 40)
        pickup_rect.center = (self.x, self.y)

        if player_rect.colliderect(pickup_rect):

            player.ammo = 7
            channel.play(sound)
            self.picked_up = True