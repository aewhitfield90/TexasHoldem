from phevaluator.evaluator import evaluate_cards
from DeckBuilder import Deck
import ctypes, pygame, sys, pygame_widgets



if __name__ == '__main__':
    screen = pygame.display.set_mode((1600, 900))
    deck = Deck()
    player_cards = []
    #for card in range(5):
    #    player_cards = player_cards.append(f"{card.rank}{card.suit}")
    #rank = evaluate_cards(player_cards[0], player_cards[1], player_cards[2], player_cards[3], player_cards[4])
    """
    Royal Flush		0.003232062	
    Straight Flush		0.027850748	
    Four-of-a-kind		0.168067227	
    Full House		2.596102271	
    Flush			3.025494123
    Straight		4.619382087	
    Three-of-a-kind		4.829869755	
    Two pair		23.49553641	
    Pair			43.82254574	
    High card		17.41191958
    """
    #rank for royal strait flush #1

    #rank range for flushes 
    highstraitflush = evaluate_cards("9H", "TH", "JH", "QH", "KH") #2
    lowstraitflush = evaluate_cards("2H", "2H", "4H", "5H", "AH") #10
    
    #rank range for four of a kind 
    fourOfaKindHigh = evaluate_cards("AH", "AD", "AC", "AS", "KH") #11
    fourOfaKindLow = evaluate_cards("2H", "2D", "2C", "2S", "3D") #166
    
    #rank range of fullhouse 
    fullhousehigh = evaluate_cards("AH","AD", "AS", "KC", "KH",) #167
    fullhouselow = evaluate_cards("2H","2D", "2S", "3C", "3H",) #322

    #rank range of flush 
    highflush = evaluate_cards("9D", "JD", "QD", "KD", "AD") #323
    lowflush = evaluate_cards("2D", "3D", "4D", "7D", "5D") #1599

    #rank range of strait 
    highstrait = evaluate_cards("TD", "JH", "QH", "KS", "AH") #1600
    lowstrait = evaluate_cards("2D", "3H", "4C", "5S", "AD") #1609

    #rank range of three of a kind 
    highthree= evaluate_cards("AD", "AH", "AC", "KS", "QD") #1610
    lowthree  = evaluate_cards("2H", "2D", "2S", "3S", "4H") #2467

    #rank range of two pair 
    hightwopair= evaluate_cards("AD", "AH", "KC", "KS", "QD") #2468
    lowtwopair  = evaluate_cards("2H", "2D", "3S", "3D", "4H") #3325

    #rank range of pair 
    highpair= evaluate_cards("AD", "AH", "KC", "QS", "JD") #3326
    lowpair  = evaluate_cards("2H", "2D", "3S", "4D", "5H") #6185

    #rank range of high card 
    highcard= evaluate_cards("AD", "KH", "QC", "JS", "9D") #6186
    lowcard  = evaluate_cards("2H", "3D", "4S", "5D", "7H") #7462

    print(lowcard)