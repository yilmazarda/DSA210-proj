# DSA210-proj: Chess Match Data Analysis

[Web site for the project.](https://yilmazarda.github.io/DSA210-proj/)

## Motivation

The motivation behind this project is to analyze my chess game data from chess.com to uncover patterns and trends that could provide insights into my playing habits and performance. By examining various factors such as the time of day, game color (black or white), openings, Elo ratings, and game duration, this project aims to improve my understanding of my own gameplay and identify areas where I can enhance my performance. Additionally, understanding the impact of game factors like Elo difference and the number of moves on my win rate will provide valuable information for future games.

## Data Source

The data for this project comes from **chess.com**, where I extracted my game history through their provided API. The dataset includes various attributes of each game, such as:

- **Game outcome**: win, loss, or draw.
- **Player’s color**: black or white.
- **Elo ratings**: both my Elo rating and my opponent's.
- **Moves**: the chess moves used in each game.
- **Resignation or timeout details**: any instances of timeout or resignation during games.

The dataset was processed and cleaned to remove irrelevant columns, handle missing data, and ensure privacy (by removing opponent usernames).

## Hypothesis

My hypothesis: My win rate changes according to the time of day.

## Findings

[Visit web site for findings.](https://yilmazarda.github.io/DSA210-proj/)

## Limitations and Future Work

While this analysis provides valuable insights, there are some limitations to consider:

- The data used in this project is limited to the games I’ve played on chess.com, and may not fully represent my overall performance or tendencies across other platforms.
- The analysis does not take into account external factors such as mood, distractions, or internet connection issues, which may affect performance.

In the future, I plan to expand this analysis by:

- **Collecting more data** over time to observe changes in performance.
- **Analyzing the relationship between move times** and performance to understand how time management affects my games.
- **Implementing machine learning models** to predict game outcomes based on player statistics, such as Elo ratings and opening choices.
- **Expanding the data set** by analyzing games from multiple platforms or online tournaments.
