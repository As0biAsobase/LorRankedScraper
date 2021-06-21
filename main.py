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
            matches = api.get_player_matches(puuid)
            print(matches)
            for matchid in matches:
                print(matchid)
                if not database.match_exists(matchid):
                    print(f"Match {matchid} does not exist. Adding...")
                    match_data, status_code = api.get_match_data(matchid)

                    print(match_data)
                    if status_code == 200:
                        player1, player2 = match_data["metadata"]["participants"]
                        
                        player1_data = api.get_player_data(player1)
                        player2_data = api.get_player_data(player2)

                        database.insert_players(player1_data)
                        database.insert_players(player2_data)
                        
                        database.insert_matches(match_data)

        time.sleep(60)

if __name__ == "__main__":
    main()
    
