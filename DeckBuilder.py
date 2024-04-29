import random
import pygame

# Define the suits and ranks for a standard deck of cards
suits = ['H', 'D', 'C', 'S']
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"] 

class Card:
    """ Represents a single playing card, identified by its suits and rank. """
    def __init__(self, suit, rank, load_images=True):
        """ Initialize a new card with given suit and rank, and load its images.
        Args:
            suit (str): The suit of the card (H, D, C, S)
            rank (str): The rank of the card (2-10, J, Q, K, A)
            load_images (bool): Whether to load the card images or not
        """ 
        self.suit = suit
        self.rank = rank
        self.load_images = load_images
        self.show = False   # Determines if the card's face is shown or the back
        self.position = (500, 500)   # Default position on the screen 
        self.id = f"{self.rank}{self.suit}"   # Unique identifier for the card
        
        if load_images:
            self.img = f"DeckOfCards/{self.id}.png"   # Path to the card's face image
            self.card_img = pygame.image.load(self.img).convert_alpha()
            self.back_img = pygame.image.load(f"DeckOfCards/BACK.png").convert_alpha()   # Load the face image
        else:
            self.card_img = None
            self.back_img = None

    # function for printing cards into pygame screen
    def render_card(self, screen):
        """ Render the card on a given pygame screen. """
        temp_image = None
        if self.show == True:
            temp_image = self.card_img
        else:
            temp_image = self.back_img
        image = pygame.transform.scale(temp_image, (120,120))   # Scale the card image
        screen.blit(image, self.position)  # Draw the image at the card's position
    
    def show_card(self):
        self.show = True
    
    def hide_card(self):
        self.show = False

class Deck:
    """ Represents a deck of playing cards. """
    def __init__(self, load_images=True): 
        """ Initialize the deck by generating a shuffling a full deck of cards. """
        self.load_images = load_images
        self.deck = self.generate_deck(load_images)
        self.shuffle_deck()

    def generate_deck(self, load_images=True):  
        """ Generate a full deck of 52 cards """
        return [Card(suit, rank) for suit in suits for rank in ranks]
        
    def shuffle_deck(self): 
        """ Shuffle the deck randomly. """
        random.shuffle(self.deck)

    def deal_card(self):
        """ Remove and return the top card from the deck if it's not empty. """
        if self.deck:
            return self.deck.pop()
        else:
            raise ValueError("Deck is empty!")

class ShortDeck(Deck):
    def generate_deck(self, load_images=True):
        """Generate a deck consisting only of high cards (T, J, Q, K, A)."""
        suits = ['H', 'D', 'C', 'S']
        ranks = ["T", "J", "Q", "K", "A"]
        return [Card(suit, rank, load_images) for suit in suits for rank in ranks]    