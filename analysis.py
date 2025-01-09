import pandas as pd
from scipy.stats import ttest_ind
from scipy import stats
from scipy.stats import f_oneway

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

def analyze_opening_impact_on_win_rate(df):
    """
    Analyze if opening choice has a significant impact on win rate using ANOVA, excluding openings played less than 10 times.
    """
    if "opening" not in df.columns or "result" not in df.columns:
        print("Data must contain 'opening' and 'result' columns.")
        return

    # Create a win column where wins = 1, draws = 0.5, losses = 0
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0))
    
    # Count the number of games per opening
    opening_counts = df["opening"].value_counts()

    # Filter out openings played less than 10 times
    valid_openings = opening_counts[opening_counts >= 10].index
    filtered_df = df[df["opening"].isin(valid_openings)]

    # Check if there are enough openings left for analysis
    if filtered_df["opening"].nunique() < 2:
        print("Not enough data to perform analysis after filtering.")
        return

    # Group win rates by opening
    openings = filtered_df["opening"].unique()
    win_rates_by_opening = [filtered_df[filtered_df["opening"] == opening]["win"] for opening in openings]
    
    # Perform ANOVA test
    f_stat, p_value = f_oneway(*win_rates_by_opening)

    print(f"F-statistic: {f_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("The difference in win rate between openings is statistically significant.")
    else:
        print("The difference in win rate between openings is not statistically significant.")


def analyze_color_impact_on_win_rate(df):
    """
    Perform a t-test to determine if color (white or black) has a significant impact on win rate,
    with draws counted as 0.5.
    """
    if "color" not in df.columns or "result" not in df.columns:
        print("Data must contain 'color' and 'result' columns.")
        return

    # Create a new column for win rate, with wins as 1, draws as 0.5, and losses as 0
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0))

    # Separate win rates by color
    white_wins = df[df["color"] == "white"]["win"]
    black_wins = df[df["color"] == "black"]["win"]

    # Perform a two-sample t-test
    t_stat, p_value = ttest_ind(white_wins, black_wins, equal_var=False)

    print(f"T-statistic: {t_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("The difference in win rate between white and black is statistically significant.")
    else:
        print("The difference in win rate between white and black is not statistically significant.")


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
        print("There is a statistically significant difference in win rates depending on the time of the day.")
    else:
        print("There is no statistically significant difference in win rates depending on the time of the day.")


def analyze_elo_diff_vs_win_rate(df):
    """Analyze Elo difference vs win rate and calculate p-value."""
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
    bins = [-float('inf'), -100, 0, 100, float('inf')]
    labels = ["< -100", "-100 to 0", "0 to 100", "> 100"]
    
    df["elo_diff_bins"] = pd.cut(df["elo_diff"], bins=bins, labels=labels, right=False)
    
    # Group by Elo difference bins
    grouped = df.groupby("elo_diff_bins")["win_rate"]
    win_rate_by_elo_diff = grouped.mean() * 100
    
    # Prepare data for ANOVA test
    groups = [df[df["elo_diff_bins"] == bin]["win_rate"].dropna() for bin in labels]
    
    # Perform one-way ANOVA
    f_stat, p_value = f_oneway(*groups)
    
    print(f"F-statistic: {f_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("There is a statistically significant effect of Elo difference on win rate.")
    else:
        print("There is no statistically significant effect of Elo difference on win rate.")
    
    return win_rate_by_elo_diff

def analyze_castling_impact_on_win_rate(df):
    """Analyze win rate based on castling (kingside, queenside, or no castling)."""
    if "moves" not in df.columns or "result" not in df.columns:
        print("Data must contain 'moves' and 'result' columns.")
        return

    # Create a new column for castling category
    def categorize_castling(moves):
        if "O-O" in moves:
            return "Kingside Castled"
        elif "O-O-O" in moves:
            return "Queenside Castled"
        else:
            return "Not Castled"
    
    # Apply categorization based on moves
    df["castling"] = df["moves"].apply(categorize_castling)

    # Create a new column for win rate, with wins as 1, draws as 0.5, and losses as 0
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0)) 

    # Group win rates by castling category
    kingside = df[df["castling"] == "Kingside Castled"]["win"]
    queenside = df[df["castling"] == "Queenside Castled"]["win"]
    not_castled = df[df["castling"] == "Not Castled"]["win"]

    # Perform ANOVA test
    f_stat, p_value = f_oneway(kingside, queenside, not_castled)

    print(f"F-statistic: {f_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("The difference in win rate between castling categories is statistically significant.")
    else:
        print("The difference in win rate between castling categories is not statistically significant.")


def analyze_castling_effect(df):
    """Analyze the effect of castling on win rate using a t-test."""
    
    # Filter data into two groups: castling (kingside or queenside) vs. no castling
    castling_games = df[df["castle"].isin(["Kingside", "Queenside"])]  # Games where castling occurred
    no_castling_games = df[df["castle"] == "None"]  # Games where no castling occurred

    # Calculate win rates for each group (win = 1, draw = 0.5, loss = 0)
    castling_win_rate = castling_games["win"].mean()
    no_castling_win_rate = no_castling_games["win"].mean()

    # Perform an independent t-test to compare the win rates
    t_stat, p_value = stats.ttest_ind(castling_games["win"], no_castling_games["win"], equal_var=False)

        # Determine if the result is significant
    if p_value < 0.05:
        print("Castling has a significant effect on win rate (p < 0.05).")
    else:
        print("No significant effect of castling on win rate (p >= 0.05).")

    print(f"Win rate with castling: {castling_win_rate * 100:.2f}%")
    print(f"Win rate without castling: {no_castling_win_rate * 100:.2f}%")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")


if __name__ == "__main__":
    df = load_data()

    # Perform analysis
    analyze_win_rate_by_color(df)
    analyze_color_impact_on_win_rate(df)
    analyze_opening_impact_on_win_rate(df)
    analyze_win_rate_by_time_of_day(df)
    analyze_elo_diff_vs_win_rate(df)
    analyze_castling_effect(df)
