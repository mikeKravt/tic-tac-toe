import numpy as np
import random

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
        self.board = np.zeros(9, np.int)
        self.human = human
        self.computer = XValue if human == OValue else OValue
        self.state_computer_winner = STATE_WINNER_X if human == OValue else STATE_WINNER_O
        self.state_human_winner = STATE_WINNER_X if human == XValue else STATE_WINNER_O
        self.isHumanOrder = human==XValue
        self.isXOrder = True;
        random.seed()
        
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
        ''' Main cycle of the game '''
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
            move = ask_number("Your move. Please, select one of empty field (1...9): ", 1, self.board.size+1)
            if move not in legal:
                print("\nThis field is already engaged. Please, use another one.\n")
        return move

    def makeComputerMove(self):
        '''Computer running function'''
        board = self.board.copy()
        BEST_MOVES = np.array([[4, 0, 2, 6, 8, 1, 3, 5, 7],
                      [8, 6, 2, 0, 4, 7, 3, 5, 1],
                      [6, 2, 0, 8, 4, 7, 3, 5, 1],
                      [4, 6, 2, 8, 0, 7, 3, 5, 1],
                      [2, 6, 0, 8, 4, 5, 7, 1, 3]], dtype=np.int)
        best_moves = BEST_MOVES[random.randrange(BEST_MOVES.shape[0])]
        print("Computer's move is ", end = " ")
        
        for move in legal_moves(board):
            board[move] = self.computer
            if winner(board) == self.state_computer_winner:
                print(move)
                return move
            board[move] = EmptyValue
        for move in legal_moves(board):
            board[move] = self.human
            if winner(board) == self.state_human_winner:
                print(move)
                return move
            board[move] = EmptyValue
        possible_moves = []
        for move in best_moves:
            if move in legal_moves(board):
                possible_moves.append((move, self.calc_fitness_comp_move(board, move)))
        possible_moves = sorted(possible_moves, key=lambda m: m[1], reverse=True)
        move = possible_moves[0][0]
        print(move)
        return move

    def calc_fitness_comp_move(self, board, move):
        ''' calculate fitness for passed move '''
        board[move] = self.computer
        fitness = 0

        state = winner(board)
        if state==self.state_computer_winner:
            fitness = 1
        elif state==self.state_human_winner:
            fitness = -1
        elif state==STATE_DRAW:
            fitness = 0
        elif state==STATE_GAME_IN_PROGRESS:
            legal = legal_moves(board);
            possible_moves = []
            for human_move in legal:
                possible_moves.append((human_move, self.calc_fitness_human_move(board, human_move)))
            possible_moves = sorted(possible_moves, key=lambda m: m[1])
            fitness = possible_moves[0][1]
        board[move] = EmptyValue
        return fitness

    def calc_fitness_human_move(self, board, move):
        ''' calculate fitness for passed move '''
        board[move] = self.human
        fitness = 0

        state = winner(board)
        if state==self.state_computer_winner:
            fitness = 1
        elif state==self.state_human_winner:
            fitness = -1
        elif state==STATE_DRAW:
            fitness = 0
        elif state==STATE_GAME_IN_PROGRESS:
            legal = legal_moves(board);
            possible_moves = []
            for computer_move in legal:
                possible_moves.append((computer_move, self.calc_fitness_comp_move(board, computer_move)))
            possible_moves = sorted(possible_moves, key=lambda m: m[1], reverse=True)
            fitness = possible_moves[0][1]
        board[move] = EmptyValue
        return fitness


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
        try:
            response = int(input(question))
        except:
            print("Please, enter one digit")
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
    if ask_yes_no("Do you wannna play as "+XChar+"? (y/n): "):
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
    while True:
        board = init_game()
        board.startGame()
        if not ask_yes_no("Do you wanna repeat? (y/n)"):
            break
    
main()
