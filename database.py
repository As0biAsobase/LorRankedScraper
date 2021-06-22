import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import re
import sys

class DBConnection:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.client = MongoClient(os.getenv("MONGODB_KEY"))

    def get_players(self):
        result = self.client['natum-perdere']['PlayersyRiotID'].find({})
        print(result)
        result = list(result)

        return result

    def player_exists(self, puuid):
        result = self.client['natum-perdere']['PlayersyRiotID'].find({ "puuid" : puuid})
        
        exists = True
        if len(list(result)) == 0:
            exists = False 
        return exists 

    def insert_players(self, player_data):
        self.client['natum-perdere']['PlayersyRiotID'].insert_one(player_data)

    def match_exists(self, matchid):
        result = self.client['natum-perdere']['LorMatches'].find({ "metadata.match_id" : matchid })

        exists = True
        if len(list(result)) == 0:
            exists = False 
        return exists 

    def insert_matches(self, match):
        self.client['natum-perdere']['LorMatches'].insert_one(match)