from database import DBConnection
from api import APIConnection

import json
import time

def main():
    database = DBConnection()
    api = APIConnection()
    while True:
        players = database.get_players() 
        
        for each in players:
            puuid = each['puuid']
            print(f"Getting matches for player {puuid}")
            matches, rate_limit = api.get_player_matches(puuid)

            for matchid in matches:
                print(matchid)
                if not database.match_exists(matchid):
                    print(f"Match {matchid} does not exist. Adding...")
                    match_data, rate_limit = api.get_match_data(matchid)
                    match_data = match_data.json()
                    print(match_data)
                    player1, player2 = match_data["metadata"]["participants"]

                    database.insert_players(player1)
                    database.insert_players(playr2)

                    
                    database.insert_matches(match_data.json())

        time.sleep(60)

if __name__ == "__main__":
    main()
    
