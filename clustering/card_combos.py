import logging
from itertools import combinations
import numpy as np
from tqdm import tqdm

# Import the Card and Deck classes from your local DeckBuilder module
from DeckBuilder import Card, Deck, ShortDeck

log = logging.getLogger(__name__)

class CardCombos:
    """This class contains methods to generate all possible combinations of cards for a given 
    street and stores the combinations and histories for different stages 
    in a poker game.
    """
    def __init__(self, low_card_rank: int = 10, high_card_rank: int = 14, load_images: bool = False):
        """Initialize the CardCombos object with a range of card ranks."""
        self.deck = ShortDeck(load_images=load_images)  # Initialize deck with or without loading images
        self._cards = np.array([card for card in self.deck.deck if low_card_rank <= card.rank_int <= high_card_rank])
        self.starting_hands = self.get_card_combos(2)
        self.flop = self.create_info_combos(self.starting_hands, self.get_card_combos(3))
        self.turn = self.create_info_combos(self.starting_hands, self.get_card_combos(4))
        self.river = self.create_info_combos(self.starting_hands, self.get_card_combos(5))

    def get_card_combos(self, num_cards: int) -> np.ndarray:
        """
        Get the card combinations for a given street.

        Parameters
        ----------
        num_cards : int
            Number of cards you want returned

        Returns
        -------
            Combos of cards (Card) -> np.ndarray
        """
        return np.array([c for c in combinations(self._cards, num_cards)])

    def create_info_combos(self, start_combos: np.ndarray, public_combos: np.ndarray) -> np.ndarray:
        """Generate combinations of private and public cards."""
        our_cards = []
        for hand in start_combos:
            for public in public_combos:
                # Ensure there is no overlap between hand and public cards
                if not np.any(np.isin(hand, public)):
                    # Combine the cards in a sorted manner for uniformity
                    combined_hand = np.concatenate((hand, public))
                    our_cards.append(combined_hand)
        return np.array(our_cards)

# Example usage
if __name__ == "__main__":
    combos = CardCombos()
    """Print information about the generated card combinations.
    print(f"Total starting hands: {len(combos.starting_hands)}")
    print(f"Sample starting hand: {combos.starting_hands[0]}")
    print(f"Sample flop combination: {combos.flop[0]}")
    print(f"Total flop combinations: {len(combos.flop)}")
    print(f"Sample turn combination: {combos.turn[0]}")
    print(f"Total turn combinations: {len(combos.turn)}")
    print(f"Sample river combination: {combos.river[0]}")
    print(f"Total river combinations: {len(combos.river)}")
    """