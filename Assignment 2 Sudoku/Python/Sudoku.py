from Field import Field


class Sudoku:

    def __init__(self, filename):
        self.board = self.read_sudoku(filename)

    def __str__(self):
        output = "╔═══════╦═══════╦═══════╗\n"
        # iterate through rows
        for i in range(9):
            if i == 3 or i == 6:
                output += "╠═══════╬═══════╬═══════╣\n"
            output += "║ "
            # iterate through columns
            for j in range(9):
                if j == 3 or j == 6:
                    output += "║ "
                output += str(self.board[i][j]) + " "
            output += "║\n"
        output += "╚═══════╩═══════╩═══════╝\n"
        return output

    @staticmethod
    def read_sudoku(filename):
        """
        Read in a sudoku file
        @param filename: Sudoku filename
        @return: A 9x9 grid of Fields where each field is initialized with all its neighbor fields
        """
        assert filename is not None and filename != "", "Invalid filename"
        # Setup 9x9 grid
        grid = [[Field for _ in range(9)] for _ in range(9)]

        try:
            with open(filename, "r") as file:
                for row, line in enumerate(file):
                    for col_index, char in enumerate(line):
                        if char == '\n':
                            continue
                        if int(char) == 0:
                            grid[row][col_index] = Field()
                        else:
                            grid[row][col_index] = Field(int(char))

        except FileNotFoundError:
            print("Error opening file: " + filename)

        Sudoku.add_neighbours(grid)
        return grid

    @staticmethod
    def add_neighbours(grid):
        """
        Adds a list of neighbors to each field
        @param grid: 9x9 list of Fields
        """

    # TODO: for each field, add its neighbors
        # Loop over all rows in the sudoku
        for row in range(9):
            # Loop over all columns in a row
            for col in range(9):
                # Create an empty set to store neighbours of one field
                neighbours = set()

                # Add neighbours in the same row
                for neighbour_col in range(9):
                    # Check if neighbour_col is not the same as the col of the current field
                    if neighbour_col != col:
                        # Add this neighbouring field in the same row if true
                        neighbours.add(grid[row][neighbour_col])

                # Add neighbours in the same column
                for neighbour_row in range(9):
                    # Check if neighbour_row is not the same as the row of the current field
                    if neighbour_row != row:
                        # Add this neighbouring field in the same row if true
                        neighbours.add(grid[neighbour_row][col])

                # Add neighbours in the same 3x3 block
                start_row = 3 * (row // 3)  # Calculate the starting row of the 3x3 block
                start_col = 3 * (col // 3)  # Calculate the starting column of the 3x3 block
                end_row = start_row + 3  # Calculate the ending row + 1 of the 3x3 block
                end_col = start_col + 3  # Calculate the ending column + 1 of the 3x3 block

                # Loop through all rows in the 3x3 block
                for neighbour_row in range(start_row, end_row):
                    # Loop through all columns in the 3x3 block
                    for neighbour_col in range(start_col, end_col):
                        # Check if the coordinates of the neighbouring field is not equal
                        # to the coordinates of the current field: grid[row][col]
                        if (neighbour_row, neighbour_col) != (row, col):
                            # Add the field as neighbour if it is indeed a neighbour
                            neighbours.add(grid[neighbour_row][neighbour_col])

                # Set neighbours for the current field
                grid[row][col].set_neighbours(list(neighbours))
    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board
