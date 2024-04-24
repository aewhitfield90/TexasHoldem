import math

def choose(n, k):
    """Calculate binomial coefficient (n choose k)"""
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def prob_higher_hand_on_flop(my_cards, flop):
    """Calculate the probability of another player having a higher hand than yours on the flop."""
    
    # Remove known cards from the deck
    deck = [i for i in range(52) if i not in my_cards + flop]
    
    # Total number of possible opponent hands
    total_hands = choose(len(deck), 2)
    
    # Number of hands that beat your hand
    num_beat = 0
    
    # Check for sets
    for card in set(my_cards + flop):
        num_beat += choose(deck.count(card), 2)
    
    # Check for two pairs
    for card in set(my_cards + flop):
        if deck.count(card) >= 2:
            num_beat += deck.count(card) * (deck.count(card) - 1)
    
    # Check for flush
    suits = [card // 13 for card in my_cards + flop + deck]
    for suit in range(4):
        if suits.count(suit) >= 5:
            num_beat += choose(suits.count(suit), 5)
    
    return num_beat / total_hands

def prob_higher_hand_on_turn(my_cards, flop, turn):
    """Calculate the probability of another player having a higher hand than yours on the turn."""
    
    # Remove known cards from the deck
    deck = [i for i in range(52) if i not in my_cards + flop + [turn]]
    
    # Total number of possible opponent hands
    total_hands = choose(len(deck), 2)
    
    # Number of hands that beat your hand
    num_beat = 0
    
    # Check for sets
    for card in set(my_cards + flop + [turn]):
        num_beat += choose(deck.count(card), 2)
    
    # Check for two pairs
    for card in set(my_cards + flop + [turn]):
        if deck.count(card) >= 2:
            num_beat += deck.count(card) * (deck.count(card) - 1)
    
    # Check for flush
    suits = [card // 13 for card in my_cards + flop + [turn] + deck]
    for suit in range(4):
        if suits.count(suit) >= 5:
            num_beat += choose(suits.count(suit), 5)
    
    return num_beat / total_hands

def prob_higher_hand_on_river(my_cards, flop, turn, river):
    """Calculate the probability of another player having a higher hand than yours on the river."""
    
    # Remove known cards from the deck
    deck = [i for i in range(52) if i not in my_cards + flop + [turn] + [river]]
    
    # Total number of possible opponent hands
    total_hands = choose(len(deck), 2)
    
    # Number of hands that beat your hand
    num_beat = 0
    
    # Check for sets
    for card in set(my_cards + flop + [turn] + [river]):
        num_beat += choose(deck.count(card), 2)
    
    # Check for two pairs
    for card in set(my_cards + flop + [turn] + [river]):
        if deck.count(card) >= 2:
            num_beat += deck.count(card) * (deck.count(card) - 1)
    
    # Check for flush
    suits = [card // 13 for card in my_cards + flop + [turn] + [river] + deck]
    for suit in range(4):
        if suits.count(suit) >= 5:
            num_beat += choose(suits.count(suit), 5)
    
    return num_beat / total_hands

# Example usage:
my_cards = [0, 1]  # Replace these with your own two cards
flop = [2, 3, 4]   # Replace these with the flop cards
turn = 5           # Replace this with the turn card
river = 6          # Replace this with the river card

print(f"Probability of a higher hand on the flop: {prob_higher_hand_on_flop(my_cards, flop) * 100:.4f}%")
print(f"Probability of a higher hand on the turn: {prob_higher_hand_on_turn(my_cards, flop, turn) * 100:.4f}%")
print(f"Probability of a higher hand on the river: {prob_higher_hand_on_river(my_cards, flop, turn, river) * 100:.4f}%")
