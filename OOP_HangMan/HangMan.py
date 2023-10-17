#HangMan Game using Python OOP
#By ShooterMK2
"""
New Tip rule:
level 0: 35% of the word 
level 1: 25% of the word
level 2: 15% of the word

Introduce Standard length of a word to provide more/fewer tips when encountering VeryLong words/VeryShort words
current standard length = 8

current tip amount formula:
(1 + (length of word - standard length) / standard length) / 1.6 * difficulty, which 1.6 is preventing tip amount > len(word)
"""
#---------------------------------------------------------#
import random
from wordhoard import Synonyms

class Hangman():
    # Class variables
    isWin = False
    word = ""
    Max_Fail = 4   #Max amount chance of the easiest mode
    Fail = 0    
    difficulty = -1
    standard_length = 8
    tip_amount = [0.4, 0.27, 0.12]
    tip_index = []
    UI_guess = []

    HANGMANPICS = [" +---+\n | |\n |\n |\n |\n |\n=========", " +---+\n | |\n | O\n |\n |\n |\n=========", " +---+\n | |\n | O\n | |\n |\n |\n=========", " +---+\n | |\n | O\n |/|\n |\n |\n=========", " +---+\n | |\n | O\n |/|\ \n |\n |\n=========", " +---+\n | |\n | O\n |/|\ \n |/ \n |\n=========", " +---+\n | |\n | O \n |/|\ \n |/ \ \n |\n========="] 

    # Class functions
    def __init__(self, target, level):  #initialize the game
        self.word = target
        self.difficulty = level
        self.Max_Fail -= level   #e.g. 4 - (level)1 = 3 chances 

        for i in range(len(self.word)):
            if self.word[i] == " ":
                self.UI_guess.append(" ")   #skip space
            else:
                self.UI_guess.append("_")
        
        self.tip_index = random.sample(range(len(self.word)), round(len(self.word) * ((1+(len(self.word) - self.standard_length) / self.standard_length) / 1.6) * self.tip_amount[self.difficulty] ))   # select tip index without duplicates

        for index in self.tip_index:
            self.UI_guess[index] = self.word[index] 
    
    def PrintGameInfo(self): # this is a Debug function, Can be ignored
        print(f"Target: {self.word}\nDifficulty :{self.difficulty}\nAttempt: {self.Max_Fail}\nTip amount: {self.tip_amount[self.difficulty]}\nUI: {self.UI_guess}")

    def update_guess(self, userInput):
        isSuccess = False
        for index, char in enumerate(self.word):
            if char.lower() == userInput.lower():
                isSuccess = True
                self.UI_guess[index] = char
        
        return isSuccess

    def PrintUI(self, UIreply):
        picIndex = round(6 * (self.Fail / self.Max_Fail))    # 6 * (Fail / Max_Fail) returns a UI picture index according to percentage of tries used
         
        UI_template = "Chance Remains: {attempts}\n{guesses}\n\n{pic}"
        
        print(UI_template.format(attempts = (self.Max_Fail - self.Fail), guesses = " ".join(self.UI_guess), pic = self.HANGMANPICS[picIndex]))
        print(UIreply)

    def UpdateALL(self):
        for index, char in enumerate(self.word):
            self.UI_guess[index] = char

    def UserAttempts(self):
        UserInput = input("input a character or a string:")

        if len(UserInput) > 1:
            if UserInput.lower() == self.word.lower():
                self.UpdateALL()
                self.isWin = True
                return True
            else:
                print("The answer is not correct!")
                return False
        else:
            return(self.update_guess(UserInput))
        
    def winCheck(self):
        count = 0 
        for item in self.UI_guess:
            if item == "_":
                count += 1
        
        if count == 0:
            self.isWin = True
        
        return True

    def startGame(self):    
        self.PrintUI("")

        while (self.Fail < self.Max_Fail) and not self.isWin:
            
            if not self.UserAttempts():
                self.Fail += 1
                self.PrintUI("Charater/String not included, Try again!\n")
            else:
                self.PrintUI("")
                self.winCheck()

        if not self.isWin:
            print("You Lose, The correct answer is:", self.word)
        else:
            print("You Win!")

# ------------------MAIN CODE------------------ #
# variables
ListofWord = []
synonyms = ""
Level = -1
Target = ""

print("  Synonyms HangMan\n\nPress Enter to start")
input()

synonyms = Synonyms(input("Type a word category here: "))
ListofWord = synonyms.find_synonyms()

Target = ListofWord[random.randint(0, len(ListofWord)-1)]

Level = int(input("Input difficulty(0/1/2): "))

game = Hangman(Target, Level) # Create Game

game.startGame()
