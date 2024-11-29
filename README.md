# DSA210-proj: Chess Match Data Analysis

## Motivation

The motivation behind this project is to analyze my chess game data from chess.com to uncover patterns and trends that could provide insights into my playing habits and performance. By examining various factors such as the time of day, game color (black or white), openings, Elo ratings, and game duration, this project aims to improve my understanding of my own gameplay and identify areas where I can enhance my performance. Additionally, understanding the impact of game factors like Elo difference and the number of moves on my win rate will provide valuable information for future games.

## Data Source

The data for this project comes from **chess.com**, where I extracted my game history through their provided API. The dataset includes various attributes of each game, such as:

- **Game outcome**: win, loss, or draw.
- **Player’s color**: black or white.
- **Elo ratings**: both my Elo rating and my opponent's.
- **Opening moves**: the chess opening used in each game.
- **Time taken for moves**: the time spent on each move.
- **Resignation or timeout details**: any instances of timeout or resignation during games.

The dataset was processed and cleaned to remove irrelevant columns, handle missing data, and ensure privacy (by removing opponent usernames).

## Data Analysis

The analysis focuses on the following areas to explore different aspects of my gameplay:

1. **Played Game Rate per Black or White**: Investigating how often I play as Black or White.
2. **Played Game Rate per Opening**: Analyzing the frequency of different chess openings used in my games.
3. **Played Game Rate per Time of the Day**: Understanding at what times of day I play the most chess.
4. **Winrate per Black or White**: Analyzing my win rate based on the color I play.
5. **Win Rate per Opening**: Comparing my win rates across various chess openings.
6. **Win Rate Considering Move Number**: Investigating how the number of moves in a game correlates with my win rate.
7. **Win Rate Considering Elo Difference**: Analyzing the effect of Elo differences between me and my opponent on win rates.
8. **Timeout, Resign, Checkmated Lose Rate**: Understanding the factors behind my losses, specifically due to timeout, resignation, or checkmate.

## Findings

The analysis aims to provide insights in several key areas, including:

- **Peak times for playing chess**: Identifying when I tend to play the most.
- **Successful openings**: Determining which chess openings have the highest win rates.
- **Elo rating differences**: Understanding how differences in Elo ratings affect my performance.
- **Loss patterns**: Investigating the common causes of losses, such as timeout, resignation, or checkmate.

The detailed analysis is presented with visualizations, such as histograms, bar charts, and line graphs, to convey the results effectively.

## Limitations and Future Work

While this analysis provides valuable insights, there are some limitations to consider:

- The data used in this project is limited to the games I’ve played on chess.com, and may not fully represent my overall performance or tendencies across other platforms.
- The analysis does not take into account external factors such as mood, distractions, or internet connection issues, which may affect performance.

In the future, I plan to expand this analysis by:

- **Collecting more data** over time to observe changes in performance.
- **Analyzing the relationship between move times** and performance to understand how time management affects my games.
- **Implementing machine learning models** to predict game outcomes based on player statistics, such as Elo ratings and opening choices.
- **Expanding the data set** by analyzing games from multiple platforms or online tournaments.
