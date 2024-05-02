#GameEngine
from River import Dealer
from phevaluator.evaluator import evaluate_cards
import PlayerNPC
import pygame
import random
from settings import *

class Poker:
    def __init__(self, players) :
        self.dealer = Dealer(players)
        self.turn = 0
        self.button = 0
        self.round_finished = False
        self.show_main_hand = False
        self.blind = False
    
    def toggle_blind(self):
        self.blind = False
    
    def increment_button(self):
        self.button += 1
        if self.button >= len(self.dealer.player_list):
            self.button = 0
        self.turn = self.button

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
            self.dealer.player_bet(self.dealer.player_list[self.button - 2 % self.dealer.player_count], self.dealer.small_blind) #small blind bet
            self.dealer.player_list[self.button - 2 % self.dealer.player_count].set_small_blind()
            self.dealer.player_bet(self.dealer.player_list[self.button - 1 % self.dealer.player_count], self.dealer.small_blind * 2)#big blind bet
            self.dealer.player_list[self.button - 1 % self.dealer.player_count].set_big_blind()
            self.dealer.player_list[self.button - 1 % self.dealer.player_count].reverse_check() #reverses check for blind players
            self.dealer.player_list[self.button].set_button()
            self.blind = True

        # NPC player actions
        if self.dealer.dealt_cards >= (self.dealer.player_count * 2):
            player = self.dealer.player_list[self.turn % self.dealer.player_count]
            if player.last_act_time == 0 and player.NPC == True:
                player.last_act_time = pygame.time.get_ticks()
            if pygame.time.get_ticks() - player.last_act_time >= 1500 or player.all_in == True or player.fold == True:
                if (player.all_in == True or player.fold == True):                  
                    self.pass_turn()

                elif (player.NPC == True and player.check == False):
                    # random number to decide NPC action
                    number = random.uniform(0, 1)
                    bet = 0

                    # pre-flop decisions
                    if self.dealer.flop == False:
                        # checks if npc has a pair
                        if player.hand[0].rank == player.hand[1].rank:
                            # has a high pair
                            if value_dict.get(player.hand[0].rank) >= 11:
                                
                                if number < 0.1:
                                    # selects random number of chips to bet between 20% of chips and 100%
                                    bet = random.randint(int(player.chips * 0.2), int(player.chips) + player.bet_gap)
                                    self.dealer.player_bet(player, bet)
                                elif 0.1 < number < 0.3:
                                    # selects random number of chips to bet between 5% of chips and 20%
                                    bet = random.randint(int(player.chips * 0.05), int(player.chips * 0.2)) + player.bet_gap
                                    if bet > player.chips:
                                        self.dealer.player_bet(player, player.chips)
                                    else:
                                        self.dealer.player_bet(player, bet)
                                else:
                                    #checks or calls
                                    if player.bet_gap == 0:
                                        player.check_hand()
                                    else:
                                        self.dealer.player_call(player)
                            # has a mid-low pair
                            else:
                                if number < 0.2:
                                    # selects random number of chips to bet between 5% of chips and 20%
                                    self.dealer.player_bet(player, random.randint(int(player.chips * 0.05), int(player.chips * 0.2)) + player.bet_gap)
                                else:
                                    #checks or calls
                                    if player.bet_gap >= player.chips * 0.2:
                                        player.fold_hand()
                                    elif player.bet_gap == 0:
                                        player.check_hand()
                                    else:
                                        self.dealer.player_call(player)
                        # checks for a high card
                        elif value_dict.get(player.hand[0].rank) > 11 or value_dict.get(player.hand[1].rank) > 11:
                            if number < 0.1:
                                # selects random number of chips to bet between 5% of chips and 20%
                                self.dealer.player_bet(player, random.randint(int(player.chips * 0.05), int(player.chips * 0.2)) + player.bet_gap)
                            else:
                                #checks or calls
                                if player.bet_gap == 0:
                                    player.check_hand()
                                elif number < 0.5:
                                    self.dealer.player_call(player)
                                else:
                                    player.fold_hand
                        else:
                            if player.bet_gap == 0:
                                player.check_hand()
                            elif player.bet_gap <= int(player.chips) * 0.02:
                                self.dealer.player_call(player)
                            else:
                                player.fold_hand()
                    # post-flop decisions
                    elif self.dealer.flop and self.dealer.round_finished == False:
                        player_cards = []
                        rank = 9999
                        for card in player.hand:
                            player_cards.append(f"{card.rank}{card.suit}")
                        for card in self.dealer.river:
                            player_cards.append(f"{card.rank}{card.suit}")
                        # calculates hand strength to make decisions
                        if len(player_cards) == 5:
                            rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                        player_cards[4])
                        elif len(player_cards) == 6:
                            rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                        player_cards[4], player_cards[5])
                        else:
                            rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                        player_cards[4], player_cards[5], player_cards[6])
                        if rank < 1500:
                            # raises if other players have bet less than 20% of current player chips
                            if player.bet_gap <= player.chips * 0.2:
                                    self.dealer.player_bet(player, random.randint(int(player.chips * 0.3), int(player.chips * 0.6)))
                            else:
                                self.dealer.player_call(player)

                        elif 1500 < rank < 4500:
                            if player.bet_gap <= player.chips * 0.1 and number < 0.5:
                                    bet = random.randint(int(player.chips * 0.1), int(player.chips * 0.3)) + player.bet_gap
                                    if bet > player.chips:
                                        self.dealer.player_bet(player, player.chips)
                                    else:
                                        self.dealer.player_bet(player, random.randint(int(player.chips * 0.11), int(player.chips * 0.3)) + player.bet_gap)
                            elif player.bet_gap <= player.chips * 0.1:
                                    self.dealer.player_call(player)
                            elif player.bet_gap <= player.chips * 0.3 and number < 0.6:
                                    self.dealer.player_call(player)
                            else:
                                player.fold_hand()

                        else:
                            if (player.bet_gap <= player.chips * 0.2 or player.bet_gap < 50) and number < 0.35:
                                    self.dealer.player_call(player)
                            elif player.bet_gap == 0:
                                player.check_hand()
                            else:
                                player.fold_hand()
                    if(player.check == True):
                        self.pass_turn()
                    
        # check if all player cards have been dealt before flop
        if self.dealer.dealt_cards == (self.dealer.player_count * 2) and (self.dealer.flop == False) and self.dealer.players_status(): # checks cards are dealt, flop hasnt happened, and if all player classes have CHECKED
            self.dealer.deal_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()

            self.turn = self.button
        
        """Removed in favor of splitting the function into two separate functions
        # deal extra cards to river
        if self.dealer.flop == True and self.dealer.can_deal == True and self.dealer.players_status():
            self.dealer.deal_after_flop()
            for card in self.dealer.river:
                card.show_card()
            for player in self.dealer.player_list:
                player.reset_turn()

            if self.dealer.dealt_cards == (self.dealer.player_count * 2) + 5:
                self.dealer.can_deal  = False
        """
        # Deal the turn card
        if len(self.dealer.river) == 3 and self.dealer.players_status():  # Checks if flop has been dealt and all players are ready
            self.dealer.deal_turn()
            self.dealer.river[3].show_card()
            for player in self.dealer.player_list:
                player.reset_turn()
            self.turn = self.button

        # Deal the river card
        if len(self.dealer.river) == 4 and self.dealer.players_status():  # Checks if turn has been dealt and all players are ready
            self.dealer.deal_river()
            self.dealer.river[4].show_card()
            for player in self.dealer.player_list:
                player.reset_turn()    
            self.turn = self.button

        # finish the round
        if ((self.dealer.can_deal == False) and (len(self.dealer.winners) < 1)) and self.dealer.players_status():
            self.dealer.winners = self.dealer.decide_winner()
            # reveals cards
            for player in self.dealer.player_list:
                if player.fold == False:
                    for card in player.hand:
                        card.show_card()
            # gather winners
            for winner in self.dealer.winners:
                self.dealer.player_list[winner].toggle_winner()
            # pays out winners
            for winner in self.dealer.winners:
                self.dealer.pay_winnings(self.dealer.player_list[winner], int(self.dealer.pot/len(self.dealer.winners)))

            

        
