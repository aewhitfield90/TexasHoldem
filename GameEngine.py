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
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2):
            if self.dealer.player_list[self.turn % self.dealer.player_count].NPC == True and self.dealer.player_list[self.turn % self.dealer.player_count].check == False:
                if self.dealer.player_list[self.turn % self.dealer.player_count].all_in == True:
                    self.pass_turn()

                elif self.dealer.player_list[self.turn % self.dealer.player_count].bet_gap == 0:
                    self.dealer.player_list[self.turn % self.dealer.player_count].check_hand()
                    self.pass_turn()

                else:
                    self.dealer.player_call(self.dealer.player_list[self.turn % self.dealer.player_count])
                    self.pass_turn()

        # Deal the flop if all player cards have been dealt and all players are ready
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False) and self.dealer.players_status():
            self.dealer.deal_flop()
            for player in self.dealer.player_list:
                player.reset_turn()
        
        """Removed in favor of splitting the function into two separate functions
        # deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True and self.dealer.players_status():
            self.dealer.deal_after_flop()
            for player in self.dealer.player_list:
                player.reset_turn()
            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False
        """
        # Deal the turn card
        if len(self.dealer.river) == 3 and self.dealer.players_status():  # Checks if flop has been dealt and all players are ready
            self.dealer.deal_turn()
            for player in self.dealer.player_list:
                player.reset_turn()

        # Deal the river card
        if len(self.dealer.river) == 4 and self.dealer.players_status():  # Checks if turn has been dealt and all players are ready
            self.dealer.deal_river()
            for player in self.dealer.player_list:
                player.reset_turn()    

        # Finish the round
        if not self.dealer.can_deal and len(self.dealer.winners) < 1 and self.dealer.players_status():
            for player in self.dealer.player_list:
                player.reset_turn()
            self.dealer.winners = self.dealer.decide_winner()
            for winner in self.dealer.winners:
                self.dealer.player_list[winner].add_chips(int(self.dealer.pot/len(self.dealer.winners)))
            self.turn = 0
            