from settings import *
import ctypes, pygame, sys, pygame_widgets, pygame_textinput
from GameEngine import Poker
from Player import Player
from Tools import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):

        # General setup\
        self.textbox_active = False
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("POKER GAME")
        self.clock = pygame.time.Clock()
        self.game_menu = True
        self.player_name = "PLAYER"
        self.game_state = "main_menu"
        self.player_num = 5
        self.players = []
        self.starting_chips = 1000
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()
        
        # loading options images
        self.start_img = pygame.image.load("menu_buttons/start_button.png").convert_alpha()
        self.settings_img = pygame.image.load("menu_buttons/settings_button.png").convert_alpha()
        self.quit_img = pygame.image.load("menu_buttons/quit_button.png").convert_alpha()
        self.back_img = pygame.image.load("menu_buttons/back_button.png").convert_alpha()
        self.start_button = Button(650, 300, self.start_img, 1)
        self.settings_button = Button(650, 500, self.settings_img, 1)
        self.quit_button = Button(650, 700, self.quit_img, 1)
        self.back_button = Button(150, 700, self.back_img, 1)

        # loading player action buttons
        self.check_img = pygame.image.load("menu_buttons/check_button.png").convert_alpha()
        self.call_img = pygame.image.load("menu_buttons/call_button.png").convert_alpha()
        self.bet_img = pygame.image.load("menu_buttons/bet_button.png").convert_alpha()
        self.fold_img = pygame.image.load("menu_buttons/fold_button.png").convert_alpha()
        self.check_button = Button(1095, 840, self.check_img, 1)
        self.call_button = Button(1220, 840, self.call_img, 1)
        self.bet_button = Button(1345, 840, self.bet_img, 1)
        self.fold_button = Button(1470, 840, self.fold_img, 1)


    def run(self):
        player_bet_output = TextBox(self.screen, 1490, 790, 80, 40, fontSize=20, colour=(255, 255, 255))
        self.start_time = pygame.time.get_ticks()
        while True:
            textbox_active = False  # Flag to track if TextBox was clicked

            events = pygame.event.get()  # Get all pygame events
             
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # main menu
            if self.game_state == "main_menu":
                draw_text(self.screen, "POKER GAME", 72, TEXT_COLOR, 500, 100)

                # start game button
                if self.start_button.draw(self.screen):
                    self.game_state = "in_game"
                    self.players.append(Player(self.player_name, self.starting_chips))

                    # creating table with players
                    for i in range (self.player_num - 1):
                        self.players.append(Player(NAME_LIST[i], self.starting_chips))
                        self.players[i + 1].NPC_toggle()
                    poker_game = Poker(self.players)

            

                
                # settings button
                if self.settings_button.draw(self.screen):
                    self.game_state = "settings"

                    # options sliders
                    player_slider = Slider(self.screen, 700, 307, 300, 40, min=2, max=MAX_PLAYERS, step=1, 
                                                colour = (255,255,255), handleRadius = 25, initial = self.player_num)
                    player_output = TextBox(self.screen, 1050, 302, 100, 50, fontSize=30, colour = (255,255,255))
                    chips_slider = Slider(self.screen, 700, 407, 300, 40, min=200, max=10000, step=100, 
                                                colour = (255,255,255) , handleRadius = 25, initial = self.starting_chips)
                    chips_output = TextBox(self.screen, 1050, 402, 100, 50, fontSize=30, colour = (255,255,255))

                # quit button
                if self.quit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
            
            # settings
            if self.game_state == "settings":
                draw_text(self.screen, "SETTINGS", 72, TEXT_COLOR, 600, 100)
                draw_text(self.screen, "Number of Players", 36, TEXT_COLOR, 300, 300)
                draw_text(self.screen, "Starting Chips", 36, TEXT_COLOR, 300, 400)
                player_output.setText(player_slider.getValue())
                player_output.disable()
                chips_output.setText(chips_slider.getValue())
                chips_output.disable()
                pygame_widgets.update(event)
                
                # saving values when returning to main menu
                if self.back_button.draw(self.screen):
                    self.game_state = "main_menu"
                    self.player_num = player_slider.getValue()
                    self.starting_chips = chips_slider.getValue()
                    del player_slider
                    del player_output
                    del chips_slider
                    del chips_output

            # in game
            if self.game_state == "in_game":
                
                # printing player cards into screen
                for i in range(self.player_num):
                    # player names
                    draw_text(self.screen, poker_game.dealer.player_list[i].name, 24, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i])
                    # player chips
                    draw_text(self.screen, f"Chips: {poker_game.dealer.player_list[i].chips}", 20, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i] + 30)
                    # player cards
                    for card in poker_game.dealer.player_list[i].hand:
                        card.render_card(self.screen)
                    # pot
                    draw_text(self.screen, f"POT: {poker_game.dealer.pot}", 28, TEXT_COLOR, 780, 400)


                # Update the TextBox based on events
                for event in events: 
                    print(f"Textbox active: {textbox_active}")
    
                # Check if mouse clicked inside TextBox
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 1490 <= event.pos[0] <= 1490 + 80 and 790 <= event.pos[1] <= 790 + 40:
                            textbox_active = True
                            print("Textbox clicked!")
                        else :
                            textbox_active = False
                # Keep updating TextBox while it's active
                    if textbox_active:
                        player_bet_output.listen(event)


                # printing river cards
                for card in poker_game.dealer.river:
                    card.render_card(self.screen)

                # skip folded or all in player
                if ((poker_game.turn % poker_game.dealer.player_count) == 0 and not(poker_game.dealer.players_status()) 
                     and (poker_game.dealer.player_list[0].fold == True or (poker_game.dealer.player_list[0].all_in == True))):
                    poker_game.pass_turn()

                # player actions
                # check
                if self.check_button.draw(self.screen):
                    if ((poker_game.turn % poker_game.dealer.player_count) == 0 and poker_game.dealer.player_list[0].bet_gap == 0 
                                                                                and poker_game.dealer.player_list[0].check == False):
                        poker_game.dealer.player_list[0].check_hand()
                        
                        if(poker_game.dealer.player_list[0].check == True):
                            poker_game.pass_turn()
                    
                # call
                if self.call_button.draw(self.screen):
                    if (poker_game.turn % poker_game.dealer.player_count) == 0 and poker_game.dealer.player_list[0].check == False:
                        if poker_game.dealer.player_list[0].chips >= poker_game.dealer.player_list[0].bet_gap:
                            poker_game.dealer.player_bet(poker_game.dealer.player_list[0], poker_game.dealer.player_list[0].bet_gap)
                        else:
                            poker_game.dealer.player_list[0].bet_raise(poker_game.dealer.player_list[0].chips)

                        if(poker_game.dealer.player_list[0].check == True):
                            poker_game.pass_turn()

                bet_input = player_bet_output.getText()
                if bet_input:
                    bet_amount = min(int(bet_input), poker_game.dealer.player_list[0].chips)
                else:
                    bet_amount = 0
                    
                # raise/bet
                if self.bet_button.draw(self.screen) and event.type == pygame.MOUSEBUTTONDOWN:
                    if (poker_game.turn % poker_game.dealer.player_count) == 0 and poker_game.dealer.player_list[0].check == False:
                        try:
                            bet_amount = int(player_bet_output.getText())
                            if bet_amount > poker_game.dealer.player_list[0].chips:
                                print("Not enough chips!")
                                return  # Exit early if not enough chips
                            poker_game.dealer.player_bet(poker_game.dealer.player_list[0], bet_amount)
                            player_bet_output.setText(str(bet_amount + 15))
                            if poker_game.dealer.player_list[0].check == True:
                                poker_game.pass_turn()
                        except ValueError:
                            print("Invalid bet amount!")

                # fold
                if self.fold_button.draw(self.screen):
                    if (poker_game.turn % poker_game.dealer.player_count) == 0 and poker_game.dealer.player_list[0].check == False:
                        poker_game.dealer.player_list[0].fold_hand()
                        
                        if(poker_game.dealer.player_list[0].check == True):
                            poker_game.pass_turn()

                # checking for winner and announcing it
                if len(poker_game.dealer.winners) > 0:
                    winner = 0
                    if len(poker_game.dealer.winners) == 1:
                        winner = poker_game.dealer.winners[0]
                        draw_text(self.screen, f"{poker_game.dealer.player_list[winner].name} WINS! ", 40, TEXT_COLOR, 650, 50)
                    else:
                        draw_text(self.screen, "ITS A TIE! SPLIT POT!", 40, TEXT_COLOR, 600, 50)
                
                poker_game.update()

                # starting a new round on a key press [W] (should be changed to time based or a button)
                if poker_game.dealer.dealt_cards == (len(poker_game.dealer.player_list)*2) + 5:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_w] == True:
                        poker_game.dealer.reset_table()
                        # quits game if player runs out of chips
                        if (poker_game.dealer.player_list[0].chips == 0):
                            self.game_state = "main_menu"
                            del player_bet_output
                            del poker_game
                            self.players = []
                            

            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()
            pygame_widgets.update(events)
            pygame.display.update()
            self.screen.fill(BACKGROUND_COLOR)

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()