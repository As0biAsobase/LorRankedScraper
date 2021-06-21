from database import DBConnection as database 
from api import APIConnection as api 

import json
import time

def main():
    while True:
        players = database.get_players() 
        
        for each in players:
            puuid = each['puuid']
            print(f"Getting matches for player {puuid}")
            matches = api.get_player_matches(puuid)

            for matchid, rate_limit in matches:
                if not database.match_exists(matchid)
                    print(f"Match {matchid} does not exist. Adding...")
                    match = match.json() 
                    player1, player2 = match["metadata"]["participants"]

                    database.insert_players(player1)
                    database.insert_players(playr2)

                    match_data = api.get_match_data(matchid)
                    database.insert_matches(match_data.json())

        time.sleep(60)

if __name__ == "__main__":
    main()
    
