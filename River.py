from phevaluator.evaluator import evaluate_cards
from DeckBuilder import Deck
from settings import *
from GameLogger import GameLogger

class Dealer:
    """
    Manages the card dealing and round progression in a Texas Hold'em game.

    Attributes:
        deck (Deck): An instance of the Deck class.
        flop (bool): Flag to check if the flop has been dealt.
        river (list): The community cards on the table.
        highest_bet (int): The current highest bet amount.
        pot (int): The current total of chips bet in the round.
        small_blind (int): The amount of the small blind.
        small_blind_player (int): Index of the player who is the small blind.
        player_list (list): List of Player objects participating in the game.
        player_count (int): Total number of players.
        num_active_players (int): Number of players not folded.
        current_player_index (int): Index of the current player.
        can_deal (bool): Flag to check if dealing can continue.
        dealt_cards (int): Count of cards dealt to players this round.
        winners (list): Indices of players who have won the round.
        round_finished (bool): Flag to check if the round has concluded.
        button (int): Index of the player who is the button.
    """

    def __init__(self, players):
        """
        Initializes the Dealer with a list of players and prepares the game for starting.

        Parameters:
            players (list): List of players who will be participating in the game.
        """
        self.deck = Deck()
        self.logger = GameLogger()  # Initialize the logger
        self.flop = False
        self.river = []
        self.pot = 0
        self.small_blind = 1
        self.player_list = players
        self.player_count = len(self.player_list)
        self.all_bets = [0] * self.player_count
        self.num_active_players = len(self.player_list)
        self.current_player_index = 0
        self.can_deal = True
        self.dealt_cards = 0
        self.winners = []
        self.round_finished = False
        self.button = 0 #person located after the blinds and the one who starts the rounds
        self.game_stage = "Setup" # Initialize the game stage

    def add_player(self, player):
        """ Adds a new player to the game table if the maximum player limit has not been reached."""
        if self.player_count < MAX_PLAYERS:
            self.player_list.append(player)
            self.player_count = len(self.player_list)
        else:
            print("Cannot Add Player")
    
    def remove_player(self, player_name):
        """ Removes a player from the game table based on the player's name."""
        removed = False
        for player in self.player_list:
            if player.name == player_name:
                self.player_list.remove(player)
                del player
                removed = True
                self.player_count = len(self.player_list)
        if removed == False:
            print("Player Not Found.")
    
    def get_highest_bet(self):
        """ Updates the highest bet from all player bets."""
        bet_list = []
        for player in self.player_list:
            bet_list.append(player.bet)
        self.highest_bet = max(bet_list)

    def update_bets(self):
        for i in range(len(self.player_list)):
            self.all_bets[i] = self.player_list[i].total_bet

        
    def set_player_bet_gaps(self):
        """ Updates each player's bet gap based on the highest bet."""
        for player in self.player_list:
            player.bet_gap = self.highest_bet - player.bet


    # sets small blind
    def set_small_blind(self, amount):
        self.small_blind = amount

    # adds bet_raise to the pot
    def player_bet(self, player, bet):
        """
        Processes a player's bet, adds the bet to the pot, and updates bet statuses.

        Parameters:
            player (Player): The player making the bet.
            bet (int): The amount of the bet.
        """
        if bet > player.chips:
            print("Insufficient chips.")
            return
        player.bet_raise(bet)
        self.pot += bet
        #checking if bets have changed and setting them
        self.get_highest_bet()
        self.set_player_bet_gaps()
        self.update_bets()
        # resets check status from other players
        for play in self.player_list:
            if play != player and not(play.fold) and not(play.all_in) and play.check:
                play.reverse_check()

    
    # function for adding player matching bet to the pot
    def player_call(self, player):
        """ Processes a player's call, adding the required bet to match the highest bet to the pot."""
        player.call_hand()
        self.pot += player.bet_gap

    def deal_player_cards(self):
        """Deals two cards to each player and sets their position based on predefined settings."""
        for player in self.player_list:
            new_card = self.deck.deal_card()
            if self.dealt_cards < self.player_count:
                new_card.position = CARDS_1[self.dealt_cards]
            else:
                new_card.position = CARDS_2[self.dealt_cards - self.player_count]
            player.hand.append(new_card)
            self.dealt_cards += 1
        self.game_stage = "Pre-Flop"
    
    # Function to check if players have concluded their turns
    def players_status(self):
        """Checks if all players have checked to conclude the betting round."""
        for player in self.player_list:
            if player.check == False:
                return False
        return True

    # deals flops
    def deal_flop(self):
        """Deals the first three community cards (flop) to the table."""
        for i in range(3):
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[i], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
        self.flop = True
        self.game_stage = "Flop" # Changed to Flop
        #for player in self.player_list:
            #print(player.name + " " + f"{player.hand[0].rank}{player.hand[0].suit}" + " " + f"{player.hand[1].rank}{player.hand[1].suit}")

    # deals the other 2 cards after flop
    def deal_after_flop(self):
        """Continues dealing community cards after the flop until all five are dealt."""
        if self.dealt_cards <= (self.player_count * 2) + 5:
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[self.dealt_cards - self.player_count * 2], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
            if self.dealt_cards == (self.player_count * 2) + 5:
                self.can_deal = False

    def deal_turn(self):
        """Deals the fourth community card (turn)."""
        if len(self.river) == 3:  # Ensures the turn is dealt after the flop
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[3], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
            self.game_stage = "Turn" # Changed to Flop

    def deal_river(self):
        """Deals the fifth community card (river)."""
        if len(self.river) == 4:  # Ensures the river is dealt after the turn
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[4], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
            self.can_deal = False
            self.game_stage = "River" # Changed to River

    def decide_winner(self):
        """
        Evaluates all players' hands to determine the winner(s) of the round by 
        using the phevaluator library to calculate the hand ranks.
        """
        self.game_stage = "Showdown" # Changed to Showdown
        for player in self.player_list:
            player_cards = []
            if player.fold == False:
                for card in player.hand:
                    player_cards.append(f"{card.rank}{card.suit}")
                for card in self.river:
                    player_cards.append(f"{card.rank}{card.suit}")
                player.hand_rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                  player_cards[4], player_cards[5], player_cards[6])
        hand_ranks = []
        for i in range(len(self.player_list)):
            hand_ranks.append(self.player_list[i].hand_rank)  
        winners_list = []
        best_hand = min(hand_ranks)
        for i in range(len(hand_ranks)):
            #print(self.player_list[i].name + ": " + str(hand_ranks[i]))
            if best_hand == hand_ranks[i]:
                winners_list.append(i)
        for winner_index in winners_list:
            winner = self.player_list[winner_index]
            self.logger.log_winner(winner.name, self.pot /len(winners_list))   # Log each winner's share of the pot
        self.round_finished = True
        return winners_list

    # pays winning amount to designated playyer and removes from pot
    def pay_winnings(self, player, ammount):
        player.add_chips(ammount)
        self.pot -= ammount
    
    def get_current_stage(self):
        return self.game_stage

    # function to get table back to starting point so a new round can be started
    def reset_table(self):
        """Resets the table and all players for a new round."""
        for player in self.player_list:
            for _ in range(len(player.hand)):
                card = player.hand.pop()
                card.hide_card()
                self.deck.deck.append(card)
            player.reset_round()
        for _ in range(len(self.river)):
            card = self.river.pop()
            card.hide_card()
            self.deck.deck.append(card)
        #for card in self.deck:
        #    card.hide_card()

        self.winners = []
        self.deck.shuffle_deck()
        self.pot = 0
        self.dealt_cards = 0
        self.flop = False
        self.can_deal = True
        self.round_finished = False
        self.game_stage = "Pre-Flop"