import requests
import json

def fetch_all_games(username, output_file="all_chess_games.json"):
    """
    Fetches all available chess games for the specified username from Chess.com API.
    
    Args:
        username (str): Chess.com username.
        output_file (str): Path to save the fetched games as a JSON file.
    
    Returns:
        list: List of all games fetched from the API.
    """
    base_url = f"https://api.chess.com/pub/player/{username}/games/archives"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch the list of archives
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Check for errors
        archives = response.json().get("archives", [])
        
        all_games = []
        print(f"Found {len(archives)} archives for {username}. Fetching games...")

        # Fetch games from each archive
        for archive_url in archives:
            print(f"Fetching games from {archive_url}...")
            archive_response = requests.get(archive_url, headers=headers)
            archive_response.raise_for_status()
            games = archive_response.json().get("games", [])
            all_games.extend(games)  # Add games to the main list

        # Save all games to a JSON file
        with open(output_file, "w") as file:
            json.dump(all_games, file, indent=4)

        print(f"Fetched {len(all_games)} games in total. Saved to {output_file}.")
        return all_games
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except json.JSONDecodeError:
        print("Error decoding the JSON response.")
    return []

if __name__ == "__main__":
    # Replace 'your_username' with your Chess.com username
    username = "ardaylmaz"
    
    # Fetch all games and save to a JSON file
    games = fetch_all_games(username)
    print(f"Fetched {len(games)} games for user {username}.")
