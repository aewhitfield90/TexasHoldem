#GameEngine
from River import Dealer
import PlayerNPC

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)
        self.turn = 0
        self.round_finished = False
        self.all_in_trigger = 4
    

    def pass_turn(self):
        self.turn += 1

    def update(self):
        # check for cards in players hands
        if self.dealer.dealt_cards < (self.dealer.player_count * 2):
            self.dealer.deal_player_cards()   

        # NPC player actions
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2):
            if self.all_in_trigger <= 0:
                self.pass_turn()
            #print("player turn name: " + self.dealer.player_list[self.turn % self.dealer.player_count].name)
            if (self.all_in_trigger > 0 and self.dealer.player_list[0].all_in == True): #only enters if PLAYER attribute all_in is true
                        #print(self.turn % self.dealer.player_count)
                        #print("entered PlayerNPC")
                        arrayVal = (self.turn % self.dealer.player_count)
                        PlayerNPC.PlayerNPC(self.dealer, arrayVal)
                        self.all_in_trigger -= 1
                        self.pass_turn()

            elif (self.dealer.player_list[self.turn % self.dealer.player_count].NPC == True and 
                  self.dealer.player_list[self.turn % self.dealer.player_count].check == False and 
                  self.dealer.player_list[self.turn % self.dealer.player_count].all_in != True and 
                  self.dealer.player_list[self.turn % self.dealer.player_count].fold != True):
                if self.dealer.player_list[self.turn % self.dealer.player_count].bet_gap == 0:
                    self.dealer.player_list[self.turn % self.dealer.player_count].check_hand()
                    self.pass_turn()

                else:
                    self.dealer.player_call(self.dealer.player_list[self.turn % self.dealer.player_count]) #if there is a bet gap, NPC will CALL
                    print("entered else")
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
            