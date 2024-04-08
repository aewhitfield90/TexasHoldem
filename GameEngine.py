#GameEngine
from River import Dealer

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)

    def update(self):
        #check for cards in players hands
        if self.dealer.dealt_cards < (self.dealer.player_count * 2):
            self.dealer.deal_player_cards()
        
        #check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False):
            self.dealer.deal_flop()
        
        #deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True:
            self.dealer.deal_after_flop()
            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False

        #check for player actions


        #finish the round
        if ((self.dealer.can_deal == False) and (len(self.dealer.winners) < 1)):
            self.dealer.winners = self.dealer.decide_winner()
            