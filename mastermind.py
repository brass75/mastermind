#! /usr/bin/env python3
import sys
import random
from collections import Counter

MAX_GUESSES = 25
DEFAULT_GUESSES = 10
MAX_DIGITS = 6
MIN_DIGITS = 2
DEFAULT_DIGITS = 4

class Guess:
    def __init__(self, secret: str, guess: str):
        close = 0
        right = 0
        count = Counter(secret)
        for i, c in enumerate(guess):
            if i < len(secret) and secret[i] == c:
                right += 1
                if count[c]:
                    count[c] -= 1
                else:
                    close -= 1
            elif c in count and count[c]:
                close += 1
                count[c] -= 1
        self.length = len(secret)
        self.guess = guess
        self.res = {'right': right, 'close': close}

    def __str__(self):
        s = ''
        s += 'X' * self.res['right']
        s += 'O' * self.res['close']
        s += '-' * (len(self.guess) - len(s))
        s += ' ' + self.guess
        return s

    def isAWin(self):
        return self.right == self.length
    
    @property
    def right(self):
        return self.res['right']

    @property
    def close(self):
        return self.res['close']


def getIntFromUser(prompt, *, low=1, high=2**31, attempts=3, default=None):
    num = 0
    count = attempts + 1
    while not num and (count := count - 1):
        read = input(prompt + '  ')
        if not read:
            if default:
                return default
            continue
        try:
            num = int(read)
            if num >= low and num <= high:
                return num
            s = 'low'
            if num > high:
                s = 'high'
            print (f"I'm sorry but {num} is too {s}. It needs to be between {low} and {high}.")
            num = 0
        except ValueError:
            print(f"I'm sorry but {read!r} is not a number.")
    print(f"I'm sorry but you've used {attempts} and I can't ask any more.")
    return None


def game():
    guesses = 0
    digits = 0
    count = 0
    history = []
    if not (guesses := getIntFromUser(f"How many guesses would you like? Please enter a number from 1 - {MAX_GUESSES} ({DEFAULT_GUESSES})", 
                                     low=1, high=MAX_GUESSES, default=DEFAULT_GUESSES)):
        print("Goodbye.")
        sys.exit(1)
    print(f"OK. So we're going to give you {guesses} to try to solve my number!")
    count = 0
    if not (digits := getIntFromUser(f"How long a problem do you want? Please enter a number from {MIN_DIGITS} - {MAX_DIGITS} ({DEFAULT_DIGITS})",
                                    low=MIN_DIGITS, high=MAX_DIGITS, default=DEFAULT_DIGITS)):
        print("Goodbye.")
        sys.exit(1)
    print (f"OK! We've got a game to play!")
    secret = str(random.randrange(10**(digits-1), 10**digits))
    while True:
        count = 0
        read = input(f"You've got {guesses} left to guess my {digits} digit number. Type 'h' to see the history or let me know what your guess is.  ")
        if not read:
            read = input("You sure you want to quit (Y/n)?  ")
            if not read or read[0].lower != 'y':
                print("OK. Goodbye! Nice playing with you!")
                sys.exit(0)
            continue
        if read.lower() == 'h':
            for i, guess in enumerate(history, 1):
                print (f"{i}:\t{guess}")
            continue
        if len(read.strip()) != digits:
            if (count := count + 1) >= 3:
                print (f"OK. {count} invalid guesses is too many. I'm outta here!")
                sys.exit(1)
            if len(read.strip()) < digits:
                s = 'less'
            else:
                s = 'more'
            print (f"Hey! {read.strip()!r} i {s} than {digits} digits. Please try again!")
            continue            
        try:
            int(read)
            guess = read
        except ValueError:
            if (count := count + 1) >= 3:
                print (f"OK. {count} invalid guesses is too many. I'm outta here!")
                sys.exit(1)
            print (f"Hey! {read.strip()!r} isn't a valid entry. Please try again!")
            continue
        result = Guess(secret, guess)
        history.append(result)
        if result.isAWin():
            print(f"Congrats! You win! You guessed my secret number of {secret}!")
            return
        if (guesses := guesses -1):
            print(f"{result}   Not quite there yet. You have {result.right} in the right place and {result.close} are in the mix.")
        else:
            print(f"YEAH!!! I WIN!!! You couldn't guess my secret number! It was {secret}")
            return

while input('Do you want to play a game with me (y/N)? ').lower() == 'y':
    game()
    
