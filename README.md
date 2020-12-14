# Mastermind.py

A Mastermind type game written in Python.

The computer will generate a number and the user will attempt to guess the number.
The user can determine:

- Whether digits are allowed to repeat
- How many unique digits are allowed in the number
- How long the number will be
- How many guesses the user will have to attempt to get the number

The game ends when either the user guesses the secret number (user win) or the 
user has exhausted the pool of guesses (computer win.)

# Requirements

Python 3.8 or above

# Game Play

Mastermind.py is a guessing game. Your goal is to guess my secret number.
But don't worry - I'll let you help me pick the secret number. You can tell me:
- How long my number should be
- Whether I can repeat digits in it
- How many different digits can be in the number

For example, let's say you just want a 4 digit number, I'll pick a number between 1000 and 9999.
But if you tell me I can't repeat digits then numbers like 9999 are out of the question and I'll
pick something like 1234.

You also get to tell me how many guesses you want. You can pick anywhere from 1 to 25.

I'll also help you out. Every time you make a guess I'll tell you how many digits were correct,
and how many were close (the digit is in the number just not where you think it is.)
For example, lets say my numbers is '5324' and you guessed '1234', I'll let you know how
you did by showing you this:

        XXO- 1254

Every 'X' means you have a digit in the correct place. Every 'O' means you have a digit in the
number but not in the reight place. Any digit that's not in my number is represented by a '-'.
But don't get confused! The 'X'es and 'O'es don't tell you which digit it is! In that example
the 1 and 4 were correct and the 2 was close but the 'X'es and 'O'es aren't in that order.

You can always take a look back at what the guesses were so far (and how close you were) by
selecting H when I ask you for a guess.

One last thing, I won't let you guess a number that is too long or too short, but I also won't
tell you if you guessed a digit that's not in the game.

Good luck!