#GameEngine
from River import Dealer

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)
        self.turn = 0

    def pass_turn(self):
        self.turn += 1

    def update(self):
        # check for cards in players hands
        if self.dealer.dealt_cards < (self.dealer.player_count * 2):
            self.dealer.deal_player_cards()   

        # NPC player actions
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2): #if dealtcards >= players*2, enters this once all cards have been dealt
            if self.dealer.player_list[self.turn % self.dealer.player_count].NPC == True and self.dealer.player_list[self.turn % self.dealer.player_count].check == False: # if Player in list is an NPC and Real player didn't select CHECK
                if self.dealer.player_list[self.turn % self.dealer.player_count].all_in == True:#if player selects ALL IN pass turn
                    self.pass_turn()

                elif self.dealer.player_list[self.turn % self.dealer.player_count].bet_gap == 0: #if there is no difference in NPC bet amount and Real Player bet amount, NPC CHECKS there own hand
                    self.dealer.player_list[self.turn % self.dealer.player_count].check_hand() 
                    self.pass_turn()

                else:
                    self.dealer.player_call(self.dealer.player_list[self.turn % self.dealer.player_count]) #if there is a bet gap, NPC will CALL
                    self.pass_turn()

        # check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False) and self.dealer.players_status(): # checks cards are dealt, flop hasnt happened, and if all player classes have CHECKED
            self.dealer.deal_flop()
            for player in self.dealer.player_list:
                player.reset_turn()
        
        # deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True and self.dealer.players_status():
            self.dealer.deal_after_flop()
            for player in self.dealer.player_list:
                player.reset_turn()
            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False


        # finish the round
        if ((self.dealer.can_deal == False) and (len(self.dealer.winners) < 1)) and self.dealer.players_status():
            self.dealer.winners = self.dealer.decide_winner()
            for winner in self.dealer.winners:
                self.dealer.player_list[winner].add_chips(int(self.dealer.pot/len(self.dealer.winners)))
            self.turn = 0
            