import sys
sys.path.append('../')  
from DeckBuilder import Card
from typing import List, Tuple, Dict

def convert_rank_to_int(rank: str) -> int:
    """ Convert card rank to integer. Handles both numerical and face cards. """
    rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    return rank_dict.get(rank.upper(), 0)

def make_starting_hand_lossless(starting_hand: List[Card], short_deck: bool = True) -> int:
    """ Evaluate and rank starting hands based on their potential strength in a poker game. """
    ranks = [convert_rank_to_int(card.rank) for card in starting_hand]
    suits = [card.suit for card in starting_hand]
    
    suited = len(set(suits)) == 1  # Check if all cards are of the same suit
    rank_counts = {rank: ranks.count(rank) for rank in ranks}
    
    # Evaluating pair, suited, and high card strengths
    if len(ranks) == 2:  # Ensure we're dealing with two cards
        if ranks[0] == ranks[1]:  # Pair
            return ranks[0] * 2 - (14 if suited else 0)
        else:
            rank_score = sum(ranks) - (10 if suited else 0)
            return rank_score if short_deck else rank_score - min(ranks)

def compute_preflop_lossless_abstraction(cards: List[Card]) -> Dict[Tuple[Card, Card], int]:
    """ Compute the preflop abstraction for a set of cards, assuming a short deck. """
    if not all(card.rank in {'T', 'J', 'Q', 'K', 'A'} for card in cards):
        raise ValueError("Preflop lossless abstraction only works with ranks T, J, Q, K, A.")

    preflop_lossless: Dict[Tuple[Card, Card], int] = {}
    sorted_cards = sorted(cards, key=lambda card: convert_rank_to_int(card.rank), reverse=True)
    
    # Evaluate all possible pairs of cards
    for i in range(len(sorted_cards)):
        for j in range(i + 1, len(sorted_cards)):
            hand = [sorted_cards[i], sorted_cards[j]]
            hand_key = tuple(sorted(hand, key=lambda card: card.rank, reverse=True))
            preflop_lossless[hand_key] = make_starting_hand_lossless(hand, True)

    return preflop_lossless

# Example usage
if __name__ == "__main__":
    # Assuming the Deck class can generate a list of Card instances
    from DeckBuilder import ShortDeck
    deck = ShortDeck(load_images=False)
    abstraction = compute_preflop_lossless_abstraction(deck.deck)
    print(abstraction)
