class Player:

    """
    Represents a player in the Texas Hold'em game, handling their chips, betting status, and actions.

    Attributes:
        name (str): The player's name.
        chips (int): Total chips available to the player for betting.
        bet (int): Current amount bet by the player in a round.
        bet_gap (int): Additional amount the player needs to bet to match the current highest bet.
        hand (list): Cards in the player's hand.
        NPC (bool): Flag indicating whether the player is controlled by the computer.
        fold (bool): Flag indicating whether the player has folded the round.
        check (bool): Flag indicating whether the player has checked.
        all_in (bool): Flag indicating whether the player has put all their chips in.
        hand_rank (int): Numerical ranking of the player's hand.
    """
       
    def __init__(self, name = "N/A", starting_chips = 0, NPC = False):
        """
        Initializes a new player with the provided name and starting chips.

        Parameters:
        name (str): The name of the player.
        starting_chips (int): The initial amount of chips the player starts with.
        """
        self.name = name
        self.chips = starting_chips
        self.bet = 0
        self.bet_gap = 0
        self.total_bet = 0
        self.hand = []
        self.NPC = NPC #placeholder flag for NPC
        self.fold = False
        self.check = False
        self.all_in = False
        self.has_bet = False
        self.has_called = False
        self.hand_rank = 9999
        self.winner = False
        self.small_blind = False
        self.big_blind = False
        self.button = False
        #variables to delay npc actions
        self.can_act = False
        self.last_act_time = 0

    # placeholder function for setting a player as an NPC
    def NPC_toggle(self):
        """ Toggle the NPC status to True, indicating this player is controlled by the computer."""
        self.NPC = True
    
    def fold_hand(self):
        """
        Handles the player's action to fold their hand, forfeiting the round.
        """
        self.fold = True
        self.check = True
        self.bet_gap = 0
    
    def bet_raise(self, amount):
        """
        Increases the player's bet by the specified amount and deducts the same from their chips.
        If the player runs out of chips, they are marked as all-in.

        Parameters:
            amount (int): The amount to add to the current bet.
        """
        self.bet += amount
        self.total_bet += amount
        self.chips -= amount
        self.has_bet = True
        self.check = True
        if self.chips == 0:
            self.all_in = True
    
    def set_bet_gap(self, gap):
        """
        Sets the bet gap, which is the amount needed to call to match the current highest bet.

        Parameters:
            gap (int): The amount required to match the current bet.
        """
        self.bet_gap = gap
    
    def call_hand(self):
        self.has_called = True
        """ Executes a call action, matching the current highest bet by betting the bet gap."""
        if self.chips > self.bet_gap:
            self.bet_raise(self.bet_gap)
        else:
            self.bet_raise(self.chips)

    def check_hand(self):
        """ Sets the player's status to checked, indicating no betting action this turn."""
        self.check = True
        self.check = True
    
    # sets check to false and other conditions to have the turn again
    def reverse_check(self):
        if self.check == True:
            self.check = False
        if self.has_called == True:
            self.has_called = False
        self.can_act = False
        self.last_act_time = 0
    
    def add_chips(self, winnings):
        """
        Adds the specified amount of chips to the player's total.

        Parameters:
            winnings (int): The amount of chips to be added.
        """
        self.chips += winnings

    def display_player_info(self):
        """ Prints the player's name, chip count, and current bet to the console."""
        print('NAME: ' + self.name + '\n' +
              'CHIPS: ' + str(self.chips) + '\n' +
              'BET: ' + str(self.bet))
    
    def toggle_action(self):
        self.can_act = True
    
    def set_act_time(self, time):
        self.last_act_time = time
    
    def toggle_winner(self):
        self.winner = True
    
    def set_small_blind(self):
        self.small_blind = True

    def set_big_blind(self):
        self.big_blind = True

    def set_button(self):
        self.button = True

    def reset_turn(self):
        """
        Resets the player's turn status, clearing bets and bet gaps, unless they are all-in.
        """
        self.bet = 0
        self.bet_gap = 0
        self.can_act = False
        self.has_bet = False
        self.has_called = False
        self.last_act_time = 0
        if self.all_in == False and self.fold == False:
            self.check = False
        
    
    def reset_round(self):
        """
        Resets the player's round status, including folding and all-in statuses, and hand rank.
        """
        self.all_in = False
        self.fold = False
        self.reset_turn()
        self.hand_rank = 9999
        self.total_bet = 0
        self.winner = False
        self.small_blind = False
        self.big_blind = False
        self.button = False
