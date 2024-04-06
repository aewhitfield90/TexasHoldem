#GameEngine
from River import Dealer

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)

    def update(self, dealer):
        #check for cards in players hands
        if self.dealt_cards < (self.player_count * 2):
            self.deal_player_cards()
        
        #check for player actions
        #if self.dealt_cards == (self.player_count * 2):
            #while not(self.players_check):
                #blinds = False
                #for i in range(self.player_count):
                    #if not(blinds):
                        #self.players[self.small_blind_player].raise_bet(self.small_blind)
                        #self.players[self.small_blind_player + 1].raise_bet(self.small_blind * 2)                       

        #check if all player cards have been dealt before flop
        if self.dealt_cards == (self.player_count * 2) and (self.flop == False):
            self.deal_flop()
        
        #deal extra cards to river
        if self.flop == True and self.can_deal == True:
            self.river.append(self.deck.deal_card())
            self.dealt_cards += 1
            if self.dealt_cards >= (self.player_count * 2) + 5:
                self.can_deal  = False
        
        #finish the round
        if self.can_deal == False or self.num_active_players <= 1:
            self.winner = self.define_winner()