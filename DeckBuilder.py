import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = [1,2,3,4,5,6,7,8,9,10,11,12,13]

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self): #creates a new deck and shuffles it
        self.deck = self.generate_deck()
        self.shuffle_deck()

    def generate_deck(self):  #generates a full deck of 52 cards
        new_deck = []
        for i in suits:
            for j in ranks:
                new_deck.append(Card(i,j))
        return new_deck
        
    def shuffle_deck(self): 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()


    