import random, pygame


suits = ['H', 'D', 'C', 'S']
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"] 

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.show = True
        self.position = (500, 500)
        self.id = f"{self.rank}{self.suit}"
        self.img = f"DeckOfCards/{self.id}.png"
        self.card_img = pygame.image.load(self.img).convert_alpha()
        self.back_img = pygame.image.load(f"DeckOfCards/BACK.png").convert_alpha()

    def render_card(self, screen):
        temp_image = None
        if self.show == True:
            temp_image = self.card_img
        else:
            temp_image = self.back_img
        image = pygame.transform.scale(temp_image, (120,120))
        screen.blit(image, self.position)

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


    