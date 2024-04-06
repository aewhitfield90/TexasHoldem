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
        self.player_count = len(players)
        self.num_active_players = len(players)
        self.current_player_index = 0
        self.can_deal = True
        self.players_check = False
        self.dealt_cards = 0
        self.winner = None

    # adds new player to the table
    def add_player(self, player):
        if self.player_count < MAX_PLAYERS:
            self.players.append(player)
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
        for player in self.players:
            player.hand.append(self.deck.deal_card())
            self.dealt_cards += 1

    #deals flop
    def deal_flop(self):
        for _ in range(3):
            self.river.append(self.deck.deal_card())
            self.dealt_cards += 1
        self.flop = True

    def deal_after_flop(self):
        if self.dealt_cards <= (self.player_count * 2) + 5:
            self.river.append(self.deck.deal_card())
            self.dealt_cards += 1
            if self.dealt_cards == (self.player_count * 2) + 5:
                self.can_deal = False

    def evaluate_hands():
        pass

    
    