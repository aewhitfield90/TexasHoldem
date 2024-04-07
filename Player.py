from DeckBuilder import Card, Deck

class Player:
    def __init__(self, name = "N/A", starting_chips = 0,):
        self.name = name
        self.chips = starting_chips
        self.bet = 0
        self.bet_gap = 0
        self.hand = []
        self.fold = False
        self.check = False
        self.all_in = False
        self.hand_rank = 0
        self.win = False
        self.button = False #person located after the blinds and the one who starts the rounds

    def fold(self):
        self.fold = True
        self.bet_gap = 0
    
    def bet_raise(self, amount):
        self.bet += amount
        self.chips -= amount
        self.check = True
    
    def call(self):
        self.bet_raise(self.bet_gap)

    def check(self):
        self.check = True
    
    def all_in(self):
        self.bet_raise(self.chips)
    
    def add_chips(self, winnings):
        self.chips += winnings

    def display_player_info(self):
        print('NAME: ' + self.name + '\n' +
              'CHIPS: ' + str(self.chips) + '\n' +
              'BET: ' + str(self.bet))

    def reset(self):
        self.bet = 0
        self.fold = False
        self.check = False
        self.all_in = False
        for _ in range(len(self.hand_attributes)):
            self.hand_attributes.pop()
        self.win = False
