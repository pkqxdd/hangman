#!/usr/bin/env python
import random

WORDLIST_FILENAME = "words.txt"

def loadWords():
	"""
	Returns a list of valid words. Words are strings of lowercase letters.

	Depending on the size of the word list, this function may
	take a while to finish.
	"""
	print("Loading word list from file...")
	# inFile: file
	inFile = open(WORDLIST_FILENAME, 'r')
	# line: string
	line = inFile.readline()
	# wordlist: list of strings
	wordlist = line.split()
	print("  ", len(wordlist), "words loaded.")
	return wordlist

def chooseWord(wordlist):
	return random.choice(wordlist)

wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
	sw = {}
	for letter in secretWord:
		sw[letter] = True if letter in lettersGuessed else False
	return False if False in sw.values() else True

def getGuessedWord(secretWord, lettersGuessed):
	sw = {}
	for letter in secretWord:
		sw[letter] = True if letter in lettersGuessed else False
	result = secretWord
	for letter in result:
		if sw[letter] == False:
			result = result.replace(letter, '_ ')
	return result

guessleft = 8
letterGuessed = []

def start_a_new_turn():
	global guessleft
	global letterGuessed
	global secretWord
	guess = Guess.get()
	if guess == "":
		return None

	try:
		assert len(guess) == 1
		assert guess in string.ascii_lowercase
	except AssertionError:
		top = tk.Toplevel()
		top.title = ('')
		tk.Label(top, text='Please enter a single letter!', font=("Helvetica", 22)).pack()
		tk.Button(top, text="Ok", command=lambda: top.destroy()).pack()
		Guess.delete(0, tk.END)
		return None
	except:
		pass
	guess.lower()
	#check if the word was guessed
	if guess in letterGuessed:
		Feedback.config(text="Oops! You've already guessed that letter!")
		Guess.delete(0, tk.END)
		return None
	letterGuessed += guess

	exec(guess + ".config(fg='grey')")#change the color of available letters map

	if isWordGuessed(secretWord, letterGuessed):
		#Winning window
		top = tk.Toplevel()
		top.title = ('')
		tk.Label(top, text='Congratulations! You won!').grid(row=0, column=0, columnspan=3)
		frame = tk.Frame(top)
		tk.Label(frame, text='The word was').grid(row=0, column=0)
		tk.Label(frame, text=secretWord, fg='green').grid(row=0, column=1)
		frame.grid(row=1, column=0, columnspan=3)
		tk.Button(top, text="Quit", command=lambda: root.destroy()).grid(row=2, column=2, sticky='e')
		tk.Button(top, text="Restart", command=lambda: [f() for f in [restart,top.destroy]]).grid(row=2, column=0, sticky='w')
		return None
	

	if guessleft == 0:
		#Losing window
		top = tk.Toplevel()
		top.title = ('')
		tk.Label(top, text='Sorry, you ran out of guesses.').grid(row=0, column=0, columnspan=3)
		frame = tk.Frame(top)
		tk.Label(frame, text='The word was').grid(row=0, column=0)
		tk.Label(frame, text=secretWord, fg='red').grid(row=0, column=1)
		frame.grid(row=1, column=0, columnspan=3)
		tk.Button(top, text="Quit", command=lambda: root.destroy()).grid(row=2, column=2, sticky='e')
		tk.Button(top, text="Restart", command=lambda: [f() for f in [restart,top.destroy]]).grid(row=2, column=0, sticky='w')
		return None
	if guess in secretWord:
		Feedback.config(text='Good guess!')
	else:
		Feedback.configure(text='Oops! That letter is not in my word!')
		guessleft -= 1
	Guessleft.config(text=guessleft)#refresh the red number
	_.config(text=getGuessedWord(secretWord, letterGuessed))
	Guess.delete(0, tk.END)#clear textbox

######GUI#####
import tkinter as tk
import string

def restart():
	global letterGuessed
	global guessleft
	global secretWord
	global Feedback
	global Guessleft
	global _
	letterGuessed = []
	guessleft = 8
	secretWord = chooseWord(wordlist).lower()
	for letter in string.ascii_lowercase:
		exec('global ' + letter)
		exec(letter + ".config(fg='black')")
	Guess.delete(0, tk.END)
	Feedback.config(text="The secret word is " + str(len(secretWord)) + " letters long")
	Guessleft.config(text=guessleft)
	_.config(text=getGuessedWord(secretWord, letterGuessed))
secretWord = chooseWord(wordlist).lower()

root = tk.Tk()
root.wm_title('Hangman')
tk.Label(root, text='Welcome to the game, Hangman!', font=("Times New Roman", 24)).grid(row=0, column=1, rowspan=2)
tk.Label(root, text="You Have").grid(column=2, row=3)
tk.Label(root, text="Guess Left").grid(column=2, row=4)
Guessleft = tk.Label(text=guessleft, font=("Times New Roman", 50), fg='red')
Guessleft.grid(column=3, row=2, rowspan=4)
Feedback = tk.Label(root, text="The secret word is " + str(len(secretWord)) + " letters long")
Feedback.grid(column=1, row=3)
_ = tk.Label(root, text=getGuessedWord(secretWord, letterGuessed))
_.grid(column=1, row=4)
submit = tk.Frame(root)
submit.grid(row=5, column=1)
tk.Label(submit, text='Please enter a letter:').grid(row=0, column=0)
Guess = tk.Entry(submit, width=1)
Guess.grid(row=0, column=1, sticky='w')
Guess.bind('<Return>', lambda x: start_a_new_turn())
Guess.bind('<Button-1>',lambda x:arrow.grid_forget())
arrow=tk.Label(submit, text="<--Enter Your Answer Here", fg="red")
arrow.grid(row=0,column=2)
Available = tk.Frame(root, )
Available.grid(row=3, column=0, rowspan=5)
tk.Label(root, text="Available Letters:", font=('Times New Roman', 14, 'bold')).grid(row=2, column=0)
tk.Button(root, text="Restart", command=lambda: restart()).grid(row=7, column=3)

####available letters map
arrange = (
	['a', 'b', 'c', 'd', 'e', 'f'],
	['g', 'h', 'i', 'j', 'k', 'l'],
	['m', 'n', 'o', 'p', 'q', 'r'],
	['s', 't', 'u', 'v', 'w', 'x'],
	['y', '' , ' ', ' ', ' ', 'z']
)
def getLocation(letter):
	for i in range(5):
		if letter in arrange[i]:
			for j in range(6):
				if letter == arrange[i][j]:
					location = 'row=' + str(i) + ',column=' + str(j)
	return location

for letter in string.ascii_lowercase:
	exec(letter + '=tk.Label(Available,text="' + letter + '")')
	exec(letter + '.grid(' + getLocation(letter) + ')')
 
root.after(2000,lambda:root.focus_force())
root.mainloop()
