#GameEngine
from River import Dealer

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)
        self.turn = 0
        self.round_finished = False
        self.show_main_hand = False
        self.show_all_hands = False
    

    def pass_turn(self):
        self.turn += 1

    def update(self):
        # check for cards in players hands
        if self.dealer.dealt_cards < (self.dealer.player_count * 2):
            self.dealer.deal_player_cards()   
        
        # showing player hand
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2):
            for card in self.dealer.player_list[0].hand:
                card.show_card()
            self.show_main_hand = True

        # NPC player actions
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2):
            if (self.dealer.player_list[self.turn % self.dealer.player_count].all_in == True or 
                  self.dealer.player_list[self.turn % self.dealer.player_count].fold == True):
                    self.pass_turn()

            if (self.dealer.player_list[self.turn % self.dealer.player_count].NPC == True and 
                  self.dealer.player_list[self.turn % self.dealer.player_count].check == False):
                if self.dealer.player_list[self.turn % self.dealer.player_count].bet_gap == 0:
                    self.dealer.player_list[self.turn % self.dealer.player_count].check_hand()
                    self.pass_turn()

                else:
                    self.dealer.player_call(self.dealer.player_list[self.turn % self.dealer.player_count])
                    self.pass_turn()

        # check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False) and self.dealer.players_status():
            self.dealer.deal_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()
        
        # deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True and self.dealer.players_status():
            self.dealer.deal_after_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()

            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False

        # finish the round
        if ((self.dealer.can_deal == False) and (len(self.dealer.winners) < 1)) and self.dealer.players_status():
            self.dealer.winners = self.dealer.decide_winner()
            for player in self.dealer.player_list:
                if player.fold == False:
                    for card in player.hand:
                        card.show_card()
            for winner in self.dealer.winners:
                self.dealer.player_list[winner].add_chips(int(self.dealer.pot/len(self.dealer.winners)))
            self.turn = 0
            