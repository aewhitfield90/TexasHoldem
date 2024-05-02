import unittest
from unittest.mock import patch
from DeckBuilder import Card, Deck, ShortDeck

class TestCard(unittest.TestCase):
    @patch('DeckBuilder.pygame')
    def test_card_creation(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        card = Card('H', 'A', load_images=False)  # Disable loading images for testing
        self.assertEqual(card.suit, 'H')
        self.assertEqual(card.rank, 'A')
        self.assertFalse(card.show)  # By default, card should be face down
        self.assertEqual(card.position, (500, 500))

    @patch('DeckBuilder.pygame')
    def test_card_show_hide(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        card = Card('D', 'K', load_images=False)  # Disable loading images for testing
        card.show_card()
        self.assertTrue(card.show)
        card.hide_card()
        self.assertFalse(card.show)

class TestDeck(unittest.TestCase):
    @patch('DeckBuilder.pygame')
    def test_deck_creation(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        deck = Deck(load_images=False)  # Disable loading images for testing
        self.assertEqual(len(deck.deck), 52)

    @patch('DeckBuilder.pygame')
    def test_deck_shuffle(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        deck = Deck(load_images=False)  # Disable loading images for testing
        original_order = deck.deck[:]
        deck.shuffle_deck()
        self.assertNotEqual(original_order, deck.deck)

    @patch('DeckBuilder.pygame')
    def test_deck_deal_card(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        deck = Deck(load_images=False)  # Disable loading images for testing
        card = deck.deal_card()
        self.assertIsInstance(card, Card)

class TestShortDeck(unittest.TestCase):
    @patch('DeckBuilder.pygame')
    def test_short_deck_creation(self, mock_pygame):
        mock_pygame_initialized = mock_pygame.init()
        short_deck = ShortDeck(load_images=False)  # Disable loading images for testing
        self.assertEqual(len(short_deck.deck), 20)  # Only high cards in short deck

if __name__ == '__main__':
    unittest.main()
