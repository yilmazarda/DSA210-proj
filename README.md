# DSA210-proj

# Chess Match Data Analysis

## Project Overview

This project involves analyzing chess game data from chess.com to explore various patterns and statistics related to my gameplay. Using Python, Jupyter Notebook, Matplotlib, and Pandas, this analysis aims to provide insights into game rates, win rates, and the factors that influence my chess performance.

## Objective

The main goal of this project is to analyze various aspects of my chess games to understand patterns in:

- Played game rate per color (Black or White)
- Played game rate per opening
- Played game rate per time of the day
- Win rate per color (Black or White)
- Win rate per opening
- Win rate considering the number of moves
- Win rate considering Elo difference
- Loss rate due to timeout, resignation, or checkmate

## Tools and Libraries

This project makes use of the following Python libraries and tools:

- **Python**: The programming language used to analyze the data.
- **Jupyter Notebook**: The environment used for writing and running the analysis.
- **Matplotlib**: Used for visualizing the data with static plots.
- **Pandas**: Used for data processing, manipulation, and analysis.
- **NumPy**: Used for numerical operations and calculations.

## Data Source

The data for this project comes from **chess.com**, where I extracted my game history through their provided API. The data contains various attributes of each game, including:

- Game outcome (win, loss, draw)
- Player's color (black or white)
- Elo ratings (both player and opponent)
- Opening moves
- Time taken for moves
- Resignation or timeout details

## Data Processing

The data will be preprocessed to ensure that:

- Irrelevant columns have been removed.
- Data has been cleaned and structured in a way that makes it easy to analyze.
- Missing or inconsistent data has been handled appropriately.
- Opponent usernames are removed to ensure privacy and confidentiality.

## Data Analysis

The analysis will focus on the following key areas:

1. **Played Game Rate per Black or White**: Investigating how often games are played as Black or White.
2. **Played Game Rate per Opening**: Analyzing the frequency of different chess openings used.
3. **Played Game Rate per Time of the Day**: Understanding the times of day when I tend to play chess.
4. **Winrate per Black or White**: Analyzing the win rate based on the color played.
5. **Win Rate per Opening**: Comparing win rates for different chess openings.
6. **Win Rate Considering Move Number**: Analyzing how the number of moves influences the win rate.
7. **Win Rate Considering Elo Difference**: Investigating how Elo differences affect win rates.
8. **Timeout, Resign, Checkmated Lose Rate**: Understanding the causes of losses in my games (timeout, resignation, or checkmate).


## Visualizations

Various visualizations will be created to present the findings, including:

- **Histograms**: For visualizing distributions such as game rates per time of day, Elo difference, and game outcomes.
- **Line Charts**: To track changes over time or the relationship between different factors.
- **Density Plots**: To show the distribution of Elo ratings for both players.
- **Bar Charts**: For comparing win rates across different openings, move numbers, and more.


## Results

Key findings from the analysis will be summarized here once the project is complete. These may include:

- **Peak times** for playing chess.
- The **most successful openings** based on win rate.
- **Patterns in Elo rating differences** and their influence on my performance.
- Insights into **resignation and timeout** behavior.

## Future Work

In the future, I plan to expand this analysis by:

- Collecting more data over time to track changes in performance.
- Analyzing the relationship between move times and performance.
- Exploring more advanced machine learning models to predict game outcomes based on player statistics.
