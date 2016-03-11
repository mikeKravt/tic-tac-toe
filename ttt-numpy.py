import numpy as np

XChar = "X"
OChar = "O"
EmptyChar = " "

EmptyValue = 0
XValue = 1
OValue = 2

STATE_GAME_IN_PROGRESS = 0
STATE_WINNER_X = 1
STATE_WINNER_O = 2
STATE_DRAW = 3

board = None

class Board(object):
    '''class for game-board handling'''
    
    def __init__(self, human):
        '''constructor'''
        # print(human)
        self.board = np.zeros(9, np.int)
        self.human = human
        self.isHumanOrder = human==XValue
        self.isXOrder = True;
        
    @staticmethod
    def valueAsChar(value):
        if value == EmptyValue:
            return EmptyChar
        elif value == XValue:
            return XChar
        elif value == OValue:
            return OChar
        else:
            raise Exception("Unknown value in board!!!")
    
    def display(self):
        '''method display the current position on the console'''
        print("\n\t", self.valueAsChar(self.board[0]), "|",
              self.valueAsChar(self.board[1]), "|", self.valueAsChar(self.board[2]))
        print("\t", "--+---+--")
        print("\t", self.valueAsChar(self.board[3]), "|",
              self.valueAsChar(self.board[4]), "|", self.valueAsChar(self.board[5]))
        print("\t", "--+---+--")
        print("\t", self.valueAsChar(self.board[6]), "|",
              self.valueAsChar(self.board[7]), "|", self.valueAsChar(self.board[8]), "\n")

    def startGame(self):
        while not isGameEnded(self.board):
            self.display()
            if self.isHumanOrder:
                self.board[self.makeHumanMove()] = XValue if self.isXOrder else OValue
            else:
                self.board[self.makeComputerMove()] = XValue if self.isXOrder else OValue
            self.isHumanOrder = not self.isHumanOrder
            self.isXOrder = not self.isXOrder

        self.display()
        gameResult = winner(self.board)
        print(gameResult)
        if gameResult == STATE_DRAW:
            print("Game result is DRAW. Nobody won.")
        elif (gameResult == STATE_WINNER_X and self.human==XValue)\
            or (gameResult == STATE_WINNER_O and self.human==OValue):
                print("You won! Congratulates!")
        elif (gameResult == STATE_WINNER_X and self.human==OValue)\
            or (gameResult == STATE_WINNER_O and self.human==XValue):
                print("I am winner! Don't worry, baby!")
        else:
            raise Exception("Something wrong")
        

    def makeHumanMove(self):
        '''Human running function'''
        legal = legal_moves(self.board)
        move = None
        while move not in legal:
            print(self.board)
            move = ask_number("Your move. Please, select one of empty field (1...9): ", 1, self.board.size)
            if move not in legal:
                print("\nThis field is already engaged. Please, use another one.\n")
        return move

    def makeComputerMove(self):
        '''Computer running function'''

def legal_moves(board):
    '''Function to create a list of available moves'''
    moves = []
    for square in range(board.size):
        if board[square] == EmptyValue:
            moves.append(square)
    return moves

def ask_number(question, low, high):
    '''Function for the number of band request'''
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response-1

def isGameEnded(board):
    '''returns true if game has ended'''
    return winner(board)!=STATE_GAME_IN_PROGRESS
        
def winner(board):
    '''Winner determination function, returns STATE_* constants'''
    WAYS_TO_WIN = ((0, 1, 2),
                   (3, 4, 5),
                   (6, 7, 8),
                   (0, 3, 6),
                   (1, 4, 7),
                   (2, 5, 8),
                   (0, 4, 8),
                   (2, 4, 6))
    for row in WAYS_TO_WIN:
        if board[row[0]] == board[row[1]] == board[row[2]] != EmptyValue:
            if (board[row[0]]==XValue):
                return STATE_WINNER_X
            else:
                return STATE_WINNER_O
    if EmptyValue not in board:
        return STATE_DRAW
    return STATE_GAME_IN_PROGRESS


def ask_yes_no(question):
    '''Function asks the question, the answer to be yes or no'''
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response == "y"

def display_instructions():
    '''Function for the user instructing'''
    print(
    """
    Welcome to the tic-tac-toe game.
    To make a move, enter a digit from 1 to 9. This digit accords
    to the board's fields as it defined below:
    
    1 | 2 | 3
    --+---+--
    4 | 5 | 6
    --+---+--
    7 | 8 | 9
    """
    )

def init_game():
    '''Function asks who is moving the first'''
    if ask_yes_no("Do you want to play as "+XChar+"? (y/n): "):
        human = XValue
        print("You move first")
    else:
        human = OValue
        print("Computer moves first")
    board = Board(human)
    return board

def main():
    display_instructions()
    global board
    board = init_game()
    board.startGame()
    
main()
