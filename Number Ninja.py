import random
import os
import time
import json
import math
from datetime import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 70)
    print("  [*]  N U M B E R   G U E S S I N G   G A M E  [*]  ")
    print("=" * 70)

def print_separator(char="=", length=70):
    print(char * length)

def get_difficulty():
    print("\n  SELECT DIFFICULTY LEVEL:")
    print("  " + "-" * 40)
    print("  [1] Easy     (1-10)    5 attempts")
    print("  [2] Medium   (1-50)    7 attempts")
    print("  [3] Hard     (1-100)   10 attempts")
    print("  [4] Expert   (1-500)   15 attempts")
    print("  [5] Legend   (1-1000)  20 attempts")
    print("  [6] Custom   (Set your own)")
    print("  [7] Random   (Surprise me!)")
    print("  " + "-" * 40)
    
    while True:
        try:
            choice = int(input("  Enter your choice (1-7): "))
            if choice == 1:
                return 10, 5, "Easy"
            elif choice == 2:
                return 50, 7, "Medium"
            elif choice == 3:
                return 100, 10, "Hard"
            elif choice == 4:
                return 500, 15, "Expert"
            elif choice == 5:
                return 1000, 20, "Legend"
            elif choice == 6:
                max_num = int(input("  Enter maximum number: "))
                attempts = int(input("  Enter number of attempts: "))
                return max_num, attempts, "Custom"
            elif choice == 7:
                levels = [(10,5,"Easy"), (50,7,"Medium"), (100,10,"Hard"), (500,15,"Expert"), (1000,20,"Legend")]
                return random.choice(levels)
            else:
                print("  Invalid choice. Please enter 1-7.")
        except ValueError:
            print("  Please enter a valid number.")

def get_hint(secret, guess, attempts_left, max_num):
    diff = abs(secret - guess)
    
    if diff == 0:
        return "[*] PERFECT!"
    elif diff <= 2:
        return "(!!!) Very close!"
    elif diff <= 5:
        return (f"(!) Close!")
    elif diff <= 10:
        return "(+) Getting closer"
    elif diff <= 20:
        return "(-) Not too close"
    elif diff <= 50:
        return "(.) Cold"
    else:
        return "(..) Freezing cold!"

def get_emoji_feedback(guess, secret):
    if guess < secret:
        return "[^] Too low!"
    else:
        return "[v] Too high!"

def get_streak_message(streak):
    if streak == 0:
        return "Better luck next time!"
    elif streak <= 2:
        return "Good start!"
    elif streak <= 5:
        return "You're getting better!"
    elif streak <= 10:
        return "Amazing streak!"
    elif streak <= 20:
        return "Legendary!"
    else:
        return "GODLIKE!"

def get_score_based_on_attempts(attempts_used, max_attempts):
    ratio = attempts_used / max_attempts
    if ratio <= 0.2:
        return 100, "PERFECT SCORE!"
    elif ratio <= 0.4:
        return 80, "Excellent!"
    elif ratio <= 0.6:
        return 60, "Good job!"
    elif ratio <= 0.8:
        return 40, "Not bad!"
    else:
        return 20, "You barely made it!"

def play_game():
    clear_screen()
    print_header()
    
    max_num, max_attempts, difficulty = get_difficulty()
    
    if max_num > 1000000:
        print("\n  Number too large! Setting to 1000000")
        max_num = 1000000
    
    secret = random.randint(1, max_num)
    attempts = 0
    attempts_left = max_attempts
    guesses = []
    start_time = time.time()
    score = 0
    streak = 0
    
    clear_screen()
    print_header()
    print(f"\n  [*] DIFFICULTY: {difficulty.upper()}")
    print(f"  [#] RANGE: 1 to {max_num:,}")
    print(f"  [!] ATTEMPTS: {max_attempts}")
    print_separator("-", 70)
    
    while attempts_left > 0:
        print(f"\n  [-] ATTEMPTS LEFT: {attempts_left}")
        print(f"  [%] GUESSES SO FAR: {len(guesses)}")
        if guesses:
            print(f"  [>] YOUR GUESSES: {', '.join(map(str, guesses))}")
        print("  " + "-" * 40)
        
        try:
            guess = int(input(f"  Enter your guess (1-{max_num}): "))
            
            if guess < 1 or guess > max_num:
                print(f"  [!] Please enter a number between 1 and {max_num}")
                continue
            
            attempts += 1
            attempts_left -= 1
            guesses.append(guess)
            
            if guess == secret:
                elapsed = time.time() - start_time
                score, grade = get_score_based_on_attempts(attempts, max_attempts)
                streak += 1
                
                clear_screen()
                print_header()
                print(f"\n  " + "*" * 20)
                print(f"  [*] CORRECT! You guessed the number in {attempts} tries!")
                print(f"  [#] The number was: {secret}")
                print(f"  [T] Time: {elapsed:.2f} seconds")
                print(f"  [$] Score: {score}/100 - {grade}")
                print(f"  [+] Current Streak: {streak}")
                print(f"  [^] Best Streak: {get_streak_message(streak)}")
                print(f"  " + "*" * 20 + "\n")
                
                return score, streak, True, difficulty, attempts
            
            else:
                hint = get_hint(secret, guess, attempts_left, max_num)
                direction = get_emoji_feedback(guess, secret)
                print(f"  {direction} {hint}")
                
                if attempts_left > 0:
                    if guess < secret:
                        print(f"  [?] Hint: The number is higher than {guess}")
                    else:
                        print(f"  [?] Hint: The number is lower than {guess}")
                    
                    if attempts_left <= 3:
                        print(f"  [!] WARNING: Only {attempts_left} attempts left!")
                
                print("  " + "-" * 40)
                
        except ValueError:
            print("  [!] Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n  Game interrupted. Returning to menu...")
            return 0, 0, False, difficulty, 0
    
    clear_screen()
    print_header()
    print(f"\n  [-] GAME OVER!")
    print(f"  [#] The number was: {secret}")
    print(f"  [%] You used {attempts} attempts")
    print(f"  [!] Better luck next time!\n")
    
    return 0, 0, False, difficulty, attempts

def save_stats(stats):
    filename = "game_stats.json"
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except:
        data = {"games": [], "total_games": 0, "total_wins": 0, "total_losses": 0}
    
    data["games"].append(stats)
    data["total_games"] += 1
    if stats["won"]:
        data["total_wins"] += 1
    else:
        data["total_losses"] += 1
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def view_stats():
    try:
        with open("game_stats.json", 'r') as f:
            data = json.load(f)
        
        clear_screen()
        print_header()
        print("\n  [%] GAME STATISTICS")
        print_separator("-", 70)
        
        total = data["total_games"]
        wins = data["total_wins"]
        losses = data["total_losses"]
        
        if total > 0:
            win_rate = (wins / total) * 100
            print(f"\n  [#] TOTAL GAMES: {total}")
            print(f"  [+] WINS: {wins}")
            print(f"  [-] LOSSES: {losses}")
            print(f"  [^] WIN RATE: {win_rate:.1f}%")
            print_separator("-", 70)
            
            print("\n  [=] RECENT GAMES:")
            recent = data["games"][-10:]
            for i, game in enumerate(recent, 1):
                status = "[+] WIN" if game["won"] else "[-] LOSS"
                print(f"  {i}. {status} | Difficulty: {game['difficulty']} | Attempts: {game['attempts']} | Score: {game['score']}")
        else:
            print("\n  No games played yet.")
        
        print_separator("-", 70)
        input("\n  Press Enter to continue...")
        
    except FileNotFoundError:
        print("\n  No statistics available yet. Play some games first!")

def get_motivational_quote():
    quotes = [
        "The only way to win is to keep guessing!",
        "Every wrong guess brings you closer to the right one.",
        "Patience is the key to success.",
        "Think carefully, but don't overthink!",
        "Sometimes the answer is simpler than it seems.",
        "Trust your instincts!",
        "Success is not final, failure is not fatal.",
        "Believe in yourself and your guesses!",
        "The journey of a thousand guesses begins with one.",
        "You are closer than you think!"
    ]
    return random.choice(quotes)

def print_loading_animation():
    print("\n  Loading", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(" Done! [+]")

def main_menu():
    while True:
        clear_screen()
        print_header()
        print("\n  [#] MAIN MENU")
        print_separator("-", 70)
        print("  [1] Play Game")
        print("  [2] View Statistics")
        print("  [3] How to Play")
        print("  [4] Settings")
        print("  [5] Exit Game")
        print_separator("-", 70)
        
        choice = input("\n  Enter your choice (1-5): ")
        
        if choice == '1':
            score, streak, won, difficulty, attempts = play_game()
            
            if won or attempts > 0:
                stats = {
                    "timestamp": datetime.now().isoformat(),
                    "won": won,
                    "difficulty": difficulty,
                    "attempts": attempts,
                    "score": score,
                    "streak": streak
                }
                save_stats(stats)
            
            print("\n  " + get_motivational_quote())
            input("\n  Press Enter to continue...")
            
        elif choice == '2':
            view_stats()
            
        elif choice == '3':
            clear_screen()
            print_header()
            print("\n  [?] HOW TO PLAY")
            print_separator("-", 70)
            print("""
  [*] OBJECTIVE:
  Guess the secret number correctly!

  [-] HOW TO PLAY:
  1. Choose a difficulty level
  2. Enter your guess
  3. Get feedback (too high/low)
  4. Use hints to improve
  5. Guess correctly to win!

  [!] TIPS:
  * Start with middle numbers
  * Use the hints wisely
  * Pay attention to feedback
  * Don't rush - think logically
  * Learn from your mistakes

  [$] SCORING:
  * 100 points: Guessed in first 20% of attempts
  * 80 points: Guessed in first 40% of attempts
  * 60 points: Guessed in first 60% of attempts
  * 40 points: Guessed in first 80% of attempts
  * 20 points: Guessed with last few attempts
            """)
            print_separator("-", 70)
            input("\n  Press Enter to continue...")
            
        elif choice == '4':
            clear_screen()
            print_header()
            print("\n  [*] SETTINGS")
            print_separator("-", 70)
            print("""
  [-] AVAILABLE SETTINGS:
  
  * Difficulty Levels: Easy, Medium, Hard, Expert, Legend, Custom, Random
  * Attempts: Varies by difficulty
  * Number Range: Varies by difficulty
  * Hints: Enabled
  * Statistics: Auto-save
  * Score System: Enabled
  
  [!] PRO TIP:
  Custom mode allows you to set your own
  number range and attempts!
            """)
            print_separator("-", 70)
            input("\n  Press Enter to continue...")
            
        elif choice == '5':
            clear_screen()
            print_header()
            print("\n  [+] THANK YOU FOR PLAYING!")
            print("  [-] See you next time!")
            print_separator("=", 70)
            print("\n  " + get_motivational_quote())
            print("\n")
            break
            
        else:
            print("  [!] Invalid choice. Please enter 1-5.")
            time.sleep(1)

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n  [-] Game interrupted. Goodbye!")
    except Exception as e:
        print(f"\n  [!] An error occurred: {e}")
        print("  Please restart the game.")

if __name__ == "__main__":
    main()