import unittest
from unittest.mock import Mock
import pygame
from main import Game  # Assuming your Game class is in a file named 'main.py'

class TestGame(unittest.TestCase):
    def test_initial_game_state(self):
        game = Game()
        self.assertEqual(game.game_state, "main_menu")

    def test_player_count(self):
        game = Game()
        self.assertEqual(game.player_num, 5)  # Assuming default player count is 5

    # Add more test cases as needed...

    def test_game_state_transition(self):
        game = Game()
        self.assertEqual(game.game_state, "main_menu")

        # Simulate a button click to transition to in-game state
        game.game_state = "in_game"
        
        # Verify that the game state has changed
        self.assertEqual(game.game_state, "in_game")


if __name__ == "__main__":
    unittest.main()
