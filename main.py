from settings import *
import ctypes, pygame, sys, pygame_widgets, random
from GameEngine import Poker
from Player import Player
from Tools import *
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox



ctypes.windll.user32.SetProcessDPIAware()


class Game:
    """
    Main class to initialize and run the Texas Hold'em poker game, handling game states, user inputs,
    and rendering the game interface.

    Attributes:
        screen (pygame.Surface): The main screen surface on which all game elements are drawn.
        clock (pygame.Clock): Clock used to manage game's frame rate.
        game_menu (bool): Flag to indicate if the game menu is active.
        player_name (str): Default player name, used if no input is given.
        game_state (str): Current state of the game, controls which part of the game logic is executed.
        player_num (int): Number of players in the game.
        players (list): List of Player objects participating in the game.
        starting_chips (int): Initial number of chips each player starts with.
        start_img, settings_img, quit_img, back_img (pygame.Surface): Surfaces for menu button images.
        start_button, settings_button, quit_button, back_button (Button): Button widgets for menu interactions.
        check_img, call_img, bet_img, fold_img (pygame.Surface): Surfaces for in-game action button images.
        check_button, call_button, bet_button, fold_button (Button): Button widgets for in-game actions.
    """

    def __init__(self):
        """
        General setup: Initializes the game environment, setting up the screen, loading images, and creating buttons.
        """
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
        self.small_blind = 1
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()
        self.textbox_active = False
        self.start_time = pygame.time.get_ticks()

        # Load images and create buttons for the main menu and in-game actions
        self.load_images()
        self.create_buttons()
        
    def run(self):
        """
        Main game loop that handles events, updates game state, and renders game elements.
        """
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
                    player_bet_output = TextBox(self.screen, 1490, 790, 80, 40, fontSize=20, colour=(255, 255, 255))
                    self.players.append(Player(self.player_name, self.starting_chips))

                    # creating table with players
                    for _ in range (self.player_num - 1):
                        self.players.append(Player(NAME_LIST[random.randint(0, 21)], self.starting_chips, True)) # True flag for NPC player
                    poker_game = Poker(self.players)
                    poker_game.dealer.set_small_blind(self.small_blind)

                    # textbox for player betting
                    player_bet_output = TextBox(self.screen, 1490, 790, 80, 40, fontSize=20, colour=(255, 255, 255))


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
                    blind_slider = Slider(self.screen, 700, 607, 300, 40, min=1, max=300, step=1, 
                                                colour = (255,255,255) , handleRadius = 25, initial = 1)
                    blind_output = TextBox(self.screen, 1050, 602, 100, 50, fontSize=30, colour = (255,255,255))
                    player_name_output = TextBox(self.screen, 680, 502, 400, 50, fontSize=30, colour = (255,255,255))

                # high scores button
                if self.high_scores_button.draw(self.screen):
                    self.game_state = "high_scores"

                
                # quit button
                if self.quit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
            

            # settings
            if self.game_state == "settings":
                draw_text(self.screen, "SETTINGS", 72, TEXT_COLOR, 600, 100)
                draw_text(self.screen, "Number of Players", 36, TEXT_COLOR, 300, 300)
                draw_text(self.screen, "Starting Chips", 36, TEXT_COLOR, 300, 400)
                draw_text(self.screen, "Player Name", 36, TEXT_COLOR, 300, 500)
                draw_text(self.screen, "Small Blind", 36, TEXT_COLOR, 300, 600)
                player_output.setText(player_slider.getValue())
                player_output.disable()
                chips_output.setText(chips_slider.getValue())
                chips_output.disable()
                blind_output.setText(blind_slider.getValue())
                blind_output.disable()
                self.player_name = player_name_output.getText()


                # saving values when returning to main menu
                if self.back_button_1.draw(self.screen):
                    self.game_state = "main_menu"
                    self.player_num = player_slider.getValue()
                    self.starting_chips = chips_slider.getValue()
                    self.small_blind = blind_slider.getValue()
                    del player_slider
                    del player_output
                    del chips_slider
                    del chips_output
                    del blind_slider
                    del blind_output
                    del player_name_output
            
            # high scores
            if self.game_state == "high_scores":
                draw_text(self.screen, "HIGH SCORES", 72, TEXT_COLOR, 550, 100)
                if self.back_button_1.draw(self.screen):
                    self.game_state = "main_menu"

            # in game
            if self.game_state == "in_game":

                # printing player cards and info into screen
                for i in range(poker_game.dealer.player_count):
                    # player names
                    draw_text(self.screen, poker_game.dealer.player_list[i].name, 24, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i])
                    # player chips
                    draw_text(self.screen, f"Chips: {poker_game.dealer.player_list[i].chips}", 20, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i] + 30)
                    # player cards
                    for card in poker_game.dealer.player_list[i].hand:
                        card.render_card(self.screen)
                    # pot
                    draw_text(self.screen, f"POT: {poker_game.dealer.pot}", 28, TEXT_COLOR, 780, 400)
                    draw_text(self.screen, "Button", 14, (0,0,0), PLAYER_X[poker_game.start_turn] - 80, PLAYER_Y[poker_game.start_turn] - 30)
                    draw_text(self.screen, f"BET: {poker_game.dealer.player_list[i].total_bet}", 20, TEXT_COLOR, PLAYER_X[i], PLAYER_Y[i] + 60)
                    draw_text(self.screen, poker_game.dealer.get_current_stage(), 40, (255,255,10), 20, 650)
                    draw_text(self.screen, "TURN", 18, (255,0,0), PLAYER_X[poker_game.turn % poker_game.dealer.player_count] - 80, PLAYER_Y[poker_game.turn % poker_game.dealer.player_count] - 50)
                    if poker_game.dealer.player_list[i].all_in:
                        draw_text(self.screen, "ALL IN", 32, (250,0,0), PLAYER_X[i], PLAYER_Y[i] - 30)
                    elif poker_game.dealer.player_list[i].fold:
                        draw_text(self.screen, "FOLDED", 20, (0,0,0), PLAYER_X[i], PLAYER_Y[i] - 30)
                    elif poker_game.dealer.player_list[i].has_called:
                        draw_text(self.screen, "CALL", 20, (0,0,0), PLAYER_X[i], PLAYER_Y[i] - 30)
                    elif poker_game.dealer.player_list[i].has_bet:
                        draw_text(self.screen, f"BET + {poker_game.dealer.player_list[i].bet}", 20, (0,0,230), PLAYER_X[i], PLAYER_Y[i] - 30)
                    elif poker_game.dealer.player_list[i].check:
                        draw_text(self.screen, "CHECK", 20, (0,0,0), PLAYER_X[i], PLAYER_Y[i] - 30)
                    if poker_game.dealer.player_list[i].winner:
                        draw_text(self.screen, "WINNER", 32, (0,0,0), PLAYER_X[i] - 15, PLAYER_Y[i] - 220)
                    


                # Update the TextBox based on events
                for event in events: 
                    #print(f"Textbox active: {textbox_active}")
    
                # Check if mouse clicked inside TextBox
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if 1490 <= event.pos[0] <= 1490 + 80 and 790 <= event.pos[1] <= 790 + 40:
                            textbox_active = True
                            print("Textbox clicked!")
                        else :
                            textbox_active = False
                # Keep updating TextBox while it's active
                    if textbox_active:
                        if event.type == pygame.KEYDOWN:
                            if pygame.K_0 <= event.key <= pygame.K_9 or event.key == pygame.K_BACKSPACE:
                                player_bet_output.listen(event)

                                bet_input = player_bet_output.get_text()

                                try:
                                    bet_amount = int(bet_input)

                                    bet_amount = min(bet_amount, poker_game.dealer.player_list[0].chips)
                                except ValueError:
                                    print("Invalid input! Please enter a valid number.")


                # printing river cards
                for card in poker_game.dealer.river:
                    card.render_card(self.screen)


                # player actions
                # check
                if poker_game.dealer.player_list[0].bet_gap == 0:
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
                            poker_game.dealer.player_call(poker_game.dealer.player_list[0])
                        else:
                            poker_game.dealer.player_list[0].bet_raise(poker_game.dealer.player_list[0].chips)

                        if(poker_game.dealer.player_list[0].check == True):
                            poker_game.pass_turn()

  
                # raise/bet
                if self.bet_button.draw(self.screen) and event.type == pygame.MOUSEBUTTONDOWN:
                    if (poker_game.turn % poker_game.dealer.player_count) == 0 and poker_game.dealer.player_list[0].check == False:
                        try:
                            bet_amount = int(player_bet_output.getText())
                            if bet_amount > poker_game.dealer.player_list[0].chips:
                                print("Not enough chips!")
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

                # starting a new round on a button press
                
                if poker_game.dealer.dealt_cards == (len(poker_game.dealer.player_list)*2) + 5 and poker_game.dealer.players_status():
                    # prints deal cards button
                    if self.deal_button.draw(self.screen):
                        # remove npc player if they reach 0 chips
                        players_to_remove =[]
                        for player in poker_game.dealer.player_list:
                            if player.NPC and player.chips == 0:
                                players_to_remove.append(player.name)
                        for player in players_to_remove:
                            poker_game.dealer.remove_player(player)

                        #starts a new table if main_player is the only player left
                        if poker_game.dealer.player_count < 2:
                            main_player = poker_game.dealer.player_list[0]
                            self.players = []
                            self.players.append(main_player)
                            for i in range(self.player_num - 1):
                                self.players.append(Player(NAME_LIST[i], main_player.chips, True))
                            poker_game = Poker(self.players)
                            poker_game.turn = 0
                        
                        # restart table
                        poker_game.increment_button()
                        poker_game.dealer.reset_table()
                        poker_game.toggle_blind()

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

    def load_images(self):
        """
        Loads images for all buttons used in the game.
        """
        self.start_img = pygame.image.load("menu_buttons/start_button.png").convert_alpha()
        self.settings_img = pygame.image.load("menu_buttons/settings_button.png").convert_alpha()
        self.quit_img = pygame.image.load("menu_buttons/quit_button.png").convert_alpha()
        self.high_scores_img = pygame.image.load("menu_buttons/high_scores_button.png").convert_alpha()
        self.back_img = pygame.image.load("menu_buttons/back_button.png").convert_alpha()
        self.check_img = pygame.image.load("menu_buttons/check_button.png").convert_alpha()
        self.call_img = pygame.image.load("menu_buttons/call_button.png").convert_alpha()
        self.bet_img = pygame.image.load("menu_buttons/bet_button.png").convert_alpha()
        self.fold_img = pygame.image.load("menu_buttons/fold_button.png").convert_alpha()
        self.back_img_2 = pygame.transform.scale_by(self.back_img, 0.8)
        self.deal_img = pygame.image.load("menu_buttons/deal_button.png").convert_alpha()

    
    
    def create_buttons(self):
        """
        Creates button widgets for all actions in the game.
        """
        # loading player action buttons
        self.start_button = Button(650, 300, self.start_img, 1)
        self.settings_button = Button(650, 500, self.settings_img, 1)
        self.quit_button = Button(650, 700, self.quit_img, 1)
        self.high_scores_button = Button(300, 500, self.high_scores_img, 1)
        self.back_button_1 = Button(150, 700, self.back_img, 1)
        self.back_button_2 = Button(10, 820, self.back_img_2, 1)
        self.check_button = Button(1095, 840, self.check_img, 1)
        self.call_button = Button(1220, 840, self.call_img, 1)
        self.bet_button = Button(1345, 840, self.bet_img, 1)
        self.fold_button = Button(1470, 840, self.fold_img, 1)
        self.deal_button = Button(10, 700, self.deal_img, 1)
    
if __name__ == '__main__':
    game = Game()
    game.run()