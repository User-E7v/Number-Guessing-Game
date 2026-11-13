# Number Guessing Game

An interactive Command-Line Interface (CLI) application written in Python. This project allows players to test their logic and deduction skills across multiple difficulty levels, featuring a dynamic hint system, performance-based scoring, and persistent statistics tracking via JSON.

---

## Table of Contents

1. [Key Features](#key-features)
2. [Prerequisites and Dependencies](#prerequisites-and-dependencies)
3. [Architecture and Function Reference](#architecture-and-function-reference)
4. [Difficulty Levels and Scoring System](#difficulty-levels-and-scoring-system)
5. [Installation and Usage](#installation-and-usage)
6. [Data Persistence](#data-persistence)

---

## Key Features

* **Seven Difficulty Modes:** Offers five preset tiers ranging from Easy (1–10) to Legend (1–1000), alongside a Custom mode for user-defined parameters and a Random mode.
* **Dynamic Proximity Hints:** Calculates the absolute difference between the user's guess and the target number to provide real-time feedback on proximity and direction (higher or lower).
* **Performance-Based Scoring:** Evaluates player efficiency on a 100-point scale determined by the ratio of attempts used to maximum attempts allowed.
* **Win Streak Tracking:** Monitors consecutive victories during a session and assigns progressive rank titles.
* **Automated Statistics Logging:** Records match outcomes, timestamps, attempt counts, and scores in a local `game_stats.json` file.
* **Clean Terminal Interface:** Utilizes screen-clearing utilities and structured text separators to maintain readability throughout gameplay.

---

## Prerequisites and Dependencies

This application is built entirely using the Python Standard Library and requires no third-party package installations:

* `random`: Generates secret target numbers and selects random difficulty levels and motivational quotes.
* `os`: Executes system-level commands to clear the terminal screen (`cls` for Windows, `clear` for Unix-based systems).
* `time`: Measures round duration and manages brief interface pauses.
* `json`: Handles serialization and deserialization of player statistics.
* `datetime`: Captures ISO-formatted timestamps for each completed game.

---

## Architecture and Function Reference

### 1. User Interface Utilities
* `clear_screen()`: Clears the console output to maintain a clean display state across menus and rounds.
* `print_header()`: Renders the standardized application title banner.
* `print_separator(char, length)`: Outputs horizontal dividers to structure console output.
* `print_loading_animation()`: Displays a brief progress indicator using sequential periods.

### 2. Core Game Logic and Evaluation
* `get_difficulty()`: Prompts the user to select a difficulty mode (1–7) and returns the upper bound (`max_num`), attempt limit (`max_attempts`), and mode name.
* `get_hint(secret, guess, attempts_left, max_num)`: Evaluates $| \text{secret} - \text{guess} |$ and returns a proximity status string.
* `get_emoji_feedback(guess, secret)`: Returns directional indicators (`[^]` for too low, `[v]` for too high).
* `get_score_based_on_attempts(attempts_used, max_attempts)`: Computes the final numeric score and performance grade based on attempt efficiency.
* `get_streak_message(streak)`: Maps the current consecutive win count to a corresponding rank title.
* `get_motivational_quote()`: Selects and returns a random encouragement message at the end of a session.

### 3. Application Flow and Data Management
* `play_game()`: Executes the primary gameplay loop, validates numeric inputs, tracks elapsed time, and determines win/loss conditions.
* `save_stats(stats)`: Appends session results to `game_stats.json` and updates cumulative totals for games played, wins, and losses.
* `view_stats()`: Reads `game_stats.json` to calculate the overall win rate and display a summary of the 10 most recent matches.
* `main_menu()` & `main()`: Manages top-level navigation (Play, Statistics, Instructions, Settings, Exit) and handles exceptions such as `KeyboardInterrupt`.

---

## Difficulty Levels and Scoring System

### Difficulty Tiers

| Option | Level Name | Number Range | Maximum Attempts |
| :--- | :--- | :--- | :--- |
| **1** | Easy | $1 - 10$ | 5 |
| **2** | Medium | $1 - 50$ | 7 |
| **3** | Hard | $1 - 100$ | 10 |
| **4** | Expert | $1 - 500$ | 15 |
| **5** | Legend | $1 - 1000$ | 20 |
| **6** | Custom | User-defined (Capped at $1,000,000$) | User-defined |
| **7** | Random | Randomly selected from options 1–5 | Corresponding to selected tier |

### Scoring Rubric

Scores are calculated using the attempt efficiency ratio ($\text{Ratio} = \frac{\text{Attempts Used}}{\text{Max Attempts}}$):

* **100 Points (`PERFECT SCORE!`):** Solved within $\le 20\%$ of maximum attempts.
* **80 Points (`Excellent!`):** Solved within $\le 40\%$ of maximum attempts.
* **60 Points (`Good job!`):** Solved within $\le 60\%$ of maximum attempts.
* **40 Points (`Not bad!`):** Solved within $\le 80\%$ of maximum attempts.
* **20 Points (`You barely made it!`):** Solved using $> 80\%$ of maximum attempts.

---

## Installation and Usage

1. Ensure **Python 3.x** is installed on your system.
2. Save the source code to a local file named `guessing_game.py`.
3. Open a terminal or command prompt and navigate to the directory containing the file.
4. Execute the script using the following command:

   ```bash
   python guessing_game.py
   ```

5. Follow the on-screen numeric prompts to navigate the menu and play the game.

---

## Data Persistence

Upon completing a game, the application automatically creates or updates `game_stats.json` in the root directory. The data is structured as follows:

```json
{
    "games": [
        {
            "timestamp": "2026-11-13T16:30:00.000000",
            "won": true,
            "difficulty": "Hard",
            "attempts": 4,
            "score": 80,
            "streak": 1
        }
    ],
    "total_games": 1,
    "total_wins": 1,
    "total_losses": 0
}
```