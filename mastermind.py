#! /usr/bin/env python3
import sys
import random
from collections import Counter

MAX_GUESSES = 25
DEFAULT_GUESSES = 10
MAX_DIGITS = 6
DEFAULT_DIGITS = 4

def getHint(secret: str, guess: str) -> str:
    cows = 0
    bulls = 0
    count = Counter(secret)
    for i, c in enumerate(guess):
        if i < len(secret) and secret[i] == c:
            bulls += 1
            if count[c]:
                count[c] -= 1
            else:
                cows -= 1
        elif c in count and count[c]:
            cows += 1
            count[c] -= 1
    return {'right': bulls, 'close': cows}

def game():
    guesses = 0
    digits = 0
    count = 0
    while guesses <= 0:
        read = input(f"How many guesses would you like? Please enter a number from 1 - {MAX_GUESSES} ({DEFAULT_GUESSES}) ")
        if not read:
            guesses = DEFAULT_GUESSES
        else:
            try:
                guesses = int(read)
                if guesses > MAX_GUESSES:
                    print(f"Hey! I said you could go as high as {MAX_GUESSES}! {guesses} is too much!")
                    guesses = 0
            except ValueError:
                print(f"Hey! {read} is not a number!")
                if (count := count + 1) >= 3:
                    guesses = DEFAULT_GUESSES
    print(f"OK. So we're going to give you {guesses} to try to solve my number!")
    count = 0
    while digits <= 0:
        read = input(f"How long a problem do you want? Please enter a number from 1 - {MAX_DIGITS} ({DEFAULT_DIGITS})  ")
        if not read:
            digits = DEFAULT_DIGITS
        else:
            try:
                digits = int(read)
                if digits > MAX_DIGITS:
                    print(f"Hey! I said you could go as high as {MAX_DIGITS}! {digits} is too much!")
                    digits = 0
            except ValueError:
                print(f"Hey! {read} is not a number!")
                if (count := count + 1) >= 3:
                    digits = DEFAULT_DIGITS
    print (f"OK! We've got a game to play!")
    count = 0
    secret = str(random.randrange(10**(digits-1), 10**digits))
    while True:
        read = input(f"You've got {guesses} left to guess my {digits} digit number. What's your guess?  ")
        if not read:
            read = "You sure you want to quit (Y/n)?  "
            if not read or read[0].lower != 'y':
                print("OK. Goodbye! Nice playing with you!")
                sys.exit(0)
            continue
        try:
            int(read)
            guess = read
        except ValueError:
            if (count := count + 1) >= 3:
                print (f"OK. {count} invalid guesses is too many. I'm outta here!")
                sys.exit(1)
            continue
        result = getHint(secret, guess)
        if result['right'] == digits:
            print(f"Congrats! You win! You guessed my secret number of {secret}!")
            return
        if (guesses := guesses -1):
            print(f"Not quite there yet. You have {result['right']} in the right place and {result['close']} are in the mix.")
        else:
            print(f"YEAH!!! I WIN!!! You couldn't guess my secret number! It was {secret}")
            return

while input('Do you want to play a game with me (y/N)? ').lower() == 'y':
    game()
    
