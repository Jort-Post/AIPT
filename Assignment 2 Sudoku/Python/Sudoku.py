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
            # Block indices range from 0 to 8. 0 is top left, 8 is bottom right.
            for field_index, field in enumerate(block):
                # Field indices range from 0 to 8, 0 is top left, 8 is bottom right.
                neighbours = []

                for neighbour in block:
                    if neighbour != field:
                        neighbours.append(neighbour)

                # Left & Right; Row

                if field_index in (0, 3, 6):
                    for i in range(3):

                        if block_index in (2, 5, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (1, 4, 7):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 3, 6):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])

                elif field_index in (1, 4, 7):
                    for i in range(-1, 2):

                        if block_index in (2, 5, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (1, 4, 7):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 3, 6):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])

                elif field_index in (2, 5, 8):
                    for i in range(-2, 1):

                        if block_index in (2, 5, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (1, 4, 7):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 3, 6):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])

                # Above & Below; Column

                if field_index in (0, 1, 2):
                    for i in range(3):

                        if block_index in (6, 7, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (3, 4, 5):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 1, 2):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])

                elif field_index in (3, 4, 5):
                    for i in range(-1, 2):

                        if block_index in (6, 7, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (3, 4, 5):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 1, 2):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])

                elif field_index in (6, 7, 8):
                    for i in range(-2, 1):

                        if block_index in (6, 7, 8):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index - 2][field_index + i])

                        elif block_index in (3, 4, 5):
                            neighbours.append(grid[block_index - 1][field_index + i])
                            neighbours.append(grid[block_index + 1][field_index + i])

                        elif block_index in (0, 1, 2):
                            # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                            neighbours.append(grid[block_index + 1][field_index + i])
                            # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                            neighbours.append(grid[block_index + 2][field_index + i])


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
