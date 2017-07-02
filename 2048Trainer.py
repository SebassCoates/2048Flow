#Script to train neural network to play 2048 to be implemented with 2048Flow.go

#for 2048
import random as rand
import time as time

#for reinforcement training
import numpy as np
import tensorflow as tf

#Constants
DIMEN      = 4
QUIT       = 'q'
EMPTY      = -1
BORDER     = "-----------------"
SPACE      = "____"
EMPTY_ROW  = "|                 |"
UP         = 'w'
DOWN       = 's'
LEFT       = 'a'
RIGHT      = 'd'

# "Instance Variables"
board     = [[0 for x in range(DIMEN)] for y in range(DIMEN)] 
highestScore = [0 for x in range(1)]
rand.seed(time.time())

#functions 
#Populate board array with empty spaces and initial tiles
def initializeBoard() :
	for r in range(DIMEN):
		for c in range(DIMEN):
			board[r][c] = EMPTY

	#Choose two distinct coordinate pairs
	x1, x2, y1, y2 = 0, 0, 0, 0
	x1 = rand.randint(0, DIMEN - 1)
	x2 = rand.randint(0, DIMEN - 1)
	y1 = rand.randint(0, DIMEN - 1)
	y2 = rand.randint(0, DIMEN - 1)

	while (y1 == y2) :
		y2 = rand.randint(0, DIMEN - 1)

	if chooseFour():
		board[y1][x1] = 4 
	else: 
		board[y1][x1] = 2

	if chooseFour():
		board[y2][x2] = 4 
	else:
		board[y2][x2] = 2

#Add new random tile to board (more likely 2 than 4)  IF POSSIBLE!
def addRandomVals():
	if boardIsFull():
		return

	x1, y1 = rand.randint(0, DIMEN - 1), rand.randint(0, DIMEN - 1)
	while (board[y1][x1] != EMPTY) :
		x1 = rand.randint(0, DIMEN - 1)
		y1 = rand.randint(0, DIMEN - 1)

	if chooseFour():
		board[y1][x1] = 4
	else:
		board[y1][x1] = 2

#Determine if the board is full (no empty tiles)
def boardIsFull():
	fullnessCounter = 0
	for r in range(DIMEN):
		for c in range(DIMEN):
			if (board[r][c] == EMPTY): 
				fullnessCounter += 1

	if (fullnessCounter == 0):
		return True

	return False

#Probability of adding a 4 instead of a 2 to the board after a move
def chooseFour():
	#10 percent chance to be a 4
	return (rand.randint(0,9) == 0)

#Filter input for valid characters, q + wasd
def chooseMove():
	#TODO
	#Replace with machine learning algorithm !!

	#time.sleep(.5) #sleep for x seconds

	if (rand.randint(0, 1) == 0):
		return 'a'
	elif (rand.randint(0, 2) > 0):
		return 's'
	elif (rand.randint(0, 1) == 1):
		return 'w'
	else:
		return 'd'

#Convert byte to lowercase
def toLowerCase(input):
	if (input >= 65 and input <= 90):
		input += 32

	return input

#Shift board in direction specified by user
def updateBoard(command):

	if (command == UP) :
		shiftUp()
	elif (command == LEFT) :
		shiftLeft()
	elif (command == DOWN) :
		shiftDown()
	else :
		shiftRight()

#Shifts tiles up in grid according to 2048 rules
def shiftUp():
	for r in range(DIMEN - 1):
		for c in range(DIMEN): 
			if (board[r][c] == EMPTY):
				for k in range(1, 4 - r, 1):
					if (board[r+k][c] != EMPTY):
						board[r][c] = board[r+k][c]
						board[r+k][c] = EMPTY
						c -= 1
						break
			else:
				for k in range(1, 4 - r, 1):
					if (board[k+r][c] == board[r][c]):
						board[r][c] *= 2
						board[k+r][c] = EMPTY
						break
					if (board[k+r][c] != EMPTY):
						break


#Shifts tiles down in grid according to 2048 rules
def shiftDown():
	for r in range(DIMEN - 1, 0, -1):
		for c in range(DIMEN): 
			if (board[r][c] == EMPTY): 
				for k in range(1, r + 1, 1):
					if (board[r-k][c] != EMPTY): 
						board[r][c] = board[r-k][c]
						board[r-k][c] = EMPTY
						c -= 1
						break
			else:
				for k in (1, r + 1, 1):
					if (board[r-k][c] == board[r][c]): 
						board[r][c] *= 2
						board[r-k][c] = EMPTY
						break
					if (board[r-k][c] != EMPTY):
						break

#Shifts tiles to left in grid according to 2048 rules
def shiftLeft():
	for r in range(DIMEN):
		for c in range (DIMEN - 1):
			if (board[r][c] == EMPTY):
				for k in range(1, 4 - c, 1): 
					if (board[r][c+k] != EMPTY):
						board[r][c] = board[r][c+k]
						board[r][c+k] = EMPTY
						c -= 1
						break
					
				
			else: 
				for k in range(1, 4 - c, 1):
					if (board[r][c+k] == board[r][c]): 
						board[r][c] *= 2
						board[r][c+k] = EMPTY
						break
					
					if (board[r][c+k] != EMPTY): 
						break
					
				
			
		
	


#Shifts tiles to right in grid according to 2048 rules
def shiftRight():
	for r in range(DIMEN): 
		for c in range(DIMEN - 1, 0, -1):
			if (board[r][c] == EMPTY):
				for k in range(1, c + 1, 1):
					if (board[r][c-k] != EMPTY): 
						board[r][c] = board[r][c-k]
						board[r][c-k] = EMPTY
						c += 1
						break
					
				
			else:
				for k in range(1, c + 1, 1):
					if (board[r][c-k] == board[r][c]):
						board[r][c] *= 2
						board[r][c-k] = EMPTY
						break
					
					if (board[r][c-k] != EMPTY): 
						break

#Prints board in nice format to console
def printBoard():
	print(" %s\n" % BORDER, end='')
	for r in range(DIMEN):
		print("%s" % EMPTY_ROW)
		print("| ", end='')

		for c in range(DIMEN):
			if (board[r][c] == EMPTY):
				print("%s" % SPACE , end='')
			else:
				print("%d" % board[r][c] , end='')
				printSpacing(board[r][c])

		print("|")
	print(" %s" % BORDER)

##Print spacing based on length of number (assumes 4 digits max number)
def printSpacing(printedInt):
	if (printedInt > 99) :
		print(" ", end='')
	elif (printedInt > 9) :
		print("  ", end='')
	else :
		print("   ", end='')

#Checks if no valid moves are left in board, signifies end of game
def gameOver():
	for r in range(DIMEN): 
		for c in range(DIMEN):
			if (board[r][c] == EMPTY): 
				return False
			
			if (r-1 >= 0): 
				if (board[r-1][c] == board[r][c]): 
					return False
				
			
			if (r+1 < 4): 
				if (board[r+1][c] == board[r][c]): 
					return False
				
			
			if (c-1 >= 0): 
				if (board[r][c-1] == board[r][c]): 
					return False
				
			
			if (c+1 < 4): 
				if (board[r][c+1] == board[r][c]): 
					return False
	return True


#Returns int value of highest tile value in board
def highestTileValue():
	highestTile = 0

	for r in range(DIMEN):
		for c in range(DIMEN):
			if (board[r][c] > highestTile):
				highestTile = board[r][c]
	return highestTile

def updateState(command):
	updateBoard(command)
	addRandomVals()
	currHighScore = highestTileValue();
	if gameOver():
		if (currHighScore > highestScore[0]):
			highestScore[0] = currHighScore
		return (currHighScore, True)
	else:
		return (currHighScore, False)

def main():
	numGames = 10
	for i in range(numGames):
		initializeBoard() #resets board to beginning state
		while (True):
			command = chooseMove()
			newScore, gameOver = updateState(command)
			if (gameOver):
				break
		
	print("Highest score = %d" % highestScore[0])	

#Call main function on execution 
if __name__ == "__main__":
    main()

