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
        # A grid is a list with 9 sublists, every sublist has 9 values, each value is an instance of Field()
        # Enumerate() is going to be key here.
        # I need to be able to access neighbouring fields in different sublists, but how?
        # Use Field.set_neighbours

        for block_index, block in enumerate(grid):
            for field_index, field in enumerate(block):
                neighbours = []

                # Check left neighbour
                if field_index > 0:
                    left = block[field_index - 1]
                # Check left neighbour in left neighbouring block
                elif block_index not in (1, 4, 7):  # this is the same as elif block_index != 1 || block_index != 4 || block_index != 7:
                    left = grid[block_index - 1][field_index + 2]
                # If current field is in the first column of the grid (leftmost, has no neighbours to it's left):
                else:
                    left = None
                neighbours.append(left)

                # Check right neighbour inside current block
                if field_index < 3:
                    right = block[field_index + 1]
                # Check right neighbour in the right neighbouring block
                elif block_index not in (3, 6, 9):
                    right = grid[block_index + 1][field_index - 2]
                # If current field is on the last column of the grid (rightmost, has no neighbours to the right:
                else:
                    right = None
                neighbours.append(right)

                # Check field above current field
                if field_index > 3:
                    up = block[field_index + 3]
                # Check field above current field if this is field is inside 1 block above
                elif block_index not in (1, 2, 3):  # could use block_index > 3, but this is more consistent with syntax
                    up = grid[block_index - 3][field_index + 6]
                else:
                    up = None
                neighbours.append(up)

                # Check field below current field
                if field_index < 7:
                    down = block[field_index + 3]
                elif block_index not in (7, 8, 9):
                    down = grid[block_index + 3][field_index - 6]
                else:
                    down = None
                neighbours.append(down)

                field.set_neighbours(neighbours)



    def board_to_string(self):

        output = ""
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                output += self.board[row][col].get_value()
            output += "\n"
        return output

    def get_board(self):
        return self.board
