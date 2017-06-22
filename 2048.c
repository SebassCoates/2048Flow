 /*
 //My C Implementation of 2048 to translate to Go

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

const int DIMEN = 4;
const int QUIT = 'q';
const int EMPTY = '_';
const char * BORDER = "-----------------";
const char * SPACE = "____";
const char * EMPTY_ROW = "|                 |";
const char UP = 'w';
const char DOWN = 's';
const char LEFT = 'a';
const char RIGHT = 'd';

void printWelcomeMessage();
int** allocateMemory();
void initializeBoard(int **);
void addRandomVals(int **);
bool boardIsFull(int** board);
bool chooseFour();
bool inputIsValid(char);
char toLowerCase(char);
void updateBoard(char, int**);
void shiftUp(int**);
void shiftDown(int**);
void shiftLeft(int**);
void shiftRight(int**);
void printBoard(int **);
void printSpacing(int);
bool gameOver(int **);
void freeMemory(int**);

int main() {
	srand(time(NULL));

	printWelcomeMessage();

	int** board = allocateMemory();
	initializeBoard(board);
	printBoard(board);

	char input;
	while(true) {
		do{
			scanf("%c", &input);
			input = toLowerCase(input);
		}
		while(!inputIsValid(input));

		if (input == QUIT) { break; }

		updateBoard(input, board);
		addRandomVals(board);
		printBoard(board);

		if (gameOver(board)) {
			printf("Game Over!\n");
			break;
		}
	}
	freeMemory(board);
	return EXIT_SUCCESS;
}

//Print message specifying gameplay instructions to user
void printWelcomeMessage() {
	printf("\nWecome to 2048\n");
	printf("To move the tiles, use the WASD keys followed by a return\n");
	printf("To quit at any time, press Q\n");
}

//Allocate heap memory for board
int** allocateMemory() {
	int **board = malloc(DIMEN * sizeof(int *));
	for (int i = 0; i < DIMEN; i++) {
		board[i] = malloc(DIMEN * sizeof(int));
	}
	return board;
}

//Populate board array with empty spaces and initial tiles
void initializeBoard(int** board) {
	for (int r = 0; r < DIMEN; r++){
		for (int c = 0; c < DIMEN; c++){
			board[r][c] = EMPTY;
		}
	}

	//Choose two distinct coordinate pairs
	int x1, x2, y1, y2;
	x1 = rand() % DIMEN;
	x2 = rand() % DIMEN;
	y1 = rand() % DIMEN;

	do {
		y2 = rand() % DIMEN;
	}
	while (y1 == y2);

	if (chooseFour()) {
		board[y1][x1] = 4;
	} else {
		board[y1][x1] = 2;
	}

	if (chooseFour()) {
		board[y2][x2] = 4;
	} else {
		board[y2][x2] = 2;
	}
}

//Add new random tile to board (more likely 2 than 4)  IF POSSIBLE!
void addRandomVals(int** board) {
	if (boardIsFull(board)) {
		return;
	}

	int x1, y1;
	do {
		x1 = rand() % DIMEN;
		y1 = rand() % DIMEN;
	}
	while(board[y1][x1] != EMPTY);

	if (chooseFour()) {
		board[y1][x1] = 4;
	} else {
		board[y1][x1] = 2;
	}
}

//Determine if the board is full (no empty tiles)
bool boardIsFull(int** board) {
	int fullnessCounter = 0;
	for (int r = 0; r < DIMEN; r++){
		for (int c = 0; c < DIMEN; c++) {
			if (board[r][c] == EMPTY) {
				fullnessCounter++;
			}
		}
	}
	if (fullnessCounter == 0) {
		return true;
	}
	return false;
}

//Probability of adding a 4 instead of a 2 to the board after a move
bool chooseFour() {
	return (rand() % 10 == 0);
}

//Filter input for valid characters, q + wasd
bool inputIsValid(char input) {

	if (input == UP) {
		return true;
	} else if (input == LEFT) {
		return true;
	} else if (input == DOWN) {
		return true;
	} else if (input == RIGHT) {
		return true;
	} else if (input == QUIT) {
		return true;
	}

	return false;
}

//Convert char to lowercase 
char toLowerCase(char input) {
    if ((input >= 65) && (input <= 90))
        input += 32; 
    return input;  
}


//Shift board in direction specified by user
void updateBoard(char command, int** board) {

	if (command == UP) {
		shiftUp(board);
	} else if (command == LEFT) {
		shiftLeft(board);
	} else if (command == DOWN) {
		shiftDown(board);
	} else {
		shiftRight(board);
	}
}

//Shifts tiles up in grid according to 2048 rules
void shiftUp(int** board) {
	for (int r = 0; r < DIMEN - 1; r++) {
		for (int c = 0; c < DIMEN; c++) {
			if (board[r][c] == EMPTY) {
				for (int k = 1; k + r < 4; k++){
					if (board[r + k][c] != EMPTY){
						board[r][c] = board[r + k][c];
						board[r + k][c] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for (int k = 1; k + r < 4; k++) {
					if (board[k + r][c] == board[r][c]) {
						board[r][c] *= 2;
						board[k + r][c] = EMPTY;
						break;
					} if (board[k + r][c] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles down in grid according to 2048 rules
void shiftDown(int** board) {
	for (int r = DIMEN - 1; r > 0; r--) {
		for (int c = 0; c < DIMEN; c++) {
			if (board[r][c] == EMPTY) {
				for (int k = 1; r - k >= 0; k++){
					if (board[r - k][c] != EMPTY){
						board[r][c] = board[r - k][c];
						board[r - k][c] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for (int k = 1; r - k >= 0; k++) {
					if (board[r - k][c] == board[r][c]) {
						board[r][c] *= 2;
						board[r - k][c] = EMPTY;
						break;
					} if (board[r - k][c] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles to left in grid according to 2048 rules
void shiftLeft(int** board) {
	for (int r = 0; r < DIMEN; r++) {
		for (int c = 0; c < DIMEN - 1; c++) {

			if (board[r][c] == EMPTY) {
				for (int k = 1; k + c < 4; k++){
					if (board[r][c + k] != EMPTY){
						board[r][c] = board[r][c + k];
						board[r][c + k] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for (int k = 1; k + c < 4; k++) {
					if (board[r][c + k] == board[r][c]) {
						board[r][c] *= 2;
						board[r][c + k] = EMPTY;
						break;
					} if (board[r][c + k] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles to right in grid according to 2048 rules
void shiftRight(int** board) {
	for (int r = 0; r < DIMEN; r++) {
		for (int c = DIMEN - 1; c > 0; c--) {
			if (board[r][c] == EMPTY) {
				for (int k = 1; c - k >= 0; k++){
					if (board[r][c - k] != EMPTY){
						board[r][c] = board[r][c - k];
						board[r][c - k] = EMPTY;
						c++;
						break;
					}
				}
			} else {
				for (int k = 1; c - k >= 0; k++) {
					if (board[r][c - k] == board[r][c]) {
						board[r][c] *= 2;
						board[r][c - k] = EMPTY;
						break;
					} if (board[r][c - k] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Prints board in nice format to console
void printBoard(int** board) {
	printf(" %s\n", BORDER);
	for (int r = 0; r < DIMEN; r++) {
		printf("%s\n", EMPTY_ROW);
		printf("| ");

		for (int c = 0; c < DIMEN; c++) {
			if (board[r][c] == EMPTY) {
				printf("%s", SPACE);
			} else{ 
				printf("%d", board[r][c]);
				printSpacing(board[r][c]);
			}
		}
		printf("|\n");
	}
	printf(" %s\n", BORDER);
}

//Print spacing based on length of number (assumes 4 digits max number)
void printSpacing(int printedInt) {
	if (printedInt / 100 > 0) {
		printf(" ");
	} else if (printedInt / 10 > 0) {
		printf("  ");
	} else {
		printf("   ");
	}
}

//Checks if no valid moves are left in board, signifies end of game
bool gameOver(int ** board) {
	
	for (int r = 0; r < DIMEN; r++) {
		for (int c = 0; c < DIMEN; c++) {
			if (board[r][c] == EMPTY) {
				return false;
			}
			if (r - 1 >= 0) {
				if (board[r - 1][c] == board[r][c]) {
					return false;
				}
			}
			if (r + 1 < 4) {
				if (board[r + 1][c] == board[r][c]) {
					return false;
				}
			}
			if (c - 1 >= 0) {
				if (board[r][c - 1] == board[r][c]) {
					return false;
				}
			}
			if (c + 1 < 4) {
				if (board[r][c + 1] == board[r][c]) {
					return false;
				}
			}
 		}
	}

	return true;
}

//Frees dynamic memory allocated for 2048 board
void freeMemory(int** toDelete) {
	for (int i = 0; i < DIMEN; i++) {
		free(toDelete[i]);
	}
	free(toDelete);
}

*/
