#GameEngine
from River import Dealer
import pygame

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)
        self.turn = 0
        self.start_turn = 0
        self.round_finished = False
        self.show_main_hand = False
        self.show_all_hands = False
        self.blind = False
    
    def toggle_blind(self):
        self.blind = False
    
    def increment_button(self):
        self.start_turn += 1
        if self.start_turn == self.dealer.player_count:
            self.start_turn = 0
        self.turn = self.start_turn

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

        # blinds
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2) and self.blind == False:
            self.dealer.player_bet(self.dealer.player_list[self.start_turn - 2 % self.dealer.player_count], self.dealer.small_blind)
            self.dealer.player_bet(self.dealer.player_list[self.start_turn - 1 % self.dealer.player_count], self.dealer.small_blind * 2)
            self.dealer.player_list[self.start_turn - 1 % self.dealer.player_count].reverse_check()
            self.blind = True

        # NPC player actions
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2): #if dealtcards >= players*2, enters this once all cards have been dealt
            if self.dealer.player_list[self.turn % self.dealer.player_count].last_act_time == 0:
                self.dealer.player_list[self.turn % self.dealer.player_count].last_act_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.dealer.player_list[self.turn % self.dealer.player_count].last_act_time >= 100: # wait time for NPCs actions
                if (self.dealer.player_list[self.turn % self.dealer.player_count].all_in == True or 
                    self.dealer.player_list[self.turn % self.dealer.player_count].fold == True): #if player selects ALL IN or FOLD pass turn
                        
                        self.pass_turn()


                if (self.dealer.player_list[self.turn % self.dealer.player_count].NPC == True and 
                    self.dealer.player_list[self.turn % self.dealer.player_count].check == False):
                    
                    if self.dealer.player_list[self.turn % self.dealer.player_count].bet_gap == 0:  #if there is no difference in NPC bet amount and Real Player bet amount, NPC CHECKS there own hand
                        self.dealer.player_list[self.turn % self.dealer.player_count].check_hand()
                        self.pass_turn()

                    else:
                        self.dealer.player_call(self.dealer.player_list[self.turn % self.dealer.player_count])
                        self.pass_turn()
                    self.pass_turn()

        # check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False) and self.dealer.players_status(): # checks cards are dealt, flop hasnt happened, and if all player classes have CHECKED
            self.dealer.deal_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()

            self.turn = self.start_turn
        
        # deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True and self.dealer.players_status():
            self.dealer.deal_after_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()

            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False
            
            self.turn = self.start_turn


        # finish the round
        if ((self.dealer.can_deal == False) and (len(self.dealer.winners) < 1)) and self.dealer.players_status():
            self.dealer.winners = self.dealer.decide_winner()
            bet_sum = 0
            bet_difference = 0
            # reveals cards
            for player in self.dealer.player_list:
                if player.fold == False:
                    for card in player.hand:
                        card.show_card()
            # gather winners
            for winner in self.dealer.winners:
                bet_sum += self.dealer.player_list[winner].total_bet
                self.dealer.player_list[winner].toggle_winner()
            # pays extra amount bet back
            for player in self.dealer.player_list:
                for winner in self.dealer.winners:
                    if player.total_bet > self.dealer.player_list[winner].total_bet:
                        if bet_difference == 0 or bet_difference > player.total_bet - self.dealer.player_list[winner].total_bet:
                            bet_difference = player.total_bet - self.dealer.player_list[winner].total_bet
                self.dealer.pay_winnings(player, bet_difference)
                bet_difference = 0
            # pays out winners
            for winner in self.dealer.winners:
                self.dealer.pay_winnings(self.dealer.player_list[winner], int(self.dealer.pot*(self.dealer.player_list[winner].total_bet / bet_sum)))
                #self.dealer.player_list[winner].add_chips(int(self.dealer.pot*(self.dealer.player_list[winner].total_bet / bet_sum)))

            

        
