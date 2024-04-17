class Player:
    def __init__(self, name = "N/A", starting_chips = 0,):
        self.name = name
        self.chips = starting_chips
        self.bet = 0
        self.bet_gap = 0
        self.hand = []
        self.NPC = False #placeholder flag for NPC
        self.fold = False
        self.check = False
        self.all_in = False
        self.hand_rank = 9999

    # placeholder function for setting a player as an NPC
    def NPC_toggle(self):
        self.NPC = True
    
    def fold_hand(self):
        self.fold = True
        self.check = True
        self.bet_gap = 0
    
    def bet_raise(self, amount):
        self.bet += amount
        self.chips -= amount
        self.check = True
        if self.chips == 0:
            self.all_in = True
    
    def set_bet_gap(self, gap):
        self.bet_gap = gap
    
    def call_hand(self):
        self.bet_raise(self.bet_gap)

    def check_hand(self):
        self.check = True
    
    def add_chips(self, winnings):
        self.chips += winnings

    def display_player_info(self):
        print('NAME: ' + self.name + '\n' +
              'CHIPS: ' + str(self.chips) + '\n' +
              'BET: ' + str(self.bet))

    def reset_turn(self):
        self.bet = 0
        self.bet_gap = 0
        if self.all_in == False and self.fold == False:
            self.check = False
    
    def reset_round(self):
        self.all_in = False
        self.fold = False
        self.reset_turn()
        self.hand_rank = 9999
