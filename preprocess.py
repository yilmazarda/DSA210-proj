import pandas as pd
import json

def preprocess_games(input_file="all_chess_games.json", output_file="cleaned_games.csv", your_username="ardaylmaz"):
    with open(input_file, "r") as file:
        games = json.load(file)

    # Extract relevant fields
    processed_data = []
    for game in games:
        # Determine if you are white or black in this game
        if game["white"]["username"] == your_username:
            color = "white"
            result = game["white"]["result"]
        else:
            color = "black"
            result = game["black"]["result"]

        game_data = {
            "result": result,
            "color": color,
            "opening": game.get("eco", "Unknown"),
            "time": game.get("end_time"),
        }
        processed_data.append(game_data)

    # Create a DataFrame
    df = pd.DataFrame(processed_data)
    df.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}.")

if __name__ == "__main__":
    preprocess_games(your_username="ardaylmaz")
