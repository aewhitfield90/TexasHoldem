from phevaluator.evaluator import evaluate_cards
from River import Dealer

class PlayerNPC:
    def __init__(self, dealer): #creates a new deck and shuffles it
        print("entered PlayerNPC")
        for player in dealer.player_list: #takes list of Player objects
            if player.NPC == True: #only if its an NPC player will it calculate choices
                #take current river + NPC hand cards, evaluate ranks, make decisions on rank found
                cards = player.hand + dealer.river
                print(len(cards))
                if len(cards) == 5: #evaluates flop hand
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4])
                    if highestHand > 6185: #pair or better
                        player.all_in = True
                    else:
                        player.fold = True
                elif len(cards) == 6: #evaluates turn hand
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5])
                    if highestHand > 3325: #pair or better
                        player.all_in = True
                    else:
                        player.fold = True
                elif len(cards) == 7: # evaluates river hand
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6])
                    if highestHand > 6185: #pair or better
                        player.all_in = True
                    else:
                        player.fold = True
                else:
                    print("the river plus the hand does not equal 5, 6, or 7")

            else:
                return
                
