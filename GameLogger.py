import json

class GameLogger:
    """
    Handles logging of game results and provides functions for retrieving player statistics.

    Attributes:
        file_name (str): The file path for storing game logs in JSON format.
        data (dict): A dictionary to store player scores and other relevant data.
    """
    def __init__(self, file_name='game_log.json'):
        """
        Initializes the game logger, loading existing game data from a file, or creating a new file if not present.

        Parameters:
            file_name (str): The name of the file where game data is stored.
        """
        self.file_name = file_name
        try:
            with open(self.file_name, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {}

    def log_winner(self, winner_name, chips):
        """
        Logs the winner of a game along with the chips won.

        Parameters:
            winner_name (str): The name of the player who won.
            chips (int): The number of chips the player won.
        """
        if winner_name in self.data:
            self.data[winner_name] += chips
        else:
            self.data[winner_name] = chips
        self.save_log()

    def save_log(self):
        """
        Saves the current game data to a JSON file.
        """
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_top_players(self, top_n=5):
        """
        Retrieves the top players based on the chips won.

        Parameters:
            top_n (int): The number of top players to retrieve.

        Returns:
            list: A sorted list of tuples, where each tuple contains a player's name and their chip count.
        """
        return sorted(self.data.items(), key=lambda item: item[1], reverse=True)[:top_n]
