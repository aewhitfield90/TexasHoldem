import numpy as np
from typing import List
from random import sample
from DeckBuilder import Card, Deck, ShortDeck
from phevaluator.evaluator import evaluate_cards

class GameUtility:
    """Class to handle game-related functions, particularly evaluating hands and determining winners."""

    def __init__(self, our_hand: np.ndarray, board: np.ndarray, cards: np.ndarray):
    #def __init__(self, our_hand: List[Card], board: List[Card], deck: Deck):
        """Initialize the GameUtility class with our hand, the board, and the deck."""
        
        # For testing purposes
        #print("Our hand:", [f"{card.rank}{card.suit}" for card in our_hand])
        #print("Board:", [f"{card.rank}{card.suit}" for card in board])

        # Combine cards from hand and board to be used together when evaluating
        self.combined_our_hand = np.concatenate([our_hand, board], axis=0) #NEW
        unavailable_cards = np.concatenate([our_hand, board], axis=0)
        self.available_cards = np.array([c for c in cards if c not in unavailable_cards])
        # print("Available cards:", [f"{card.rank}{card.suit}" for card in self.available_cards]) 
        self.our_hand = our_hand  
        self.board = board  
        #self.cards = cards 

    def evaluate_hand(self, hand: np.ndarray) -> int:
        """
        Evaluate a hand.

        Parameters
        ----------
        hand : np.ndarray
            Hand to evaluate.

        Returns
        -------
            Evaluation of hand
        """
        # Convert the np.ndarray to a list if not already a list
        hand_list = hand.tolist() #if isinstance(hand, np.ndarray) else hand

        # Generate the representation needed for the evaluate_cards function
        hand_repr = [f"{card.rank}{card.suit}" for card in hand_list]

        # Evaluate the hand using the phevaluator library function
        return evaluate_cards(*hand_repr)

    def get_winner(self, opp_hand: np.ndarray) ->int: 
        """Get the winner.

        Returns
        -------
            int of win (0), lose (1) or tie (2) - this is an index in the
            expected hand strength array
        """        
        combined_opp_hand = np.concatenate([self.opp_hand, self.board])
        opp_hand_rank = self.evaluate_hand(combined_opp_hand)
        our_hand_rank = self.evaluate_hand(self.combined_our_hand)
        #print("Our hand rank:", our_hand_rank) # For testing purposes
        if our_hand_rank < opp_hand_rank:
            return 0
        elif our_hand_rank > opp_hand_rank:
            return 1
        else:
            return 2

    @property
    def opp_hand(self) -> List[Card]:
        """Get random card.

        Returns
        -------
            Two cards for the opponent (Card)
        """
        return np.random.choice(self.available_cards, 2, replace=False)

