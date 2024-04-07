#GameEngine
from River import Dealer

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)

    def update(self):
        #check for cards in players hands
        if self.dealer.dealt_cards < (self.dealer.player_count * 2):
            self.dealer.deal_player_cards()
        
        #check for player actions


        #check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False):
            self.dealer.deal_flop()
        
        #deal extra cards to river

        if self.dealer.flop == True and self.dealer.can_deal == True:
            self.dealer.deal_after_flop()
            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False
        
        #finish the round
        #if self.dealer.can_deal == False or self.dealer.num_active_players <= 1:
            #self.winner = self.dealer.define_winner()