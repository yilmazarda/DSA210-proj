import pandas as pd
import json
import re
from datetime import datetime

# Function to convert decimal minutes to minutes:seconds format
def convert_to_minutes_seconds(duration):
    minutes = int(duration)
    seconds = round((duration - minutes) * 60)
    return f"{minutes}:{seconds:02d}"

# Function to count moves in the PGN string
def count_moves(pgn):
    move_pairs = re.findall(r'\d+\.\s([a-zA-Z0-9\+\#=\-]+)\s([a-zA-Z0-9\+\#=\-]+)', pgn)
    if move_pairs:
        return len(move_pairs)
    single_moves = re.findall(r'\d+\.\s([a-zA-Z0-9\+\#=\-]+)', pgn)
    return len(single_moves) // 2

# Function to check for castling
def detect_castling(moves, color):
    castle = "None"
    for move in moves:
        if color == "white":
            if "0-0" in move:  # White castles kingside
                castle = "Kingside"
            elif "0-0-0" in move:  # White castles queenside
                castle = "Queenside"
        elif color == "black":
            if "0-0" in move:  # Black castles kingside
                castle = "Kingside"
            elif "0-0-0" in move:  # Black castles queenside
                castle = "Queenside"
    return castle

def preprocess_games(input_file="all_chess_games.json", output_file="cleaned_games.csv", your_username="ardaylmaz"):
    with open(input_file, "r") as file:
        games = json.load(file)

    processed_data = []
    for game in games:
        if game.get("time_class", "") != "rapid":
            continue  # Skip non-rapid games

        white_elo = None
        black_elo = None
        result = "Unknown"
        color = None
        castle = "None"
        opponent_castle = "None"
        game_duration = None
        move_count = None


        # Check if you are the white player
        if game["white"]["username"].lower() == your_username.lower():
            color = "white"
            result = game["white"].get("result", "Unknown")
            white_elo = game["white"].get("rating", None)
            black_elo = game["black"].get("rating", None)
            # Check for castling in PGN (white's moves)
            pgn = game.get("pgn", "")
            if "O-O" in pgn.split()[::2]:  # Only check white's moves (odd-indexed moves in PGN)
                castle = "Kingside"
            elif "O-O-O" in pgn.split()[::2]:
                castle = "Queenside"
        # Otherwise, you're the black player
        elif game["black"]["username"].lower() == your_username.lower():
            color = "black"
            result = game["black"].get("result", "Unknown")
            white_elo = game["white"].get("rating", None)
            black_elo = game["black"].get("rating", None)
            # Check for castling in PGN (black's moves)
            pgn = game.get("pgn", "")
            if "O-O" in pgn.split()[1::2]:  # Only check black's moves (even-indexed moves in PGN)
                castle = "Kingside"
            elif "O-O-O" in pgn.split()[1::2]:
                castle = "Queenside"
        else:
            # If you're not in the game, skip it
            continue
    
            
        # Determine opponent's castling (opposite color to yours)
        opponent_color = "white" if color == "black" else "black"
        opponent_pgn = game.get("pgn", "")
        
        # Split PGN into moves for each player
        if opponent_color == "white":
            # Opponent is white, check their moves (even-indexed moves)
            if "O-O" in opponent_pgn.split()[::2]:
                opponent_castle = "Kingside"
            elif "O-O-O" in opponent_pgn.split()[::2]:
                opponent_castle = "Queenside"
        else:
            # Opponent is black, check their moves (odd-indexed moves)
            if "O-O" in opponent_pgn.split()[1::2]:
                opponent_castle = "Kingside"
            elif "O-O-O" in opponent_pgn.split()[1::2]:
                opponent_castle = "Queenside"

        pgn = game.get("pgn", "")
        if pgn:
            start_time = None
            end_time = None
            date_match = re.search(r'\[UTCDate "(\d{4}\.\d{2}\.\d{2})"\]', pgn)
            time_match = re.search(r'\[UTCTime "(\d{2}:\d{2}:\d{2})"\]', pgn)

            if date_match and time_match:
                start_time_str = date_match.group(1) + " " + time_match.group(1)
                start_time = datetime.strptime(start_time_str, "%Y.%m.%d %H:%M:%S")

            end_time_match = re.search(r'\[EndTime "(\d{2}:\d{2}:\d{2})"\]', pgn)
            if end_time_match:
                end_time_str = date_match.group(1) + " " + end_time_match.group(1)
                end_time = datetime.strptime(end_time_str, "%Y.%m.%d %H:%M:%S")

            if start_time and end_time:
                game_duration = (end_time - start_time).total_seconds() / 60

            move_count = count_moves(pgn)

            # Parse the moves and detect castling
            moves = re.findall(r'\d+\.\s([a-zA-Z0-9\+\#=\-]+)\s?([a-zA-Z0-9\+\#=\-]+)?', pgn)  # Modified regex to capture all moves

        if game_duration is not None:
            game_duration = convert_to_minutes_seconds(game_duration)


        opening_url = game.get("eco", "Unknown")
        if opening_url != "Unknown":
            opening_name = opening_url.split('/')[-1].replace('-', ' ').strip()
            if ":" in opening_name:
                opening_name = opening_name.split(":")[0]
        else:
            opening_name = "Unknown Opening"

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


        game_data = {
            "result": result,
            "color": color,
            "opening": opening_name,
            "time": time,
            "game_duration": game_duration,
            "move_count": move_count,
            "castle": castle,  # Now includes detected castling
            "opponent_castle": opponent_castle,  # Opponent's castling
            "white_elo": white_elo,
            "black_elo": black_elo
        }
        processed_data.append(game_data)

    df = pd.DataFrame(processed_data)
    df.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}.")

if __name__ == "__main__":
    preprocess_games(your_username="ardaylmaz")
