import random
import pygame

class CandyCrushGame:
    """
    Class to represent the Candy Crush game.

    Attributes:
    - board: list of lists
        Represents the game board as a 2D grid of candies.
    - rows: int
        Number of rows in the game board.
    - cols: int
        Number of columns in the game board.
    """

    def __init__(self, rows: int, cols: int):
        """
        Constructor to instantiate the CandyCrushGame class.

        Parameters:
        - rows: int
            Number of rows in the game board.
        - cols: int
            Number of columns in the game board.
        """

        self.rows = rows
        self.cols = cols
        self.board = self.create_board()

    def create_board(self):
        """
        Creates a new game board with random candies.

        Returns:
        - list of lists:
            The newly created game board.
        """

        # List of possible candy types
        candy_types = ['A', 'B', 'C', 'D', 'E']

        # Creating an empty game board
        board = [[' ' for _ in range(self.cols)] for _ in range(self.rows)]

        # Filling the game board with random candies
        for row in range(self.rows):
            for col in range(self.cols):
                board[row][col] = random.choice(candy_types)

        return board

    def print_board(self):
        """
        Prints the current game board.
        """

        for row in self.board:
            print(' '.join(row))

    def swap_candies(self, row1: int, col1: int, row2: int, col2: int):
        """
        Swaps two candies on the game board.

        Parameters:
        - row1: int
            Row index of the first candy.
        - col1: int
            Column index of the first candy.
        - row2: int
            Row index of the second candy.
        - col2: int
            Column index of the second candy.
        """

        # Swapping the candies
        self.board[row1][col1], self.board[row2][col2] = self.board[row2][col2], self.board[row1][col1]

    def check_matches(self):
        """
        Checks for matches (3 or more candies of the same type) on the game board.

        Returns:
        - bool:
            True if there are matches, False otherwise.
        """

        # Checking for horizontal matches
        for row in range(self.rows):
            for col in range(self.cols - 2):
                if self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2]:
                    return True

        # Checking for vertical matches
        for row in range(self.rows - 2):
            for col in range(self.cols):
                if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col]:
                    return True

        return False

# Example usage of the CandyCrushGame class:

# Creating a new game with 5 rows and 5 columns
game = CandyCrushGame(5, 5)

# Printing the initial game board
print("Initial Game Board:")
game.print_board()

# Swapping candies at (0, 0) and (0, 1)
game.swap_candies(0, 0, 0, 1)

# Printing the game board after swapping candies
print("\nGame Board after Swapping Candies:")
game.print_board()

# Checking for matches on the game board
if game.check_matches():
    print("\nThere are matches on the game board.")
else:
    print("\nThere are no matches on the game board.")