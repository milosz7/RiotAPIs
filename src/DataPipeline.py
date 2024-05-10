from dotenv import load_dotenv
import os
import numpy as np
import requests

class DataPipeline:
    def __init__(self, dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        api_key_env_name = "RIOT_API_KEY"
        self.api_key = os.getenv(api_key_env_name)

        if self.api_key is None:
            raise ValueError(f"Environment variable f{api_key_env_name} not found.")

        self.divisions = ["I", "II", "III", "IV"]
        self.tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
        self.queue = "RANKED_SOLO_5x5"
        self.europe_base_url = "https://europe.api.riotgames.com"
        self.euw1_base_url = "https://euw1.api.riotgames.com"

    def get_random_user_from_tier(self, tier):
        # tier selected randomly as we don't care about it that much
        division = np.random.choice(self.divisions)

        summoner_id_url = "{}/lol/league-exp/v4/entries/{}/{}/{}?api_key={}".format(self.euw1_base_url,
                                                                        self.queue,
                                                                        tier,
                                                                        division,
                                                                        self.api_key)
        response = requests.get(summoner_id_url)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}")

        response = response.json()
        summoner_id = response[0]["summonerId"]

        return summoner_id


    def get_user_matches(self, summoner_id):
        summoner_info_url = "{}/lol/summoner/v4/summoners/{}?api_key={}".format(self.euw1_base_url,
                                                                                 summoner_id,
                                                                                 self.api_key)
        response = requests.get(summoner_info_url)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}")
        puuid = response.json()["puuid"]

        matches_url = "{}/lol/match/v5/matches/by-puuid/{}/ids?start=0&count=20&api_key={}".format(self.europe_base_url,
                                                                                   puuid,
                                                                                   self.api_key)
        response = requests.get(matches_url)
        return response.json()
