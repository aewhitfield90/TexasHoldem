#set of tools for user interaction with game and menus
import pygame
from settings import *

#Class to create interactable buttons
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self, surface):
        action = False
        position = pygame.mouse.get_pos()

        #check if mouse is over button and click conditions
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

def draw_text(screen, text, size, text_col, x, y):
        font = pygame.font.SysFont(GAME_FONT, size)
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))