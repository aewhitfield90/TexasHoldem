from phevaluator.evaluator import evaluate_cards
from DeckBuilder import Deck
from settings import *

class Dealer:
    def __init__(self, players):
        self.deck = Deck()
        self.flop = False
        self.river = []
        self.highest_bet = 0
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
        self.button = 0 #person located after the blinds and the one who starts the rounds

    # adds new player to the table
    def add_player(self, player):
        if self.player_count < MAX_PLAYERS:
            self.player_list.append(player)
            self.player_count = len(self.player_list)
        else:
            print("Cannot Add Player")
    
    # removes existing player from the table
    def remove_player(self, player_name):
        removed = False
        for player in self.player_list:
            if player.name == player_name:
                self.player_list.remove(player)
                del player
                removed = True
                self.player_count = len(self.player_list)
        if removed == False:
            print("Player Not Found.")
    
    def get_highest_bet(self):
        bet_list = []
        for player in self.player_list:
            bet_list.append(player.bet)
        self.highest_bet = max(bet_list)

    def set_player_bet_gaps(self):
        for player in self.player_list:
            player.bet_gap = self.highest_bet - player.bet

    # adds bet_raise to the pot
    def player_bet(self, player, bet):
        player.bet_raise(bet)
        self.pot += bet
        #checking if bets have changed and setting them
        self.get_highest_bet()
        self.set_player_bet_gaps()
    
    # function for adding player matching bet to the pot
    def player_call(self, player):
        player.call_hand()
        self.pot += player.bet_gap

    # deals player cards
    def deal_player_cards(self):
        for player in self.player_list:
            new_card = self.deck.deal_card()
            if self.dealt_cards < self.player_count:
                new_card.position = CARDS_1[self.dealt_cards]
            else:
                new_card.position = CARDS_2[self.dealt_cards - self.player_count]
            player.hand.append(new_card)
            self.dealt_cards += 1
    
    # Function to check if players have concluded their turns
    def players_status(self):
        for player in self.player_list:
            if player.check == False:
                return False
        return True

    # deals flops
    def deal_flop(self):
        for i in range(3):
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[i], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
        self.flop = True
        #for player in self.player_list:
            #print(player.name + " " + f"{player.hand[0].rank}{player.hand[0].suit}" + " " + f"{player.hand[1].rank}{player.hand[1].suit}")

    # deals the other 2 cards after flop
    def deal_after_flop(self):
        if self.dealt_cards <= (self.player_count * 2) + 5:
            new_card = self.deck.deal_card()
            new_card.position = (RIVER_X[self.dealt_cards - self.player_count * 2], RIVER_Y)
            self.river.append(new_card)
            self.dealt_cards += 1
            if self.dealt_cards == (self.player_count * 2) + 5:
                #print(self.dealt_cards)
                self.can_deal = False

    # uses the pheavluator library to calculate poker hands by rank
    def decide_winner(self):
        for player in self.player_list:
            player_cards = []
            if player.fold == False:
                for card in player.hand:
                    player_cards.append(f"{card.rank}{card.suit}")
                for card in self.river:
                    player_cards.append(f"{card.rank}{card.suit}")
                player.hand_rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3],
                                                  player_cards[4], player_cards[5], player_cards[6])
        hand_ranks = []
        for i in range(len(self.player_list)):
            hand_ranks.append(self.player_list[i].hand_rank)  
        winners_list = []
        best_hand = min(hand_ranks)
        for i in range(len(hand_ranks)):
            #print(self.player_list[i].name + ": " + str(hand_ranks[i]))
            if best_hand == hand_ranks[i]:
                winners_list.append(i)
        self.round_finished = True
        return winners_list

    # function to get table back to starting point so a new round can be started
    def reset_table(self):
        for player in self.player_list:
            for _ in range(len(player.hand)):
                card = player.hand.pop()
                card.hide_card()
                self.deck.deck.append(card)
            player.reset_round()
        for _ in range(len(self.river)):
            card = self.river.pop()
            card.hide_card()
            self.deck.deck.append(card)
        #for card in self.deck:
        #    card.hide_card()

        self.winners = []
        self.deck.shuffle_deck()
        self.pot = 0
        self.dealt_cards = 0
        self.flop = False
        self.can_deal = True
        self.round_finished = False
