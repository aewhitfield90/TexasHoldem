from settings import *
import ctypes, pygame, sys, pygame_widgets
from GameEngine import Poker
from Player import Player
from Tools import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("POKER GAME")
        self.clock = pygame.time.Clock()
        self.game_menu = True
        self.player_name = "PLAYER"
        self.game_state = "main_menu"
        self.player_num = 2
        self.players = []
        self.starting_chips = 1000
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()
        
        #loading options images
        self.start_img = pygame.image.load("menu_buttons/start_button.png").convert_alpha()
        self.settings_img = pygame.image.load("menu_buttons/settings_button.png").convert_alpha()
        self.quit_img = pygame.image.load("menu_buttons/quit_button.png").convert_alpha()
        self.back_img = pygame.image.load("menu_buttons/back_button.png").convert_alpha()
        self.start_button = Button(650, 300, self.start_img, 1)
        self.settings_button = Button(650, 500, self.settings_img, 1)
        self.quit_button = Button(650, 700, self.quit_img, 1)
        self.back_button = Button(150, 700, self.back_img, 1)

        #options sliders
        self.player_slider = Slider(self.screen, 700, 307, 300, 40, min=2, max=MAX_PLAYERS, step=1, 
                                colour = (255,255,255), handleRadius = 25, initial = self.player_num)
        self.player_output = TextBox(self.screen, 1050, 302, 100, 50, fontSize=30, colour = (255,255,255))
        self.chips_slider = Slider(self.screen, 700, 407, 300, 40, min=200, max=10000, step=100, 
                                colour = (255,255,255) , handleRadius = 25, initial = self.starting_chips)
        self.chips_output = TextBox(self.screen, 1050, 402, 100, 50, fontSize=30, colour = (255,255,255))


    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #events = pygame.event.get()

            #main menu
            if self.game_state == "main_menu":
                draw_text(self.screen, "POKER GAME", 72, TEXT_COLOR, 500, 100)

                # start game button
                if self.start_button.draw(self.screen):
                    self.game_state = "in_game"
                    self.players.append(Player(self.player_name, self.starting_chips))
                    #creating table with players
                    for i in range (self.player_num - 1):
                        self.players.append(Player(NAME_LIST[i], self.starting_chips))
                    poker_game = Poker(self.players)

                # settings button
                if self.settings_button.draw(self.screen):
                    self.game_state = "settings"

                # quit button
                if self.quit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
            
            #settings
            if self.game_state == "settings":
                draw_text(self.screen, "SETTINGS", 72, TEXT_COLOR, 600, 100)
                draw_text(self.screen, "Number of Players", 36, TEXT_COLOR, 300, 300)
                draw_text(self.screen, "Starting Chips", 36, TEXT_COLOR, 300, 400)
                self.player_output.setText(self.player_slider.getValue())
                self.player_output.disable()
                self.chips_output.setText(self.chips_slider.getValue())
                self.chips_output.disable()
                pygame_widgets.update(event)
                
                #saving values when returning to main menu
                if self.back_button.draw(self.screen):
                    self.game_state = "main_menu"
                    self.player_num = self.player_slider.getValue()
                    self.starting_chips = self.chips_slider.getValue()

            #in game
            if self.game_state == "in_game":
                #for card in poker_game.dealer.deck.deck:
                    #card.render_card(self.screen)
                for i in range(self.player_num):
                    draw_text(self.screen, poker_game.dealer.player_list[i].name, 24, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i])
                    for card in poker_game.dealer.player_list[i].hand:
                        card.render_card(self.screen)
                for card in poker_game.dealer.river:
                    card.render_card(self.screen)
                if len(poker_game.dealer.winners) > 0:
                    winners = ""
                    for i in poker_game.dealer.winners:
                        winners += poker_game.dealer.player_list[i].name + " "
                    draw_text(self.screen, winners + " WINS! ", 40, TEXT_COLOR, 700, 50)
                poker_game.update()

            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame.display.update()
            self.screen.fill(BACKGROUND_COLOR)

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()