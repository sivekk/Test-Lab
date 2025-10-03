#!/usr/bin/env python
#put your code here:
import time
import random

def ALL():
    print('How much money would you like to bet?')

def countdown(seconds):
    while seconds > 0:
        print(seconds, end='\r')
        time.sleep(1)
        seconds -= 1

def lottery():
    print('Welcome to the Mega Millions Lottery!')
    
def russianRoulet():
    print('Welcome to Russian Roulet!')
    russianRNG=random.randint(1,4)
    if russianRNG == 2:
        print("BANG! You're dead")
        quit()
    else:
        print('You survived!')
        print('\nDouble or Nothing?  Please enter yes or no')
        russianDON=input()
        russianRNG2=random.randint(1,2)
        if russianDON == 'yes':
            print('You Selected: Double or Nothing.')
            if russianRNG2 == 1:
                countdown(3)
                print('You Survived again!')
                print('\nTriple or Nothing?  Please enter yes or no')
                russianTON=input()
                if russianTON == 'yes':
                    print('You Selected: Triple or Nothing.')
                    countdown(3)
                    print("\nBANG! You're dead")
                    print('You made: $0')
                    print('Your total balance is: $0')
                    quit()
                else:
                    print('You Selected: No Double or Nothing')
                    print('You made: idk')
                    print('Your total balance is: idk')
                    quit()
            else:
                print("\nBANG! You're dead")
                print('You made: $0')
                print('Your total balance is: $0')
                quit()
        else:
            print('You Selected: No Double or Nothing')
            print('You made:')
            print('Your total balance is:')
            quit()

def slots():
    print('Welcome to the Slot Machine!')
    slotsRNG1=random.randint(1,5)
    slotsRNG2=random.randint(1,5)
    slotsRNG3=random.randint(1,5)
    if slotsRNG1 == slotsRNG2:
        if slotsRNG2 == slotsRNG3:
            print("YOU'RE THE LUCKY WINNER!!!")
            print('$$$')
            print('You won $1,000')
        else:
            print('You lost.')
            print('You made: $0')
            print('Your total balance is: $0')
        quit()
    else:
        print('You lost.')
        print('You made: $0')
        print('Your total balance is: $0')
        quit()

def poker():
    print('\n\nGO AWAY!!\nGOSH!, some people.')
    print('Welcome to Poker!')
def Games():
    print('WHICH GAME WOULD YOU LIKE TO PLAY?')
    print('Please enter a, b, c, or d')
    print('a. Lottery Ticket')
    print('b. Russian Roulet')
    print('c. Slots')
    print('d. Poker')
    game=input()
    print('\n')
    if game == 'a':
        print('Lottery selected, game starting in:')
        countdown(3)
        lottery()
    elif game == 'b':
        print('Russian Roulet selected, game starting in:')
        countdown(3)
        russianRoulet()
    elif game == 'c':
        print('Slots selected, game starting in:')
        countdown(3)
        slots()
    elif game == 'd':
        print('Poker selected, game starting in:')
        countdown(3)
        poker()
    else:
        print('Please enter a, b, c, or d')

def password():
    print('Please enter Password:')
    pswrd=input()
    if pswrd == 'hi':
        print('Correct!')
        print('\n')
        Games()
password()
