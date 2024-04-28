from phevaluator.evaluator import evaluate_cards
from River import Dealer
import random

class PlayerNPC:
    def __init__(self, dealer, nameInList): 
        print("entered PlayerNPC")
        #builds a card array of current flop/turn/river + NPCplayer hand for evaluating best hand rank
        cards = []
        for card in dealer.player_list[nameInList].hand:
            cards.append(f"{card.rank}{card.suit}")
        for card in dealer.river:
            cards.append(f"{card.rank}{card.suit}")
        #cards = dealer.player_list[nameInList].hand + dealer.river
        #print(len(cards))
        #print(cards)
        #for player in dealer.player_list: #takes list of Player objects
            #if player.NPC == True: #only if its an NPC player will it calculate choices
        
        if dealer.player_list[nameInList].NPC == True and dealer.player_list[0].all_in == True and (dealer.player_list[nameInList].all_in == False and dealer.player_list[nameInList].fold == False): #only if its an NPC player and hasn't gone all in yet or folded will it calculate choices
                #print("entered NPC")
                #take current river + NPC hand cards, evaluate ranks, make decisions on rank found
                print(len(cards))
                if len(cards) == 2: #evaluates two card hand before flop
                    print("entered NPC 2 card check")
                    #highestHand = evaluate_cards(cards[0],cards[1])
                    if random.randrange(0,3) == 0: #randomly decides to go all in or fold on player all in choice
                        dealer.player_list[nameInList].all_in = True
                        self.all_in_set_pot(dealer, nameInList)
                        print(dealer.player_list[nameInList].name + " went all in!")
                    else:
                        dealer.player_list[nameInList].fold = True
                        print(dealer.player_list[nameInList].name + " FOLDED")
                                        
                elif len(cards) == 5: #evaluates flop hand
                    print("entered NPC 5 card check")
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4])
                    if highestHand > 6185: #pair or better
                        dealer.player_list[nameInList].all_in = True
                        self.all_in_set_pot(dealer, nameInList)
                        print(dealer.player_list[nameInList].name + " went all in!")
                    else:
                        dealer.player_list[nameInList].fold = True
                        print(dealer.player_list[nameInList].name + " FOLDED")
                elif len(cards) == 6: #evaluates turn hand
                    print("entered NPC 6 card check")
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5])
                    if highestHand > 3325: #pair or better
                        dealer.player_list[nameInList].all_in = True
                        self.all_in_set_pot(dealer, nameInList)
                        print(dealer.player_list[nameInList].name + " went all in!")
                    else:
                        dealer.player_list[nameInList].fold = True
                        print(dealer.player_list[nameInList].name + " FOLDED")
                elif len(cards) == 7: # evaluates river hand
                    print("entered NPC 7 card check")
                    highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6])
                    if highestHand > 6185: #pair or better
                        dealer.player_list[nameInList].all_in = True
                        self.all_in_set_pot(dealer, nameInList)
                        print(dealer.player_list[nameInList].name + " went all in!")
                    else:
                        dealer.player_list[nameInList].fold = True
                        print(dealer.player_list[nameInList].name + " FOLDED")
                else:
                    print("the river plus the hand does not equal 2, 5, 6, or 7")
                dealer.player_list[nameInList].check = True
        elif dealer.player_list[0].check == True: #when player has checked
            print("entered if Player Checks")
            if len(cards) == 2: #decides to check, raise or fold pre-flop
                    print("entered Player checks, 2 card hand (pre flop)")
                #if random.randrange(0,2) == 0: #randomly decides to check
                #if card[0].rank == card[1].rank: #if NPC has a starting pair
                #    if random.randrange(0,2) == 0: #randomly decides to check or raise
                #        dealer.player_list[nameInList].check = True
                #    else:
                #        dealer.player_list[nameInList].bet_raise(50)
                #        dealer.pot += dealer.player_list[nameInList].bet
                #else:
                    self.chance_to_raise(dealer, nameInList)
                    #if random.randrange(0,10) == 0: #if cards arent a pair randomly decides to check or raise
                    #    dealer.player_bet(dealer.player_list[nameInList], 50)
                    #else:
                    #    dealer.player_call(dealer.player_list[nameInList])

            elif len(cards) == 5:
                print("entered Player checks, 5 card hand")
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4])
                if highestHand >= 6185 and highestHand <= 3326: #if flop gives a pair, check
                    dealer.player_call(dealer.player_list[nameInList])
                elif highestHand >= 3325 and highestHand <= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 50)
                elif highestHand >= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 100)
                else:
                    dealer.player_list[nameInList].fold_hand()
            elif len(cards) == 6:
                print("entered Player checks, 6 card hand")
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5])
                if highestHand >= 6185 and highestHand <= 3326: #if a pair, check
                    dealer.player_call(dealer.player_list[nameInList])
                elif highestHand >= 3325 and highestHand <= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 50)
                elif highestHand >= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 100)
                else:
                    dealer.player_list[nameInList].fold_hand()
            elif len(cards) == 7:
                print("entered Player checks, 7 card hand")
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6])
                if highestHand >= 6185 and highestHand <= 3326: #if a pair, check
                    dealer.player_list[nameInList].check = True
                elif highestHand >= 3325 and highestHand <= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 50)
                elif highestHand >= 1610:
                    self.chance_to_raise(dealer, nameInList)
                    #dealer.player_bet(dealer.player_list[nameInList], 100)
                else:
                    dealer.player_list[nameInList].fold_hand()
            else:
                print("the river plus the hand does not equal 2, 5, 6, or 7")
        elif dealer.player_list[nameInList].bet_gap != 0: #when player has increased bet
            print("entered if there is a bet gap")
            rand = random.randrange(0,4)
            if len(cards) == 2: #decides to check, raise or fold based if there is a bet gap
                if rand > 1: #50% chance to check
                    dealer.player_call(dealer.player_list[nameInList]) #calls amount of gap
                elif rand == 1: #25% chance to bet
                    self.chance_to_raise(dealer, nameInList)
                else: #25% chance to fold
                    dealer.player_list[nameInList].fold_hand()

            elif len(cards) == 5:
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4])
                if highestHand >= 6185 and highestHand <= 3326: #pair, check
                    dealer.player_call(dealer.player_list[nameInList])
                elif highestHand >= 3325 and highestHand <= 1610: #triple, raise
                    self.chance_to_raise(dealer, nameInList)
                elif highestHand >= 1610: #higher than triple, raise
                    self.chance_to_raise(dealer, nameInList)
                else:
                    dealer.player_list[nameInList].fold_hand()
            elif len(cards) == 6:
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5])
                if highestHand >= 6185 and highestHand <= 3326: #pair, check
                    dealer.player_call(dealer.player_list[nameInList])
                elif highestHand >= 3325 and highestHand <= 1610:#triple, raise
                    self.chance_to_raise(dealer, nameInList)
                elif highestHand >= 1610:
                    self.chance_to_raise(dealer, nameInList)
                else:
                    dealer.player_list[nameInList].fold_hand()
            elif len(cards) == 7:
                highestHand = evaluate_cards(cards[0],cards[1],cards[2],cards[3],cards[4],cards[5],cards[6])
                if highestHand >= 6185 and highestHand <= 3326: #pair, check
                    dealer.player_call(dealer.player_list[nameInList])
                elif highestHand >= 3325 and highestHand <= 1610:#triple, raise
                    self.chance_to_raise(dealer, nameInList)
                elif highestHand >= 1610:#higher than triple, raise
                    self.chance_to_raise(dealer, nameInList)
                else:
                    dealer.player_list[nameInList].fold_hand()
            else:
                print("the river plus the hand does not equal 2, 5, 6, or 7")

        else:
            return

    def all_in_set_pot(self, dealer, nameInList):
        if dealer.player_list[0].bet <= dealer.player_list[nameInList].chips: #if player bets all in with lower or equal chip value, NPC does bet raise of that amount
            dealer.player_list[nameInList].bet_raise(dealer.player_list[0].bet)
            dealer.pot += dealer.player_list[0].bet
        else:
            dealer.player_list[nameInList].bet_raise(dealer.player_list[nameInList].chips) # if player has larger chip amount than NPC, NPC bets rest of chips it has
            dealer.pot += dealer.player_list[nameInList].chips
                
    def chance_to_raise(self, dealer, nameInList):
        if random.randrange(0,10) == 0: #if cards arent a pair randomly decides to check or raise
            dealer.player_bet(dealer.player_list[nameInList], 50)
        else:
            dealer.player_call(dealer.player_list[nameInList])
