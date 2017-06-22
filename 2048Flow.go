package main

import (
	"fmt"
	"math/rand"
	"time"
)

const (
	DIMEN     int    = 4
	QUIT      byte   = 'q'
	EMPTY     int    = '_'
	BORDER    string = "-----------------"
	SPACE     string = "____"
	EMPTY_ROW string = "|                 |"
	UP        byte   = 'w'
	DOWN      byte   = 's'
	LEFT      byte   = 'a'
	RIGHT     byte   = 'd'
)

var (
	generator = rand.New(rand.NewSource(time.Now().UnixNano()))
	board     [DIMEN][DIMEN]int
)

func main() {
	//These will finish before user can send to Scanf, no need to wait
	go printWelcomeMessage();
	go initializeBoard();
	go printBoard();

	var input byte;
	for true {
		fmt.Scanf("%c", &input)
		input = toLowerCase(input)
		for !inputIsValid(input) {
			fmt.Scanf("%c", &input);
			input = toLowerCase(input);
		}
	
		if input == QUIT { break; }

		updateBoard(input);
		addRandomVals();
		printBoard();

		if (gameOver()) {
			fmt.Printf("Game Over!\n");
			break;
		}
	}
}

//Print message specifying gameplay instructions to user
func printWelcomeMessage() {
	fmt.Printf("\nWecome to 2048\n");
	fmt.Printf("To move the tiles, use the WASD keys followed by a return\n");
	fmt.Printf("To quit at any time, press Q\n");
}

//Populate board array with empty spaces and initial tiles
func initializeBoard() {
	for r := 0; r < DIMEN; r++ {
		for c := 0; c < DIMEN; c++ {
			board[r][c] = EMPTY;
		}
	}

	//Choose two distinct coordinate pairs
	var x1, x2, y1, y2 int;
	x1 = generator.Intn(DIMEN)
	x2 = generator.Intn(DIMEN)
	y1 = generator.Intn(DIMEN)
	y2 = generator.Intn(DIMEN);

	for y1 == y2 {
		y2 = generator.Intn(DIMEN);
	}
	

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
func addRandomVals() {
	if (boardIsFull()) {
		return;
	}

	var x1, y1 = generator.Intn(DIMEN), generator.Intn(DIMEN)
	for board[y1][x1] != EMPTY {
		x1 = generator.Intn(DIMEN);
		y1 = generator.Intn(DIMEN);
	}
	
	
	if (chooseFour()) {
		board[y1][x1] = 4;
	} else {
		board[y1][x1] = 2;
	}
}

//Determine if the board is full (no empty tiles)
func boardIsFull() bool{
	fullnessCounter := 0;
	for r := 0; r < DIMEN; r++ {
		for c := 0; c < DIMEN; c++ {
			if board[r][c] == EMPTY {
				fullnessCounter++;
			}
		}
	}
	if fullnessCounter == 0 {
		return true;
	}
	return false;
}

//Probability of adding a 4 instead of a 2 to the board after a move
func chooseFour() bool{
	return (generator.Intn(DIMEN) == 3);
}

//Filter input for valid characters, q + wasd
func inputIsValid(input byte) bool{

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

//Convert byte to lowercase 
func toLowerCase(input byte) byte {
   	if input >= 65 && input <= 90 {
    	    input += 32 
	}
   	return input;  
}


//Shift board in direction specified by user
func updateBoard(command byte) {

	if (command == UP) {
		shiftUp();
	} else if (command == LEFT) {
		shiftLeft();
	} else if (command == DOWN) {
		shiftDown();
	} else {
		shiftRight();
	}
}

//Shifts tiles up in grid according to 2048 rules
func shiftUp() {
	for r := 0; r < DIMEN - 1; r++ {
		for c := 0; c < DIMEN; c++ {
			if (board[r][c] == EMPTY) {
				for k := 1; k + r < 4; k++ {
					if (board[r + k][c] != EMPTY){
						board[r][c] = board[r + k][c];
						board[r + k][c] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for k := 1; k + r < 4; k++ {
					if (board[k + r][c] == board[r][c]) {
						board[r][c] *= 2;
						board[k + r][c] = EMPTY;
						break;
					} 
					if (board[k + r][c] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles down in grid according to 2048 rules
func shiftDown() {
	for r := DIMEN - 1; r > 0; r-- {
		for c := 0; c < DIMEN; c++ {
			if (board[r][c] == EMPTY) {
				for k := 1; r - k >= 0; k++{
					if (board[r - k][c] != EMPTY){
						board[r][c] = board[r - k][c];
						board[r - k][c] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for k := 1; r - k >= 0; k++ {
					if (board[r - k][c] == board[r][c]) {
						board[r][c] *= 2;
						board[r - k][c] = EMPTY;
						break;
					} 
					if (board[r - k][c] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles to left in grid according to 2048 rules
func shiftLeft() {
	for r := 0; r < DIMEN; r++ {
		for c := 0; c < DIMEN - 1; c++ {

			if (board[r][c] == EMPTY) {
				for k := 1; k + c < 4; k++{
					if (board[r][c + k] != EMPTY){
						board[r][c] = board[r][c + k];
						board[r][c + k] = EMPTY;
						c--;
						break;
					}
				}
			} else {
				for k := 1; k + c < 4; k++ {
					if (board[r][c + k] == board[r][c]) {
						board[r][c] *= 2;
						board[r][c + k] = EMPTY;
						break;
					} 
					if (board[r][c + k] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Shifts tiles to right in grid according to 2048 rules
func shiftRight() {
	for r := 0; r < DIMEN; r++ {
		for c := DIMEN - 1; c > 0; c-- {
			if board[r][c] == EMPTY {
				for k := 1; c - k >= 0; k++ {
					if (board[r][c - k] != EMPTY){
						board[r][c] = board[r][c - k];
						board[r][c - k] = EMPTY;
						c++;
						break;
					}
				}
			} else {
				for k := 1; c - k >= 0; k++ {
					if (board[r][c - k] == board[r][c]) {
						board[r][c] *= 2;
						board[r][c - k] = EMPTY;
						break;
					} 
					if (board[r][c - k] != EMPTY) {
						break;
					}
				}
			}
		}
	}
}

//Prints board in nice format to console
func printBoard() {
	fmt.Printf(" %s\n", BORDER)
	for r := 0; r < DIMEN; r++ {
		fmt.Printf("%s\n", EMPTY_ROW)
		fmt.Printf("| ")

		for c := 0; c < DIMEN; c++ {
			if board[r][c] == EMPTY {
				fmt.Printf("%s", SPACE)
			} else {
				fmt.Printf("%d", board[r][c])
				printSpacing(board[r][c])
			}
		}
		fmt.Printf("|\n")
	}
	fmt.Printf(" %s\n", BORDER)
}

//Print spacing based on length of number (assumes 4 digits max number)
func printSpacing(printedInt int) {
	if printedInt/100 > 0 {
		fmt.Printf(" ")
	} else if printedInt/10 > 0 {
		fmt.Printf("  ")
	} else {
		fmt.Printf("   ")
	}
}

//Checks if no valid moves are left in board, signifies end of game
func gameOver() bool{
	
	for r := 0; r < DIMEN; r++ {
		for c := 0; c < DIMEN; c++ {
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
