import random
import time
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

# Constants
WORD_CATEGORIES_FILE = 'word_categories.json'
LEADERBOARD_FILE = 'leaderboard.json'
CORRECT_MESSAGE = Fore.GREEN + 'Correct!' + Style.RESET_ALL
INCORRECT_MESSAGE = Fore.RED + 'Incorrect!' + Style.RESET_ALL

# Take words from JSON File
def load_words_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Update the leaderboard
def update_leaderboard(username, words_per_minute, category):
    leaderboard = load_words_from_json(LEADERBOARD_FILE)
    leaderboard_entry = {"username": username, "wpm": words_per_minute, "category": category}
    
    if "leaderboard" not in leaderboard:
        leaderboard["leaderboard"] = []

    leaderboard["leaderboard"].append(leaderboard_entry)
    leaderboard["leaderboard"].sort(key=lambda x: x["wpm"], reverse=True)
    
    with open(LEADERBOARD_FILE, 'w') as file:
        json.dump(leaderboard, file, indent=2)

# Display the leaderboard
def show_leaderboard():
    leaderboard = load_words_from_json(LEADERBOARD_FILE).get("leaderboard", [])
    print("--- Leaderboard ---")
    for idx, entry in enumerate(leaderboard, start=1):
        print(f"{idx}. {entry['username']} - {entry['wpm']} WPM (Category: {entry['category']})")

    clear = lambda: os.system('cls')
    clear()

# Run the test
def run_typing_test(player_name, chosen_category, num_words):
    words_data = load_words_from_json(WORD_CATEGORIES_FILE)[chosen_category]
    random.shuffle(words_data)
    selected_words = words_data[:num_words]
    start_time = time.time()
    correct_words_count = 0
    clear = lambda: os.system('cls')
    clear()
    print(f"Welcome, {player_name}!\nPress 'Ctrl + Q' to quit at any time.")
    input("Press any key to start...")
    clear = lambda: os.system('cls')
    clear()
    print('Words to type: ')
    print(*selected_words, sep='  ')
    print('\n')
    for word in selected_words:
        user_input = input(f"Type: {word} ")
        if user_input == word:
            print(CORRECT_MESSAGE)
            correct_words_count += 1
        elif user_input == "Ctrl + Q":
            break
        else:
            print(INCORRECT_MESSAGE)

    end_time = time.time()
    elapsed_time = end_time - start_time
    words_per_minute = (correct_words_count / elapsed_time) * 60

    print(f"\nTyping Metrics for {player_name}: ")
    print(f"Words Typed: {correct_words_count}")
    print(f"Time Taken: {elapsed_time:.2f} seconds")
    print(f"Words Per Minute: {words_per_minute:.2f}")
    input('Press any key to continue...')
    clear = lambda: os.system('cls')
    clear()

    update_leaderboard(player_name, words_per_minute, chosen_category)

# Main function
def main():
    print("Welcome to Terminal Typing Master!")
    input('Press any key to continue...')
    clear = lambda: os.system('cls')
    clear()
    player_name = input("Enter your username: ")
    clear()

    while True:
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("Choose a category:")
            categories = load_words_from_json(WORD_CATEGORIES_FILE).keys()
            for idx, category in enumerate(categories, start=1):
                print(f"{idx}. {category}")
            
            category_choice = input("Enter the number for your chosen category: ")
            category_choice = int(category_choice) - 1
            if category_choice < 0 or category_choice >= len(categories):
                print("Invalid category choice.")
                continue
            num_words = int(input("Enter the number of words to practice (1-200): "))
            if num_words < 1 or num_words > 200:
                print("Invalid number of words.")
                continue
            run_typing_test(player_name, list(categories)[category_choice], num_words)
        elif choice == '2':
            show_leaderboard()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
