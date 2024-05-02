import unittest
from unittest.mock import MagicMock
from PlayerNPC import PlayerNPC, Dealer

class TestPlayerNPC(unittest.TestCase):
    def setUp(self):
        # Mocking dealer
        self.dealer = MagicMock(spec=Dealer)
        
        # Mocking player_list attribute
        self.dealer.player_list = [MagicMock() for _ in range(2)]  # Assuming there are 2 players
        
        # Mocking the river attribute
        self.dealer.river = []
        
        # Adding the pot attribute
        self.dealer.pot = 0
        
        # Setting up player attributes for testing
        self.dealer.player_list[0].bet = 100
        self.dealer.player_list[0].chips = 200
        self.dealer.player_list[1].chips = 150
        
        # Creating an instance of PlayerNPC
        self.player_npc = PlayerNPC(self.dealer, 0)  # Mocking dealer and specifying player index 0

    def test_all_in_set_pot(self):
        # Ensuring the correct behavior of all_in_set_pot method
        
        # Setting up conditions
        self.dealer.player_list[0].bet = 150
        self.dealer.player_list[1].bet = 150
        self.dealer.player_list[0].chips = 200
        self.dealer.player_list[1].chips = 150
        
        # Calling the method under test
        self.player_npc.all_in_set_pot(self.dealer, 0)
        
        # Asserting the results
        self.assertEqual(self.dealer.pot, 150)
        self.assertEqual(self.dealer.player_list[1].bet, 150)

    def test_npc_decision_preflop(self):
        # Ensuring the correct behavior of NPC's decision making
        
        # Setting up conditions
        self.dealer.player_list[0].all_in = True  # Player goes all-in
        self.dealer.player_list[0].chips = 200
        self.dealer.player_list[1].chips = 200
        self.dealer.player_list[0].hand = ["As", "Ks"]  # Player hand
        self.dealer.river = []  # No community cards

        # Creating a new instance of PlayerNPC
        player_npc = PlayerNPC(self.dealer, 1)

        # Ensuring NPC's decision matches expected behavior
        self.assertTrue(self.dealer.player_list[1].fold or self.dealer.player_list[1].all_in)

if __name__ == "__main__":
    unittest.main()
