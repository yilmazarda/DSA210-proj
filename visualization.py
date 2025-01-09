from analysis import load_data, analyze_win_rate_by_color, analyze_win_rate_by_time_of_day, analyze_elo_diff_vs_win_rate
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

def plot_win_rate_by_color(df):
    """Plot win rate by color (white vs black)."""
    if "color" not in df.columns or "result" not in df.columns:
        print("Data file must contain 'color' and 'result' columns.")
        return
    
    color_win_rate = df.groupby("color")["result"].apply(lambda x: (x == "win").sum() / len(x) * 100)
    
    # Plotting
    plt.figure(figsize=(8, 6))
    color_win_rate.plot(kind='bar', color=['black', 'gray'], title="Win Rate by Color")
    plt.ylabel('Win Rate (%)')
    plt.xlabel('Color')
    plt.xticks(rotation=0)
    plt.show()

def plot_win_rate_by_opening(df, top_n=10):
    """Horizontal bar plot for win rate by opening."""
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0))
    opening_counts = df["opening"].value_counts()
    valid_openings = opening_counts[opening_counts >= 10].index
    filtered_df = df[df["opening"].isin(valid_openings)]

    win_rate_by_opening = (
        filtered_df.groupby("opening")["win"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    plt.figure(figsize=(10, 8))
    sns.barplot(
        x=win_rate_by_opening.values,
        y=win_rate_by_opening.index,
        palette="viridis"
    )
    plt.title(f"Top {top_n} Openings by Win Rate (≥10 Games)")
    plt.xlabel("Win Rate (%)")
    plt.ylabel("Opening")
    plt.tight_layout()
    plt.show()




def plot_elo_diff_vs_win_rate(df):
    """Visualize the Elo difference vs win rate using a bar plot with a custom color palette."""
    # First analyze the data
    win_rate_by_elo_diff = analyze_elo_diff_vs_win_rate(df)
    
    if win_rate_by_elo_diff is None or len(win_rate_by_elo_diff) == 0:
        print("No data to visualize.")
        return
    
    # Use the 'Blues' palette to color the bars
    colors = plt.cm.Blues(np.linspace(0.3, 0.7, len(win_rate_by_elo_diff)))  # Adjust the range to avoid bright blues
    
    # Basic bar plot with the new color palette
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.bar(win_rate_by_elo_diff.index, win_rate_by_elo_diff, color=colors)
    
    # Add data labels on top of each bar
    for i, v in enumerate(win_rate_by_elo_diff):
        ax.text(i, v + 2, f'{v:.1f}%', ha='center')
    
    ax.set_title("Elo Difference vs Win Rate")
    ax.set_xlabel("Elo Rating Difference (My Rating - Opponent Rating)")
    ax.set_ylabel("Win Rate (%)")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, axis='y', alpha=0.3)
    plt.show()



def plot_win_rate_by_castling_type(df):
    """Visualize the win rate by castling type."""
    
    # Combine your castling and opponent's castling into a single column 'castling_type'
    df["castling_type"] = df.apply(
        lambda row: "Kingside" if row["castle"] == "Kingside" else ("Queenside" if row["castle"] == "Queenside" else "No Castling"), axis=1
    )
    
    # Create a new column for win rate, with wins as 1, draws as 0.5, and losses as 0
    df["win"] = df["result"].apply(lambda x: 1 if x == "win" else (0.5 if x == "agreed" else 0))

    # Calculate win rate by castling type
    win_rate_by_castling = df.groupby("castling_type")["win"].mean() * 100

    # Plot the win rate by castling type
    plt.figure(figsize=(8, 6))
    sns.barplot(x=win_rate_by_castling.index, y=win_rate_by_castling.values, palette="viridis")
    plt.title("Win Rate by Castling Type")
    plt.xlabel("Castling Type")
    plt.ylabel("Win Rate (%)")
    plt.show()


def plot_elo_rating_progression(df, start_date="2023-01-01"):
    """
    Visualizes Elo rating progression over time for your games from the specified start date onwards.
    
    Parameters:
    - df: DataFrame containing game data, including 'time', 'white_elo', 'black_elo', and 'color' columns.
    - start_date: Start date to filter the data (default is "2023-01-01").
    
    Returns:
    - A plot showing Elo rating progression over time.
    """
    # Make a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Ensure 'time' is a datetime column and filter the data for games from the start_date onwards
    df_copy['time'] = pd.to_datetime(df_copy['time'], errors='coerce')  # Convert time to datetime
    df_copy = df_copy[df_copy['time'] >= pd.to_datetime(start_date)]  # Filter games from 2023 onwards
    
    # Calculate your Elo rating based on whether you played as white or black
    df_copy['elo_rating'] = df_copy.apply(lambda row: row['white_elo'] if row['color'] == 'white' else row['black_elo'], axis=1)
    
    # Drop rows where Elo rating is missing
    df_copy = df_copy.dropna(subset=['elo_rating'])
    
    # Plot Elo rating progression over time without markers
    plt.figure(figsize=(10, 6))
    plt.plot(df_copy['time'], df_copy['elo_rating'], linestyle='-', color='b', label='Elo Rating')
    
    plt.title('Elo Rating Progression Over Time (2023 Onwards)')
    plt.xlabel('Date')
    plt.ylabel('Elo Rating')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_distribution_game_length(df):
    plt.figure(figsize=(10, 6))
    
    # Plot KDE (Kernel Density Estimate) as a line plot
    sns.kdeplot(df['move_count'], fill=False, color='blue', linewidth=2)
    
    # Set the y-axis to percentage format without decimal places
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x*100)}'))

    plt.title("Distribution of Game Length (Move Count)")
    plt.xlabel("Number of Moves")
    plt.ylabel("Percentage of Games (%)")
    plt.tight_layout()
    plt.show()



def plot_losses(df):
    """
    Analyzes the losses in the dataset and breaks them down by type: resigned, checkmated, abandoned, timeout.
    
    Parameters:
    - df: DataFrame containing game data, including 'result' and 'loss_type' columns.
    """
    # Define loss types based on your dataset's loss conditions
    # Anything other than 'win', 'agreed', 'repetition' is considered a loss
    loss_conditions = ['win', 'agreed', 'repetition', 'stalemate', 'insufficient', 'timevsinsufficient']
    
    # Add a column to categorize losses
    df['loss_type'] = df['result'].apply(lambda x: 'Loss' if x not in loss_conditions else None)
    
    # Now we'll define possible loss types and manually categorize them if present
    # Example: You may have a 'resignation', 'checkmate', 'abandoned', 'timeout' column or some other way to categorize losses
    # For now, we assume you already know how to classify these losses and manually add them
    
    # Here is an example approach if such columns exist (replace this with your actual categorization logic):
    df['loss_type'] = df.apply(lambda row: 'Resigned' if 'resign' in row['result'].lower() else row['loss_type'], axis=1)
    df['loss_type'] = df.apply(lambda row: 'Checkmated' if 'checkmated' in row['result'].lower() else row['loss_type'], axis=1)
    df['loss_type'] = df.apply(lambda row: 'Abandoned' if 'abandoned' in row['result'].lower() else row['loss_type'], axis=1)
    df['loss_type'] = df.apply(lambda row: 'Timeout' if 'timeout' in row['result'].lower() else row['loss_type'], axis=1)
    
    # Filter out the losses and categorize them
    losses_df = df[df['loss_type'].notna()]
    
    # Now we'll analyze the counts of each type of loss
    loss_counts = losses_df['loss_type'].value_counts(normalize=True) * 100
    
    # Print out the counts of each loss type
    print(f"Loss Type Percentages:\n{loss_counts}")

    # Define colors for each loss type
    colors = {
        'Resigned': 'red',
        'Checkmated': 'blue',
        'Abandoned': 'green',
        'Timeout': 'orange'
    }
    
    # Plot the loss types as a bar chart
    plt.figure(figsize=(10, 6))
    loss_counts.plot(kind='bar', color=[colors.get(loss_type, 'gray') for loss_type in loss_counts.index], alpha=0.7)
    
    plt.title("Loss Breakdown by Type")
    plt.xlabel("Loss Type")
    plt.ylabel("Loss Percentage")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_percentage_games_per_month_from_2023(df):
    """
    Plots the percentage of games played per month starting from 2023.
    """
    # Convert 'time' column to datetime if not already
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    # Filter for games starting from 2023
    df = df[df['time'] >= pd.Timestamp("2023-01-01")]
    
    # Extract year and month for grouping
    df['year_month'] = df['time'].dt.to_period('M')
    
    # Count games by month and calculate percentages
    games_per_month = df['year_month'].value_counts().sort_index()
    games_per_month_percentage = (games_per_month / games_per_month.sum()) * 100

    # Plot
    plt.figure(figsize=(10, 6))
    games_per_month_percentage.plot(kind='bar', color='skyblue')
    plt.title("Percentage of Games Played Per Month (From 2023)")
    plt.xlabel("Month")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_percentage_games_by_time_of_day(df):
    """
    Plots the percentage of games played by time of day.
    """
    # Convert 'time' column to datetime if not already
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    # Extract the hour from the datetime
    df['hour'] = df['time'].dt.hour
    
    # Count games by hour and calculate percentages
    games_by_hour = df['hour'].value_counts().sort_index()
    games_by_hour_percentage = (games_by_hour / games_by_hour.sum()) * 100

    # Plot
    plt.figure(figsize=(10, 6))
    games_by_hour_percentage.plot(kind='bar', color='orange')
    plt.title("Percentage of Games Played by Time of Day")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Percentage (%)")
    plt.xticks(range(0, 24), labels=[f'{i}:00' for i in range(24)], rotation=45)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Load the cleaned game data
    df = load_data()

    plot_percentage_games_by_time_of_day(df)
    plot_percentage_games_per_month_from_2023(df)
    
    
    plot_losses(df)
    # Perform analysis and plotting
    analyze_win_rate_by_color(df)
    plot_win_rate_by_color(df)

    plot_win_rate_by_opening(df)
    
    analyze_elo_diff_vs_win_rate(df)
    plot_elo_diff_vs_win_rate(df)
    
    analyze_win_rate_by_time_of_day(df)
    plot_win_rate_by_castling_type(df)

    plot_elo_rating_progression(df)
    plot_distribution_game_length(df)

   

    
