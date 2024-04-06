import random, pygame


suits = ['H', 'D', 'C', 'S']
ranks = [2, 3, 4, 5, 6, 7, 8, 9, "T", "J", "Q", "K", "A"] 

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.start_position = (0, 1000)
        self.id = f"{self.rank}{self.suit}"
        self.img = f"DeckOfCards/{self.id}.png"
        self.card_img = pygame.image.load(self.img)


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


    