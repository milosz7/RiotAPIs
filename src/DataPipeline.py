from dotenv import load_dotenv
import os
import numpy as np
import requests


class DataPipeline:
    """
    Class used for fetching data from Riot API.

    :param dotenv_path: path to the .env file containing the API key.

    Example usage:

    >>> dotenv_path = '.env'
    >>> print(os.path.abspath(dotenv_path))
    >>> data_pipeline = DataPipeline(dotenv_path)
    >>> summoner_id = data_pipeline.get_random_user_from_tier('GOLD')
    >>> print(summoner_id)
    >>> matches = data_pipeline.get_user_matches(summoner_id)
    >>> print(matches)
    >>> for match in matches:
    >>>     result = data_pipeline.get_match_data(match)
    >>>     if result is not None:
    >>>         match_data, player_data, ban_data = result
    >>>         # further preprocessing...
    """

    def __init__(self, dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        api_key_env_name = "RIOT_API_KEY"
        self.api_key = os.getenv(api_key_env_name)

        if self.api_key is None:
            raise ValueError(f"Environment variable {api_key_env_name} not found.")

        self.divisions = ["I", "II", "III", "IV"]
        self.tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
        self.queue = "RANKED_SOLO_5x5"
        self.europe_base_url = "https://europe.api.riotgames.com"
        self.euw1_base_url = "https://euw1.api.riotgames.com"
        self.ranked_queue_id = 420
        self.role_mapping = {
            "TOP": "TOP",
            "JUNGLE": "JNG",
            "MIDDLE": "MID",
            "BOTTOM": "BOT",
            "UTILITY": "SUPP"
        }

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

        if not response:
            return None

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

    @staticmethod
    def declare_team_first(blue, red, column):
        if blue[column]:
            return "BLUE"
        elif red[column]:
            return "RED"
        else:
            return None

    @staticmethod
    def get_bans(team):
        return [ban["championId"] for ban in team["bans"]]

    def get_match_data(self, match_id):
        match_url = "{}/lol/match/v5/matches/{}?api_key={}".format(self.europe_base_url,
                                                                   match_id,
                                                                   self.api_key)
        response = requests.get(match_url)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}")

        response = response.json()
        game_info = response["info"]
        if game_info["queueId"] != self.ranked_queue_id:
            return None

        if game_info["endOfGameResult"] != "GameComplete":
            return None

        game_duration_in_s = game_info["gameDuration"]
        game_duration_in_min = game_duration_in_s / 60

        teams = game_info["teams"]
        blue_team = teams[0]
        red_team = teams[1]

        winner = self.declare_team_first(blue_team, red_team, "win")
        first_dragon = self.declare_team_first(blue_team["objectives"]["dragon"],
                                               red_team["objectives"]["dragon"],
                                               "first")
        first_baron = self.declare_team_first(blue_team["objectives"]["baron"],
                                              red_team["objectives"]["baron"],
                                              "first")
        player_data = self.get_participants_data(game_info["participants"], game_duration_in_min, match_id)

        is_surrender = game_info["participants"][0]["gameEndedInSurrender"]

        red_bans = self.get_bans(blue_team)
        blue_bans = self.get_bans(red_team)
        ban_data = {
            "blue": blue_bans,
            "red": red_bans
        }

        match_data = {
            "match_id": match_id,
            "win": winner,
            "first_drake": first_dragon,
            "first_baron": first_baron,
            "game_duration": game_duration_in_min,
            "dragon_kills": blue_team["objectives"]["dragon"]["kills"] + red_team["objectives"]["dragon"]["kills"],
            "surrender": is_surrender,
        }

        return match_data, player_data, ban_data

    def get_participants_data(self, participants_raw, game_duration_in_min, match_id):
        player_data = []

        for player in participants_raw:
            player_info = dict()
            player_info["match_id"] = match_id
            player_info["`rank`"], player_info["division"] = self.get_player_rank(player["summonerId"])
            player_info["kills"] = player["kills"]
            player_info["deaths"] = player["deaths"]
            player_info["assists"] = player["assists"]
            player_info["dmg_per_min"] = player["challenges"]["damagePerMinute"]
            player_info["gold_per_min"] = player["challenges"]["goldPerMinute"]
            player_info["vision_score_per_min"] = player["challenges"]["visionScorePerMinute"]
            player_info["champion_id"] = player["championId"]
            player_info["team_id"] = player["teamId"]
            player_info["lane"] = self.role_mapping[player["teamPosition"]]
            player_info["wards_placed"] = player["wardsPlaced"]
            player_info["wards_destroyed"] = player["wardsKilled"]
            player_info["dmg_taken_per_min"] = player["totalDamageTaken"] / game_duration_in_min
            player_info["first_blood"] = 1 if player["firstBloodKill"] else 0
            player_info["dmg_to_towers"] = player["damageDealtToTurrets"]
            player_info["sight_wards_bought"] = player["sightWardsBoughtInGame"]
            player_info["cs_per_min"] = player["totalMinionsKilled"] / game_duration_in_min
            player_info["missing_pings"] = player["enemyMissingPings"]
            player_info["total_time_dead"] = player["totalTimeSpentDead"]

            player_data.append(player_info)

        return player_data

    def get_player_rank(self, summoner_id):
        division_to_int = {"I": 1, "II": 2, "III": 3, "IV": 4}
        summoner_info_url = "{}/lol/league/v4/entries/by-summoner/{}?api_key={}".format(self.euw1_base_url,
                                                                                        summoner_id,
                                                                                        self.api_key)
        response = requests.get(summoner_info_url)
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code}")
        response = response.json()

        # https://github.com/RiotGames/developer-relations/issues/795
        # IndexError in case the player is unranked
        try:
            response = response[0]
            return response["tier"], division_to_int[response["rank"]]
        except (KeyError, IndexError):
            return None, None
