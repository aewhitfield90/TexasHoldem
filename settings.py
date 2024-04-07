#settings files for the game and game UI
TITLE_STRING  = "POKER GAME"
MAX_PLAYERS = 5
BACKGROUND_COLOR = (33, 124, 66)
FPS = 60
WIDTH = 1600
HEIGHT = 900
GAME_FONT = "arialblack"
TEXT_COLOR = (255, 255, 255)
GAME_AUDIO = ''
NAME_LIST = ["Andrew", "Felipe", "Jonathan", "Jose", "Parker"]

# coordinates for cards and player names
#CARDS_X = [760,790,310,340,1200,1230,100,130,1400,1430]
#CARDS_Y = [750,750,280,280,1370,1370,80,80,1350,1350]
CARDS = [(710,650), (835,650), (260,470), (385,470), (1140,470), 
         (1265,470), (70,150), (195,150), (1340,150), (1465,150)]
PLAYER_X = [780,330,1220,130,1420]
PLAYER_Y = [800,620,620,300,300]
RIVER_X = [500,625,750,875,1000]
RIVER_Y = 280



value_dict = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}