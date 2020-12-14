#! /usr/bin/env python3
'''
A Mastermind type game written in Python.

The computer will generate a number and the user will attempt to guess the number.
The user can determine:

    Whether digits are allowed to repeat
    How many unique digits are allowed in the number
    How long the number will be
    How many guesses the user will have to attempt to get the number

The game ends when either the user guesses the secret number (user win) or the 
user has exhausted the pool of guesses (computer win.)
'''


import sys
import random
from collections import Counter

MAX_GUESSES = 25
DEFAULT_GUESSES = 10
MAX_DIGITS = 6
MIN_DIGITS = 2
DEFAULT_DIGITS = 4
allow_repeats = True
distinct_digits = 10

class Guess:
    def __init__(self, secret: str, guess: str):
        '''
            Constructor for the Guess class

            Parameters:
                secret:     The secret number
                guess:      The guessed number
            
            Returns:
                A Guess object
        '''
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
        '''
            Return the string representation of a guess.
        '''
        s = ''
        s += 'X' * self.res['right']
        s += 'O' * self.res['close']
        s += '-' * (len(self.guess) - len(s))
        s += ' ' + self.guess
        return s
    

    @property
    def isAWin(self):
        '''
            Property to return whether the guess was a winning guess.
        '''
        return self.right == self.length
    
    @property
    def right(self):
        '''
            Property to return the number of correct (correct number and correct place) digits in the guess.
        '''
        return self.res['right']

    @property
    def close(self):
        '''
            Property to return the number of close (correct number but incorrect place) digits in the guess.
        '''
        return self.res['close']


def getIntFromUser(prompt: str, *, low: int = 1, high: int = 2**31, attempts: int = 3, default: int = None) -> int:
    '''
        Attemps to get an integer from the user.

        Positional Parameters:
            prompt:         String. The text to prompt the user when asking for input.
        
        Named Parameters:
            low:            Integer. The lowest allowed number. Default: 1
            high:           Integer. The highest allowed number. Default: 2^31
            attempts:       Integer. The number of times to ask if invalid input was received. Default: 3
            default:        Integer. The default value. Default: None

        Returns:
            If the user entered a valid integer: The integer entered by the user.
            ELSE
            None

        NOTE: When using this function the check should be against None unless 0 is not with the range defined by high and low.
    '''
    num = 0
    count = attempts + 1
    while not num and (count := count - 1):
        read = input(prompt + '  ')
        if not read:
            if default != None:
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

def getSecret(num_digits: int, allow_repeats: bool, distinct_digits: int) -> str:
    '''
        Generate the secret number

        Parameters:
            num_digits:      Integer. The length of the secret number.
            allow_repeats:   Boolean. Whether digits are allowed to repeat.
            distinct_digits: Integer. The number of distinct digites allowed.

        Returns:
            The secret number as a string.
    '''
    if allow_repeats and distinct_digits == 10:
        return str(random.randrange(10**(num_digits-1), 10**num_digits))
    secret = []
    while len(secret) < num_digits:
        n = random.randrange(1,distinct_digits+1)
        if allow_repeats or n not in secret:
            secret.append(n)
    return ''.join(map(str, secret))


def game():
    '''
        The game function. Starts and conducts an individual game.
    '''

    guesses = 0
    digits = 0
    count = 0
    history = []
    repeat_strings = ['are not', 'are']

# allow_repeats and distinct_digits are global so the user can play a new game with the same configuration easily.
    global allow_repeats
    global distinct_digits

# Check to see if the user wants to allow repeated digits or not.
    if input(f"Repeated digits {repeat_strings[allow_repeats]} currently allowed. Do you want to change this (y/N)?").lower().strip() == 'y':
        allow_repeats = not allow_repeats

# Check to see how many unique digits the user wants in play
    if input(f"{distinct_digits} unique digits are currently in use. Do you want to change this (y/N)?").lower().strip() == 'y':
        n = getIntFromUser("How many distinct digits, 3 - 10, would you like to use?",
                           low=3, high=10, default=distinct_digits)
        if n:
            distinct_digits = n

# Give the user the current conditions of the game.
    print (f"For this game we're going to use {distinct_digits} ({', '.join(map(str, range(distinct_digits)))}) digits and repeated digits {repeat_strings[allow_repeats]} allowed.")

# Get the user to tell us how many guesses they want to try and solve the number
    if not (guesses := getIntFromUser(f"How many guesses would you like? Please enter a number from 1 - {MAX_GUESSES} ({DEFAULT_GUESSES})", 
                                     low=1, high=MAX_GUESSES, default=DEFAULT_GUESSES)):
        print("Goodbye.")
        sys.exit(1)
    print(f"OK. So we're going to give you {guesses} to try to solve my number!")
    count = 0

# If we're not allowing repeated digits we can't allow a number that is shorter than the number of distinct digits
    if not allow_repeats:
        min_digits = min(distinct_digits, MIN_DIGITS)
    else:
        min_digits = MIN_DIGITS
# Get the length of the number from the user
    if not (digits := getIntFromUser(f"How long a problem do you want? Please enter a number from {min_digits} - {MAX_DIGITS} ({DEFAULT_DIGITS})",
                                    low=min_digits, high=MAX_DIGITS, default=DEFAULT_DIGITS)):
        print("Goodbye.")
        sys.exit(1)

    secret = getSecret(digits, allow_repeats, distinct_digits)

    print (f"""OK! We've got a game to play!
For this game you have {guesses} guesses to try and guess my {digits} digit number.
As a reminder, digits {repeat_strings[allow_repeats]} to repeat and only the digits {', '.join(map(str, range(1, distinct_digits + 1)))} are in use.

Let's play!
    """)

# The game loop.
    while True:

# Initialize count to 0 at the start of each loop because the invalid guess counter should not be cumulative.
        count = 0

# Get the guess. We can't use getIntFromUser because we need to capture the 'h' if the user wants the history.
        read = input(f"You've got {guesses} left to guess my {digits} digit number. Type 'h' to see the history or let me know what your guess is.  ")
        if not read:
            read = input("You sure you want to quit (Y/n)?  ")
            if not read or read[0].lower != 'y':
                print("OK. Goodbye! Nice playing with you!")
                sys.exit(0)
            continue

# The user wants the history so lets give it to them.
        if read.lower() == 'h':
            print(f"""
You have {guesses} guesses remaining to try and guess my {digits} digit number.
As a reminder, digits {repeat_strings[allow_repeats]} to repeat and only the digits {', '.join(map(str, range(1, distinct_digits + 1)))} are in use.
                  """)
            for i, guess in enumerate(history, 1):
                print (f"{i}:\t{guess}")
            continue

# Verify that the user's number is the right length.
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
# Make sure the user's input is actually a number.
        try:
            int(read)
            guess = read
        except ValueError:
            if (count := count + 1) >= 3:
                print (f"OK. {count} invalid guesses is too many. I'm outta here!")
                sys.exit(1)
            print (f"Hey! {read.strip()!r} isn't a valid entry. Please try again!")
            continue

# Check the guess against the secret number
        result = Guess(secret, guess)
# And add it to the history.
        history.append(result)

# Determine what's next based on the guess.
        if result.isAWin:
            print(f"Congrats! You win! You guessed my secret number of {secret}!")
            return
        if (guesses := guesses -1):
            print(f"{result}   Not quite there yet. You have {result.right} in the right place and {result.close} are in the mix.")
        else:
            print(f"YEAH!!! I WIN!!! You couldn't guess my secret number! It was {secret}")
            return

def help():
    '''
        Prints the help for the game.
    '''
    print(f'''
Hello and welcome to Mastermind.py.
Mastermind.py is a guessing game. Your goal is to guess my secret number. 
But don't worry - I'll let you help me pick the secret number. You can tell me:
    How long my number should be
    Whether I can repeat digits in it
    How many different digits can be in the number

For example, let's say you just want a 4 digit number, I'll pick a number between 1000 and 9999. 
But if you tell me I can't repeat digits then numbers like 9999 are out of the question and I'll
pick something like 1234.

You also get to tell me how many guesses you want. You can pick anywhere from 1 to {MAX_GUESSES}.

I'll also help you out. Every time you make a guess I'll tell you how many digits were correct,
and how many were close (the digit is in the number just not where you think it is.)
For example, lets say my numbers is '5324' and you guessed '1234', I'll let you know how
you did by showing you this:

        {Guess('1324', '1254')}

Every 'X' means you have a digit in the correct place. Every 'O' means you have a digit in the
number but not in the reight place. Any digit that's not in my number is represented by a '-'.
But don't get confused! The 'X'es and 'O'es don't tell you which digit it is! In that example
the 1 and 4 were correct and the 2 was close but the 'X'es and 'O'es aren't in that order.

You can always take a look back at what the guesses were so far (and how close you were) by
selecting H when I ask you for a guess.

One last thing, I won't let you guess a number that is too long or too short, but I also won't
tell you if you guessed a digit that's not in the game.

Good luck!
          ''')


# Keep playing until the user says enough.
while True:
    print ("Press H for help.")
    if (read := input('Do you want to play a game with me (y/N)? ').lower().strip()) == 'y':
        game()
    elif read == 'h':
        help()
    else:
        sys.exit(0)    
    
