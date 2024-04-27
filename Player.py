class Player:
    def __init__(self, name = "N/A", starting_chips = 0, NPC = False):
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
        self.hand_rank = 9999
        self.winner = False
        #variables to delay npc actions
        self.can_act = False
        self.last_act_time = 0

    # placeholder function for setting a player as an NPC
    def NPC_toggle(self):
        self.NPC = True
    
    def fold_hand(self):
        self.fold = True
        self.check = True
        self.bet_gap = 0
    
    def bet_raise(self, amount):
        self.bet += amount
        self.total_bet += amount
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
    
    # sets check to false
    def reverse_check(self):
        if self.check == True:
            self.check = False
    
    def add_chips(self, winnings):
        self.chips += winnings

    def display_player_info(self):
        print('NAME: ' + self.name + '\n' +
              'CHIPS: ' + str(self.chips) + '\n' +
              'BET: ' + str(self.bet))
    
    def toggle_action(self):
        self.can_act = True
    
    def set_act_time(self, time):
        self.last_act_time = time
    
    def toggle_winner(self):
        self.winner = True

    def reset_turn(self):
        self.bet = 0
        self.bet_gap = 0
        self.can_act = False
        self.last_act_time = 0
        if self.all_in == False and self.fold == False:
            self.check = False
    
    def reset_round(self):
        self.all_in = False
        self.fold = False
        self.reset_turn()
        self.hand_rank = 9999
        self.total_bet = 0
        self.winner = False
