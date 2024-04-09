import itertools, phevaluator
from phevaluator.evaluator import evaluate_cards
from DeckBuilder import Deck
from Player import Player
from settings import *

class Dealer:
    def __init__(self, players):
        self.deck = Deck()
        self.flop = False
        self.river = []
        self.pot = 0
        self.small_blind = 1
        self.small_blind_player = 0
        self.player_list = players
        self.player_count = len(self.player_list)
        self.num_active_players = len(self.player_list)
        self.current_player_index = 0
        self.can_deal = True
        self.players_check = False
        self.dealt_cards = 0
        self.winners = []
        self.round_finished = False

    # adds new player to the table
    def add_player(self, player):
        if self.player_count < MAX_PLAYERS:
            self.player_list.append(player)
        else:
            print("Cannot Add Player")
    
    #removes existing player from the table
    def remove_player(self, player_name):
        removed = False
        for player in self.player_list:
            if player.name == player_name:
                self.player_list.pop(player)
                removed = True
        if removed == False:
            print("Player Not Found.")
    
    #adds bet to round pot
    def player_bet(self, bet):
        self.pot += bet

    #deals player cards
    def deal_player_cards(self):
        for player in self.player_list:
            new_card = self.deck.deal_card()
            if self.dealt_cards < self.player_count:
                new_card.position = CARDS_1[self.dealt_cards]
            else:
                new_card.position = CARDS_2[self.dealt_cards - self.player_count]
            player.hand.append(new_card)
            self.dealt_cards += 1

    #deals flop
    def deal_flop(self):
        for i in range(3):
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[i], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
        self.flop = True
        for player in self.player_list:
            print(player.name + " " + f"{player.hand[0].rank}{player.hand[0].suit}" + " " + f"{player.hand[1].rank}{player.hand[1].suit}")

    def deal_after_flop(self):
        if self.dealt_cards <= (self.player_count * 2) + 5:
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[self.dealt_cards - self.player_count * 2], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
            if self.dealt_cards == (self.player_count * 2) + 5:
                print(self.dealt_cards)
                self.can_deal = False

    # uses the pheavluator library to calculate poker hands by rank
    def decide_winner(self):
        for player in self.player_list:
            player_cards = []
            for card in player.hand:
                player_cards.append(f"{card.rank}{card.suit}")
            for card in self.river:
                player_cards.append(f"{card.rank}{card.suit}")
            player.hand_rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                 player_cards[4], player_cards[5], player_cards[6])
            #print(player.name + " " + player_cards[0] + " " + player_cards[1] + " " + player_cards[2] + " " + player_cards[3] + 
            #                                    " " + player_cards[4] + " " + player_cards[5] + " " + player_cards[6])   
        hand_ranks = []
        for i in range(len(self.player_list)):
            hand_ranks.append(self.player_list[i].hand_rank)  
        winners_list = []
        best_hand = min(hand_ranks)
        for i in range(len(hand_ranks)):
            print(self.player_list[i].name + ": " + str(hand_ranks[i]))
            if best_hand == hand_ranks[i]:
                winners_list.append(i)
        #eound finished variable should be changed for after payouts once chips are implemented
        self.round_finished = True
        return winners_list

    #function to get table back to starting point so a new round can be started
    def reset_table(self):
        for player in self.player_list:
            for _ in range(len(player.hand)):
                self.deck.deck.append(player.hand.pop())
        for _ in range(len(self.river)):
            self.deck.deck.append(self.river.pop())
        self.winners = []
        self.deck.shuffle_deck()
        self.dealt_cards = 0
        self.flop = False
        self.can_deal = True
        self.round_finished = False
