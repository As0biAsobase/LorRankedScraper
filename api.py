from dotenv import load_dotenv, find_dotenv
import os
import requests
import json

class APIConnection():
    def __init__(self):
        load_dotenv(find_dotenv())
        self.key = os.getenv("RIOT_API_KEY")

    def get_player_matches(self, uuid):
        headers = {
            "X-Riot-Token": self.key
        }

        r = requests.get(f'https://europe.api.riotgames.com/lor/match/v1/matches/by-puuid/{uuid}')

        headers = r.headers 
        headers = headers
        print(headers)

        rate_limit = False
        if headers["X-Method-Rate-Limit"].split(":")[0] <= headers["X-Method-Rate-Limit-Count"].split(":")[0]:
            rate_limit = True

        r = r.content

        return [r, rate_limit] 

    def get_match_data(self, matchid):
        headers = {
            "X-Riot-Token": self.key
        }

        r = requests.get(f'https://europe.api.riotgames.com/lor/match/v1/matches/{matchid}')
        
        headers = r.headers 
        

        rate_limit = False
        if headers["X-Method-Rate-Limit"].split(":")[0] <= headers["X-Method-Rate-Limit-Count"].split(":")[0]:
            rate_limit = True

        r = r.content

        return [r, rate_limit] 
