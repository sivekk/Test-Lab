#!/usr/bin/env python
#put your code here:
import time
import random

def ALL():

    def countdown(seconds):
        while seconds > 0:
            print(seconds, end='\r')
            time.sleep(1)
            seconds -= 1

    def lottery():
        print('Welcome to the Mega Millions Lottery!')
        print('How much money would you like to deposit?')
        totalMoney=input()
        money=(totalMoney)
        print(money)
        print('\nPlease enter amount of money you would like to spend on a lottery ticket, no $:')
        lotteryMoney=input()
        print('\nYou spent:',lotteryMoney, 'on the lottery.')
        lotteryBAL=str(int(money) - int(lotteryMoney))
        print('Your total balance is $', lotteryBAL)
        lotteryRLG1=random.randint(1,5)
        if lotteryRLG1 == 1:
            lRLG1=('A')
        elif lotteryRLG1 == 2:
            lRLG1=('B')
        elif lotteryRLG1 == 3:
            lRLG1=('C')
        elif lotteryRLG1 == 4:
            lRLG1=('D')
        else:
            lRNG1=('E')
        lotteryRNG1=random.randint(1,9)
        if lotteryRNG1 == 1:
            lRNG1=(1)
        elif lotteryRNG1 == 2:
            lRNG1=(2)
        elif lotteryRNG1 == 3:
            lRNG1=(3)
        elif lotteryRNG1 == 4:
            lRNG1=(4)
        elif lotteryRNG1 == 5:
            lRNG1=(5)
        elif lotteryRNG1 == 6:
            lRNG1=(6)
        elif lotteryRNG1 == 7:
            lRNG1=(7)
        elif lotteryRNG1 == 8:
            lRNG1=(8)
        else:
            lRNG1=(9)
        lotteryRNG2=random.randint(1,9)
        if lotteryRNG2 == 1:
            lRNG2=(1)
        elif lotteryRNG2 == 2:
            lRNG2=(2)
        elif lotteryRNG2 == 3:
            lRNG2=(3)
        elif lotteryRNG2 == 4:
            lRNG2=(4)
        elif lotteryRNG2 == 5:
            lRNG2=(5)
        elif lotteryRNG2 == 6:
            lRNG2=(6)
        elif lotteryRNG2 == 7:
            lRNG2=(7)
        elif lotteryRNG2 == 8:
            lRNG2=(8)
        else:
            lRNG2=(9)
        lotteryRNG3=random.randint(1,9)
        if lotteryRNG3 == 1:
            lRNG3=(1)
        elif lotteryRNG3 == 2:
            lRNG3=(2)
        elif lotteryRNG3 == 3:
            lRNG3=(3)
        elif lotteryRNG3 == 4:
            lRNG3=(4)
        elif lotteryRNG3 == 5:
            lRNG3=(5)
        elif lotteryRNG3 == 6:
            lRNG3=(6)
        elif lotteryRNG3 == 7:
            lRNG3=(7)
        elif lotteryRNG3 == 8:
            lRNG3=(8)
        else:
            lRNG3=(9)
        lotteryNUM=(lRLG1,lRNG1,lRNG2,lRNG3)
        print('\nYour number is:', lotteryNUM)
        countdown(3)
        lotteryCNUM1=random.randint(1,5)
        if lotteryCNUM1 == 1:
            lCNUM1=('A')
        elif lotteryCNUM1 == 2:
            lCNUM1=('B')
        elif lotteryCNUM1 == 3:
            lCNUM1=('C')
        elif lotteryCNUM1 == 4:
            lCNUM1=('D')
        else:
            lCNUM1=('E')
        lotteryCRNG1=random.randint(1,9)
        if lotteryCRNG1 == 1:
            lCRNG1=(1)
        elif lotteryCRNG1 == 2:
            lCRNG1=(2)
        elif lotteryCRNG1 == 3:
            lCRNG1=(3)
        elif lotteryCRNG1 == 4:
            lCRNG1=(4)
        elif lotteryCRNG1 == 5:
            lCRNG1=(5)
        elif lotteryCRNG1 == 6:
            lCRNG1=(6)
        elif lotteryCRNG1 == 7:
            lCRNG1=(7)
        elif lotteryCRNG1 == 8:
            lCRNG1=(8)
        else:
            lCRNG1=(9)
        lotteryCRNG2=random.randint(1,9)
        if lotteryCRNG2 == 1:
            lCRNG2=(1)
        elif lotteryCRNG2 == 2:
            lCRNG2=(2)
        elif lotteryCRNG2 == 3:
            lCRNG2=(3)
        elif lotteryCRNG2 == 4:
            lCRNG2=(4)
        elif lotteryCRNG2 == 5:
            lCRNG2=(5)
        elif lotteryCRNG2 == 6:
            lCRNG2=(6)
        elif lotteryCRNG2 == 7:
            lCRNG2=(7)
        elif lotteryCRNG2 == 8:
            lCRNG2=(8)
        else:
            lCRNG2=(9)
        lotteryCRNG3=random.randint(1,9)
        if lotteryCRNG3 == 1:
            lCRNG3=(1)
        elif lotteryCRNG3 == 2:
            lCRNG3=(2)
        elif lotteryCRNG3 == 3:
            lCRNG3=(3)
        elif lotteryCRNG3 == 4:
            lCRNG3=(4)
        elif lotteryCRNG3 == 5:
            lCRNG3=(5)
        elif lotteryCRNG3 == 6:
            lCRNG3=(6)
        elif lotteryCRNG3 == 7:
            lCRNG3=(7)
        elif lotteryCRNG3 == 8:
            lCRNG3=(8)
        else:
            lCRNG3=(9)
        lotteryCNUM=(lCNUM1,lCRNG1,lCRNG2,lCRNG3)
        print('The correct number is:',lotteryCNUM)
        if lotteryNUM == lotteryCNUM:
            print('You won the lottery!')
            lotteryWIN=lotteryMoney*100000
            print('You won:',lotteryWIN)
            print('Your total balance is now:', str(int(lotteryBAL)+int(lotteryWIN)))
        else:
            print('You lost.')
            print('You made: $0')
            print('Your total balance is: $'+ lotteryBAL)
            quit()

    def russianRoulet():
        print('Welcome to Russian Roulet!')
        print('How much money would you like to deposit?')
        totalMoney=input()
        money=(totalMoney)
        print(money)
        print('\nPlease enter amount of money you would like to spend on Russian Roulet, no $:')
        rusrouMoney=input()
        print('\nYou spent: $'+rusrouMoney,'on your life.')
        rusrouBAL=str(int(money) - int(rusrouMoney))
        print('Your total balance is: $'+ rusrouBAL)
        print('\nGame starting in:')
        countdown(3)
        rusrou1W=str(int(rusrouBAL)+1000)
        rusrou2W=str(int(rusrouBAL)+100000)
        russianRNG=random.randint(1,4)
        if russianRNG == 2:
            print("\nBANG! You're dead")
            print('You made: $0')
            print('Your total balance is: $'+rusrouBAL)
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
                        print('Your total balance is: $'+rusrouBAL)
                        quit()
                    else:
                        print('You Selected: No Triple or Nothing')
                        print('You made: $100,000')
                        print('Your total balance is: $'+rusrou2W)
                        quit()
                else:
                    print("\nBANG! You're dead")
                    print('You made: $0')
                    print('Your total balance is: $'+rusrouBAL)
                    quit()
            else:
                print('You Selected: No Double or Nothing')
                print('You made: $1,000')
                print('Your total balance is: $'+rusrou1W)
                quit()

    def slots():
        print('Welcome to the Slot Machine!')
        print('\nHow much money would you like to deposit?')
        totalMoney=input()
        money=(totalMoney)
        print(money)
        print('\n\nHow much money would you like to bet on the slot machine?')
        slotsMoney=input()
        print('You bet:', slotsMoney,'on Slots')
        slotsBAL=str(int(money)-int(slotsMoney))
        print('Your total balance is now:', slotsBAL)
        print('Slots starting in:')
        countdown(3)
        print('\n')
        slotsRNG1=random.randint(1,5)
        slotsRNG2=random.randint(1,5)
        slotsRNG3=random.randint(1,5)
        if slotsRNG1 == slotsRNG2:
            if slotsRNG2 == slotsRNG3:
                print("YOU'RE THE LUCKY WINNER!!!")
                slotsWIN=slotsMoney*1000
                print('You won'+slotsWIN)
                print('Your total balance is: $'+ str(int(slotsWIN)+(int(slotsBAL))))
            else:
                print('You lost.')
                print('You made: $0')
                print('Your total balance is: $'+ slotsBAL)
                quit()
        else:
            print('You lost.')
            print('You made: $0')
            print('Your total balance is: $'+ slotsBAL)
            quit()

    def Games():
        print('WHICH GAME WOULD YOU LIKE TO PLAY?')
        print('Please enter 1, 2, or 3')
        print('1. Lottery Ticket')
        print('2. Russian Roulet')
        print('3. Slots')
        game=input()
        print('\n')
        if game == '1':
            print('Lottery selected, game starting in:')
            countdown(3)
            lottery()
        elif game == '2':
            print('Russian Roulet selected, game starting in:')
            countdown(3)
            russianRoulet()
        elif game == '3':
            print('Slots selected, game starting in:')
            countdown(3)
            slots()
        else:
            print('Please enter 1, 2, or 3')

    def password():
        print('Please enter Password:')
        pswrd=input()
        if pswrd == 'hi':
            print('Correct!')
            print('\n')
            Games()
    password()
ALL()