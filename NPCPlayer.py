from Player import Player  
from phevaluator import evaluate_cards
import numpy as np

class NPCPlayer(Player):
    def __init__(self, name, chips, strategy):
        super().__init__(name, chips)
        self.strategy = strategy  

    def decide_action(self, dealer):
        """
        Decides the action to take based on game context and AI strategy.
        """
        game_context = {
            'highest_bet': dealer.highest_bet,
            'pot': dealer.pot,
            'community_cards': dealer.river,
            'player_hand': self.hand,
            'available_cards': dealer.deck.deck  
        }
        action = self.strategy.determine_action(game_context)
        self.execute_action(action, dealer)

    def execute_action(self, action, dealer):
        """
        Executes the action decided by the AI.
        """
        if action['type'] == 'fold':
            self.fold()
        elif action['type'] == 'call':
            amount_to_call = dealer.highest_bet - self.bet
            self.call(amount_to_call)
        elif action['type'] == 'raise':
            amount_to_raise = action['amount']
            self.raise_bet(amount_to_raise)

    def evaluate_hand_strength(self, community_cards):
        """
        Evaluates the hand strength using phevaluator or any other chosen method.
        """
        hand_cards = [f"{card.rank}{card.suit}" for card in self.hand + community_cards]
        return evaluate_cards(*hand_cards)

#Strategy Class
class AIStrategy:
    def determine_action(self, context):
        # Simplified decision-making process
        hand_strength = evaluate_cards(*[f"{card.rank}{card.suit}" for card in context['player_hand'] + context['community_cards']])
        if hand_strength < 1000:  # Simplified condition for strong hands
            return {'type': 'raise', 'amount': context['highest_bet'] + 100}
        elif hand_strength < 2000:
            return {'type': 'call'}
        else:
            return {'type': 'fold'}

# Usage in game loop
#npc_player = NPCPlayer("AI Bot", 1000, AIStrategy())
#npc_player.decide_action(dealer)
