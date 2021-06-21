from database import DBConnection
from api import APIConnection

import json
from timeit import default_timer as timer
import time

class Scraper():
    def __init__(self):
        self.start = timer()
        self.requests = 0

    def start_scraping(self):
        database = DBConnection()
        api = APIConnection()
        
        while True:
            players = database.get_players() 
            
            for each in players:
                puuid = each['puuid']
                print(f"Getting matches for player {puuid}")
                matches = api.get_player_matches(puuid)
                self.check_rate_limit()


                for matchid in matches:
                    if not database.match_exists(matchid):
                        print(f"Match {matchid} does not exist. Adding...")
                        match_data, status_code = api.get_match_data(matchid)
                        self.check_rate_limit()

                        if status_code == 200:
                            player1, player2 = match_data["metadata"]["participants"]
                            
                            player1_data = api.get_player_data(player1)
                            player2_data = api.get_player_data(player2)

                            database.insert_players(player1_data)
                            database.insert_players(player2_data)
                            
                            database.insert_matches(match_data)

    def check_rate_limit(self):
        self.requests += 1

        difference = timer() - self.start
        if difference > 120:
            self.requests = 0
            self.start = timer()
        else:
            if self.requests >= 200:
                print(f"Rate limit reached, waiting for {difference:.0f} secs")
                time.sleep(difference)
                time.start = timer()
                self.requests = 0
                


if __name__ == "__main__":
    scraper = Scraper()
    scraper.start_scraping()
    
