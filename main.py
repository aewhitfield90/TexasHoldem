from settings import *
import ctypes, pygame, sys
from GameEngine import Poker

ctypes.windll.user32.SetProcessDPIAware()

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

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("POKER GAME")
        self.clock = pygame.time.Clock()
        self.game_menu = True
        self.game_state = "main_menu"
        
        #loading main menu images
        self.start_img = pygame.image.load("menu_buttons/start_button.png").convert_alpha()
        self.settings_img = pygame.image.load("menu_buttons/settings_button.png").convert_alpha()
        self.quit_img = pygame.image.load("menu_buttons/quit_button.png").convert_alpha()
        self.start_button = Button(650, 300, self.start_img, 1)
        self.settings_button = Button(650, 500, self.settings_img, 1)
        self.quit_button = Button(650, 700, self.quit_img, 1)

    #Funtion to draw texts on screen (e.g. Title)
    def draw_text(self, text, size, text_col, x, y):
        self.font = pygame.font.SysFont(GAME_FONT, size)
        self.img = self.font.render(text, True, text_col)
        self.screen.blit(self.img, (x, y))

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            if self.game_state == "main_menu":
                self.draw_text("POKER GAME", 72, TEXT_COLOR, 500, 100)
                if self.start_button.draw(self.screen):
                    print("start game")
                if self.settings_button.draw(self.screen):
                    self.game_state = "settings"
                if self.quit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
            
            if self.game_state == "settings":
                pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #if event.type == pygame.


            
            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame.display.update()
            self.screen.fill(BACKGROUND_COLOR)

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()