from database.DatabaseConnection import DatabaseConnection
from src.DataPipeline import DataPipeline
from dotenv import find_dotenv
from random import choice

if __name__ == "__main__":

    dotenv_path = find_dotenv()
    db = DatabaseConnection(dotenv_path)
    data_pipeline = DataPipeline(dotenv_path)

    tiers = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]

    # ban_1-5 is blue_side, ban_6-10 is red_side

    summoner_id = data_pipeline.get_random_user_from_tier(choice(tiers))
    matches = data_pipeline.get_user_matches(summoner_id)
    for match in matches:
        result = data_pipeline.get_match_data(match)
        if result is not None:
            match_data, player_data, ban_data = result

            db_match_rows = db.add_match(match_data)
            for player in player_data:
                db.add_player_data(player)
            match_id = match_data["match_id"]
            bans = ban_data["blue"] + ban_data["red"]
            db.add_champion_bans(match_id, bans)
