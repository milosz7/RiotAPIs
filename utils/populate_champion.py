import requests
from dotenv import find_dotenv
from src.DatabaseConnection import DatabaseConnection


def fetch_champions():
    try:
        versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
        version = versions[0]
        champions = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()
        champions = champions["data"]

        output = []

        for champion in champions:
            name = champions[champion]["name"]
            champ_id = int(champions[champion]["key"])
            output.append((champ_id, name))

        return output

    except requests.exceptions.RequestException:
        print("Error fetching champions.")


def main():
    output = fetch_champions()
    dotenv_path = find_dotenv()
    connection = DatabaseConnection(dotenv_path)
    for champ_id, name in output:
        name = name.replace("'", "''")
        connection.add_champion(champ_id, name)


if __name__ == "__main__":
    main()
