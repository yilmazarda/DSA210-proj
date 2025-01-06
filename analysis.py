import pandas as pd
from scipy.stats import ttest_ind

def load_data(file_path="cleaned_games.csv"):
    """Load the cleaned game data."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def analyze_win_rate_by_color(df):
    """Analyze win rate by color (white vs black)."""
    if "color" not in df.columns or "result" not in df.columns:
        print("Data file must contain 'color' and 'result' columns.")
        return
    
    color_win_rate = df.groupby("color")["result"].apply(lambda x: (x == "win").sum() / len(x) * 100)
    print("Win Rate by Color:")
    print(color_win_rate)


def analyze_win_rate_by_time_of_day(df):
    """Analyze win rate by time of day."""
    df["time"] = pd.to_datetime(df["time"], errors='coerce')
    df = df.dropna(subset=["time"])
    df["hour"] = df["time"].dt.hour
    df["time_of_day"] = pd.cut(df["hour"], bins=[0, 9, 17, 21, 24], labels=["Morning", "Afternoon", "Evening", "Night"])
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else 0)

    win_rate_by_time_of_day = df.groupby("time_of_day")["win"].mean() * 100
    print("Win Rate by Time of Day:")
    print(win_rate_by_time_of_day)

    morning_afternoon = df[df["hour"] <= 17]["win"]
    evening_night = df[df["hour"] > 17]["win"]
    t_stat, p_value = ttest_ind(morning_afternoon, evening_night)
    
    print(f"T-statistic: {t_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("There is a statistically significant difference in win rates.")
    else:
        print("There is no statistically significant difference in win rates.")

def analyze_elo_diff_vs_win_rate(df):
    """Analyze Elo difference vs win rate with simplified binned categories."""
    if "result" not in df.columns or "white_elo" not in df.columns or "black_elo" not in df.columns:
        print("Data file must contain 'result', 'white_elo', and 'black_elo' columns.")
        return None
    
    # Calculate Elo difference
    df["elo_diff"] = df.apply(
        lambda row: row["white_elo"] - row["black_elo"] if row["color"] == "white" else row["black_elo"] - row["white_elo"], axis=1
    )
    
    # Calculate win rate: 1 for win, 0 for loss, 0.5 for draw
    df["win_rate"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0))
    
    # Bin the Elo difference into categories
    bins = [-float('inf'), -500, 0, 100, 200, float('inf')]
    labels = ["< -500", "-500 to 0", "0 to 100", "100 to 200", "200+"]
    
    df["elo_diff_bins"] = pd.cut(df["elo_diff"], bins=bins, labels=labels, right=False)
    
    # Group by Elo difference bins and calculate average win rate in each bin
    return df.groupby("elo_diff_bins")["win_rate"].mean() * 100

if __name__ == "__main__":
    df = load_data()

    # Perform analysis
    analyze_win_rate_by_color(df)
    analyze_win_rate_by_time_of_day(df)
    analyze_elo_diff_vs_win_rate(df)
