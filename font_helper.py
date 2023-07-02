#init stuff
import pygame
import pygame.freetype

pygame.init()

#makes a class!
class Font_Helper:

    #this method is always called when a new instance of a class is created
    def __init__(self, font):

        self.font = font

    #displays text
    def display_text(self, text, x, y, screen):

        text = str(text)

        
        text_surface, text_rect = self.font.render(text, (104, 233, 255))
        text_surface = pygame.transform.scale(text_surface, (text_rect.width * 4, text_rect.height * 4))
        text_rect = text_surface.get_rect()
        x_offset = text_rect.right - text_rect.left
        screen.blit(text_surface, (x - x_offset - 12, y + 12))
