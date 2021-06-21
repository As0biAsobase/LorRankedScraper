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

        offset = 0
        last_iteration = timer()
        match_list_counter = 0

        while True:
            players = database.get_players() 
            players = players[offset::]
            
            for each in players:
                puuid = each['puuid']
                print(f"Getting matches for player {puuid}")
                matches = api.get_player_matches(puuid)
                match_list_counter += 1
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

            players_count = len(database.get_players())
            
            if players_count-len(players) < 200-match_list_counter:
                offset = len(players)
            else:
                if offset + 200 > players_count:
                    offset = len(players)
                else:
                    offset += 200

                if offset > 600:
                    offset = 0

                difference = timer() - last_iteration
                print(f"Rate limit reached, waiting for {difference:.0f} secs")
                time.sleep(3600 - difference)
                last_iteration = timer()
                match_list_counter = 0
                


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
    
