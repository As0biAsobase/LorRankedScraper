from self.database import DBConnection
from self.api import APIConnection

import json
from timeit import default_timer as timer
import time
import random

class Scraper():
    def __init__(self):
        self.start = timer()
        self.requests = 0
        self.match_list_counter = 0
        self.match_data_counter = 0
        self.hourly_clock = timer()
        self.database = DBConnection()
        self.api = APIConnection()

    def start_scraping(self):
        while True:
            players = self.database.get_players() 
            
            for each in players:
                puuid = each['puuid']
                print(f"Getting matches for player {each["gameName"]} with id: {puuid}")
                matches = self.api.get_player_matches(puuid)
                self.match_list_counter += 1
                self.check_rate_limit()


                for matchid in matches:
                    if not self.database.match_exists(matchid):
                        print(f"Match {matchid} does not exist. Adding...")
                        match_data, status_code = self.api.get_match_data(matchid)
                        self.match_data_counter += 1
                        self.check_rate_limit()

                        if status_code == 200:                            
                            self.database.insert_matches(match_data)        


    def check_rate_limit(self):
        self.requests += 1

        difference = timer() - self.start
        if self.match_list_counter == 200 or self.match_data_counter == 100:
            difference = 3600 - (timer() - self.hourly_clock)
            print(f"Rate limit reached, waiting for {difference:.0f} secs")
            time.sleep(difference)
            self.start = timer()
            self.hourly_clock = timer()
            self.requests = 0
            self.match_data_counter = 0 
            self.match_list_counter = 0
        else:
            if difference > 120:
                self.requests = 0
                self.start = timer()
            else:
                if self.requests >= 200:
                    print(f"Rate limit reached, waiting for {difference:.0f} secs")
                    time.sleep(difference)
                    self.start = timer()
                    self.requests = 0
                


if __name__ == "__main__":
    scraper = Scraper()
    scraper.start_scraping()
    
