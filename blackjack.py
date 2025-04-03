import collections
import itertools
from colorama import Fore, Style

def initialize_deck(num_decks):
    """Creates a deck with the given number of decks."""
    single_deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4
    return list(itertools.chain(*[single_deck for _ in range(num_decks)]))

def calculate_probability(deck):
    """Calculates the probability of drawing an Ace and a high card separately."""
    count_aces = sum(1 for card in deck if card == "A")
    count_high_cards = sum(1 for card in deck if card in ["10", "J", "Q", "K"])
    return (count_aces / len(deck) if deck else 0, count_high_cards / len(deck) if deck else 0)

def calculate_card_count(deck_counts):
    """Implements basic Hi-Lo card counting system."""
    count = 0
    for card, count_in_deck in deck_counts.items():
        if card in ["2", "3", "4", "5", "6"]:
            count += count_in_deck
        elif card in ["10", "J", "Q", "K", "A"]:
            count -= count_in_deck
    return count

def calculate_true_count(card_count, remaining_decks):
    """Calculates the true count by normalizing for the number of remaining decks."""
    return card_count / remaining_decks if remaining_decks > 0 else card_count

def get_valid_drawn_cards(deck, deck_counts, prompt):
    """Repeatedly ask for drawn cards until a valid input is provided."""
    while True:
        drawn_cards = input(Fore.CYAN + prompt + Style.RESET_ALL)
        if drawn_cards.lower() in ["quit", "shuffle", "skip"]:
            return drawn_cards.lower()
        
        drawn_cards_list = [card.strip() for card in drawn_cards.split(",")]
        invalid_cards = [card for card in drawn_cards_list if card not in deck_counts]
        overdrawn_cards = [card for card in drawn_cards_list if deck_counts.get(card, 0) == 0]

        if invalid_cards:
            print(Fore.RED + "Invalid entry, please enter actual denominations." + Style.RESET_ALL)
        elif overdrawn_cards:
            print(Fore.YELLOW + f"Warning: All of the following cards have been drawn and are no longer available: {', '.join(overdrawn_cards)}. Please enter other values." + Style.RESET_ALL)
        else:
            return drawn_cards_list

def main():
    print(Fore.GREEN + "Welcome to the Blackjack Card Counter! I'll guide you along the way to let you know what your probabilities are of drawing an Ace or a 10 on your next hand. Let's begin!" + Style.RESET_ALL)
    print(Fore.MAGENTA + "You can type 'shuffle' at any time to reset the deck, 'quit' to exit, or 'skip' to skip your turn." + Style.RESET_ALL)

    num_decks = int(input(Fore.CYAN + "Enter the number of decks in the shoe (1, 2, 4, 6, 8): " + Style.RESET_ALL))
    if num_decks not in [1, 2, 4, 6, 8]:
        print(Fore.RED + "Invalid input. Using 6 decks by default." + Style.RESET_ALL)
        num_decks = 6

    num_players = int(input(Fore.CYAN + "Enter the number of players at the table (1-7): " + Style.RESET_ALL))
    if num_players not in range(1, 8):
        print(Fore.RED + "Invalid input. Using 1 player by default." + Style.RESET_ALL)
        num_players = 1

    print(Fore.GREEN + f"Game setup: {num_players} player(s) vs. the dealer." + Style.RESET_ALL)
    print(Fore.MAGENTA + "Let's begin! Dealing new deck. \nRemember to type 'shuffle' at any time to start over on a new deck." + Style.RESET_ALL)

    deck = initialize_deck(num_decks)
    deck_counts = collections.Counter(deck)

    while True:
        prob_ace, prob_high_card = calculate_probability(deck)
        print(Fore.BLUE + f"Probability of drawing an Ace next hand: {prob_ace * 100:.2f}%" + Style.RESET_ALL)
        print(Fore.BLUE + f"Probability of drawing a high card next hand: {prob_high_card * 100:.2f}%" + Style.RESET_ALL)

        card_count = calculate_card_count(deck_counts)
        remaining_decks = len(deck) / 52
        true_count = calculate_true_count(card_count, remaining_decks)

        print(Fore.YELLOW + f"Running count: {card_count}" + Style.RESET_ALL)
        print(Fore.CYAN + f"True count: {true_count:.2f}" + Style.RESET_ALL)

        if true_count > 2:
            print(Fore.GREEN + "Advice: The count is high! Consider increasing your bets." + Style.RESET_ALL)
        elif true_count < -1:
            print(Fore.RED + "Advice: The count is low. Consider playing conservatively." + Style.RESET_ALL)

        all_skipped = True

        for player in range(1, num_players + 1):
            drawn_cards_list = get_valid_drawn_cards(deck, deck_counts, f"Player {player}: Enter cards drawn (comma-separated, e.g., 2, Q, Q) or 'skip' to skip turn or 'quit' to exit: ")
            
            if drawn_cards_list == "quit":
                return
            elif drawn_cards_list == "shuffle":
                print(Fore.MAGENTA + "Shuffling deck and resetting probabilities..." + Style.RESET_ALL)
                deck = initialize_deck(num_decks)
                deck_counts = collections.Counter(deck)
                continue
            elif drawn_cards_list == "skip":
                continue
            else:
                all_skipped = False

            for card in drawn_cards_list:
                deck.remove(card)
                deck_counts[card] -= 1

        drawn_cards_list = get_valid_drawn_cards(deck, deck_counts, Fore.LIGHTRED_EX + "Dealer: Enter cards drawn (comma-separated, e.g., 2, Q, Q) or 'skip' to skip or 'quit' to exit: " + Style.RESET_ALL)

        if drawn_cards_list == "quit":
            return
        elif drawn_cards_list == "shuffle":
            print(Fore.MAGENTA + "Shuffling deck and resetting probabilities..." + Style.RESET_ALL)
            deck = initialize_deck(num_decks)
            deck_counts = collections.Counter(deck)
            continue
        elif drawn_cards_list == "skip":
            if all_skipped:
                print(Fore.CYAN + "All players and dealer skipped. Moving to next round." + Style.RESET_ALL)
                continue
        else:
            all_skipped = False

        for card in drawn_cards_list:
            deck.remove(card)
            deck_counts[card] -= 1

        print(Fore.CYAN + "Round completed. Starting next round." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
