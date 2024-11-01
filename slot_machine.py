import random
import os
from time import sleep

INITIAL_BALANCE = 100
BET = 1
TITLE = "Slot-Machine!"
SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "🍑", "💎"]
VALUES = [i for i, _ in enumerate(SYMBOLS[:-1], start=1)] + [10] #[1, 2, 3, 4, 5, 6, 7, 10]
SYMBOL_VALUES = dict(zip(SYMBOLS, VALUES))
REELS = 3

def console_clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def spin_slot_machine():
    """Spin n reels and select n symbols at random with a likelihood
    anti-proportional to their value.
    """
    weights = [max(VALUES) - i for i in range(len(SYMBOLS) -1)] + [1]
    return random.choices(SYMBOLS, weights=weights, k=REELS)

def is_win(results):
    """Check whether all symbols are the same.
    Return winning symbol or None
    """
    return results[0] if len(set(results)) == 1 else None
    
def calc_payoff(bet, symbol):
    """Return payoff as product of reels, symbol value and bet """
    return bet * SYMBOL_VALUES[symbol] * REELS

def spin_animation(results):
    """ This is just an animation leading to showing the results.
    Quick sequence of random symbols stopping one by one at the result
    """
    for i in range(REELS):
        set_symbols = results[:i]
        for j in range(10):
            symbols = set_symbols + [random.choice(SYMBOLS) for _ in range(REELS - len(set_symbols))]
            console_clear()

            print(TITLE)
            print(16 * "-")
            print(f"| {' | '.join(symbols)} |")
            print(16 * "-")
            print()

            sleep(.1)

def win_animation(symbol):
    """ three rows with winning symbols jumping up and down
    """
    a = [symbol if i % 2 == 0 else '  ' for i in range(REELS) ]
    b = [symbol if i % 2 == 1 else '  ' for i in range(REELS) ]
    for _ in range(10):
        console_clear()
        print(TITLE)
        print(f"| {' | '.join(a)} |")
        print(f"| {' | '.join(b)} |")
        print(f"| {' | '.join(a)} |")
        print()
        a, b = b, a
        sleep(.1)

def display(results):
    """clear console, print title and current symbols
    """
    console_clear()
    print(TITLE, 16 * "-", f"| {' | '.join(results)} |", 16 * "-", sep='\n', end=2*'\n')

def print_intro():
    print(
        f"Welcome to Casino Random's {TITLE}",
        16 * "-",
        f"| {' | '.join(spin_slot_machine())} |",
        16 * "-",
        f"Press [X] to exit the game.",
        sep='\n',
    )

def quit(balance):
    resp = input(f"\nPress ENTER to play. \nYou have {balance} 🪙\n")
    if resp.strip().upper() == 'X':
        return True
    return False

def play_slot_machine():
    balance = INITIAL_BALANCE
    print_intro()

    while balance >= BET:
        if quit(balance):
            break

        balance -= BET
        results = spin_slot_machine()
        spin_animation(results)
        display(results)

        win = is_win(results)
        if win:
            win_animation(win)
            display(results)
            payoff = calc_payoff(BET, win)
            balance += payoff

            print(f"🎉 Yay! You {payoff} 🪙 won!")
        else:
            print("Oh, no luck this time!")

        if balance < BET:
            print("💸 Sorry, you are too broke to play")
            break

    print("GOOD BYE!")

if __name__ == "__main__":
    play_slot_machine()
