from dotenv import load_dotenv
import os

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
