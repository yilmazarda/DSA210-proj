from analysis import load_data, analyze_win_rate_by_color, analyze_win_rate_by_time_of_day, analyze_elo_diff_vs_win_rate
import matplotlib.pyplot as plt
import seaborn as sns

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
    
def plot_elo_diff_vs_win_rate(df):
    """Visualize the Elo difference vs win rate using a bar plot."""
    # First analyze the data
    win_rate_by_elo_diff = analyze_elo_diff_vs_win_rate(df)
    
    if win_rate_by_elo_diff is None or len(win_rate_by_elo_diff) == 0:
        print("No data to visualize.")
        return
    
    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Basic bar plot
    win_rate_by_elo_diff.plot(
        kind='bar',
        color='skyblue',
        ax=ax
    )
    
    # Add data labels on top of each bar
    for i, v in enumerate(win_rate_by_elo_diff):
        ax.text(i, v + 2, f'{v:.1f}%', ha='center')
    
    ax.set_title("Elo Difference vs Win Rate")
    ax.set_xlabel("Elo Rating Difference (My Elo - Opponent Elo)")
    ax.set_ylabel("Win Rate (%)")
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, axis='y', alpha=0.3)
    plt.show()

if __name__ == "__main__":
    # Load the cleaned game data
    df = load_data()

    # Perform analysis and plotting
    analyze_win_rate_by_color(df)
    plot_win_rate_by_color(df)
    
    analyze_elo_diff_vs_win_rate(df)
    plot_elo_diff_vs_win_rate(df)
    
    analyze_win_rate_by_time_of_day(df)
