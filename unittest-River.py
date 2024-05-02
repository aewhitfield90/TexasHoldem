import unittest
from unittest.mock import MagicMock
from River import Dealer
from Player import Player

class TestDealer(unittest.TestCase):
    def setUp(self):
        # Mock Pygame functions to avoid initialization errors
        mock_image_load = MagicMock()
        mock_image_load.return_value = MagicMock(convert_alpha=MagicMock())

        with unittest.mock.patch('pygame.image.load', mock_image_load), \
             unittest.mock.patch('pygame.display', MagicMock()), \
             unittest.mock.patch('pygame.init', MagicMock()):

            # Initialize a Dealer instance with mock players
            self.player1 = Player("Player 1", 1000)
            self.player2 = Player("Player 2", 1000)
            self.dealer = Dealer([self.player1, self.player2])

    def test_add_player(self):
        # Test adding a player to the game
        self.assertEqual(len(self.dealer.player_list), 2)
        new_player = Player("Player 3", 1000)
        self.dealer.add_player(new_player)
        self.assertEqual(len(self.dealer.player_list), 3)

    def test_remove_player(self):
        # Test removing a player from the game
        self.assertEqual(len(self.dealer.player_list), 2)
        self.dealer.remove_player("Player 1")
        self.assertEqual(len(self.dealer.player_list), 1)

    def test_deal_player_cards(self):
        # Test dealing cards to players
        self.assertEqual(len(self.player1.hand), 0)
        self.assertEqual(len(self.player2.hand), 0)
        self.dealer.deal_player_cards()
        self.assertEqual(len(self.player1.hand), 1)
        self.assertEqual(len(self.player2.hand), 1)

    def test_player_bet(self):
        # Test player betting functionality
        initial_pot = self.dealer.pot
        initial_player_chips = self.player1.chips
        self.dealer.player_bet(self.player1, 100)
        self.assertEqual(self.dealer.pot, initial_pot + 100)
        self.assertEqual(self.player1.chips, initial_player_chips - 100)

    # Add more test cases for other functions as needed

if __name__ == '__main__':
    unittest.main()
