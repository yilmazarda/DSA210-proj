import pandas as pd
import json

def preprocess_games(input_file="all_chess_games.json", output_file="cleaned_games.csv", your_username="ardaylmaz"):
    with open(input_file, "r") as file:
        games = json.load(file)

    # Extract relevant fields
    processed_data = []
    for game in games:
        # Debug: Print out the game to see which ones might be missing
        print(f"Processing game: {game}")

        # Initialize variables
        white_elo = None
        black_elo = None
        result = "Unknown"
        color = None

        # Check if you are the white player
        if game["white"]["username"].lower() == your_username.lower():
            color = "white"
            result = game["white"].get("result", "Unknown")  # Use get to avoid missing key errors
            white_elo = game["white"].get("rating", None)
            black_elo = game["black"].get("rating", None)
        # Otherwise, you're the black player
        elif game["black"]["username"].lower() == your_username.lower():
            color = "black"
            result = game["black"].get("result", "Unknown")
            white_elo = game["white"].get("rating", None)
            black_elo = game["black"].get("rating", None)
        else:
            # If you're not in the game, skip it
            continue

        # Debug: Print the result for verification
        print(f"Game result for {your_username} (as {color}): {result}")

        # Extract and clean the opening name
        opening_url = game.get("eco", "Unknown")
        if opening_url != "Unknown":
            # Extract the opening name from the URL
            opening_name = opening_url.split('/')[-1].replace('-', ' ').strip()

            # Shorten the opening name by stopping at the first colon ':'
            if ":" in opening_name:
                opening_name = opening_name.split(":")[0]  # Keep only the part before the first colon
        else:
            opening_name = "Unknown Opening"

        # Extract and process the time
        time_epoch = game.get("end_time", None)
        if time_epoch:
            try:
                # Convert the epoch timestamp to a readable datetime
                time = pd.to_datetime(time_epoch, unit='s')
            except Exception as e:
                print(f"Error converting time: {e}")
                time = "Invalid Time"
        else:
            time = "Unknown Time"

        # Add relevant data to the processed list
        game_data = {
            "result": result,
            "color": color,
            "opening": opening_name,
            "time": time,
            "white_elo": white_elo,
            "black_elo": black_elo
        }
        processed_data.append(game_data)

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(processed_data)
    df.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}.")

if __name__ == "__main__":
    preprocess_games(your_username="ardaylmaz")
