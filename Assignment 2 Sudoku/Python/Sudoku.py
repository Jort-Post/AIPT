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

        Sudoku.add_neighbours2(grid)
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

        def add_row_neighbours(grid, block_index, field_index, neighbours, i):
            """
            Helper function for adding a field from a block to the right, to the left, and 2 to the right and 2 to the left of the current field to it's neighbours
            :param grid:
            :param block_index:
            :param field_index:
            :param neighbours:
            :param i:
            :return:
            """
            if block_index in (2, 5, 8):
                neighbours.add(grid[block_index - 1][field_index + i])
                # ADD ALL FIELDS FROM LEFT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                neighbours.add(grid[block_index - 2][field_index + i])

            elif block_index in (1, 4, 7):
                neighbours.add(grid[block_index - 1][field_index + i])
                neighbours.add(grid[block_index + 1][field_index + i])

            elif block_index in (0, 3, 6):
                # ADD ALL FIELDS IN NEIGHBOURING RIGHT TO CURRENT FIELD IN THE SAME ROW
                neighbours.add(grid[block_index + 1][field_index + i])
                # ADD ALL FIELDS FROM RIGHT-NEIGHBOURING BLOCK NEXT TO NEIGHBOURING BLOCK IN THE SAME ROW
                neighbours.add(grid[block_index + 2][field_index + i])

            return neighbours

        def add_column_neighbours(grid, block_index, field_index, neighbours, i):
            """
            Helper function for adding a field from a block above and below, or 2 above and 2 below the current field to it's neighbours
            :param grid:
            :param block_index:
            :param field_index:
            :param neighbours:
            :param i:
            :return:
            """
            if block_index in (6, 7, 8):
                # UP 1 BLOCK
                neighbours.add(grid[block_index - 3][field_index + 3 * i])
                # UP 2 BLOCKS
                neighbours.add(grid[block_index - 6][field_index + 3 * i])

            elif block_index in (3, 4, 5):
                # UP 1 BLOCK
                neighbours.add(grid[block_index - 3][field_index + 3 * i])
                # DOWN 1 BLOCK
                neighbours.add(grid[block_index + 3][field_index + 3 * i])

            elif block_index in (0, 1, 2):
                # DOWN 1 BLOCK
                neighbours.add(grid[block_index + 3][field_index + 3 * i])
                # DOWN 2 BLOCKS
                neighbours.add(grid[block_index + 6][field_index + 3 * i])

            return neighbours

        for block_index, block in enumerate(grid):
            # Block indices range from 0 to 8. 0 is top left, 8 is bottom right.
            for field_index, field in enumerate(block):
                # Field indices range from 0 to 8, 0 is top left, 8 is bottom right.
                neighbours = set()

                for neighbour_index in range(len(block)):
                    if neighbour_index != field_index:
                        neighbours.add(block[neighbour_index])

                # Left & Right; Row

                if field_index in (0, 3, 6):
                    for offset in range(3):
                        neighbours.update(add_row_neighbours(grid, block_index, field_index, neighbours, offset))

                elif field_index in (1, 4, 7):
                    for offset in range(-1, 2):
                        neighbours.update(add_row_neighbours(grid, block_index, field_index, neighbours, offset))

                elif field_index in (2, 5, 8):
                    for offset in range(-2, 1):
                        neighbours.update(add_row_neighbours(grid, block_index, field_index, neighbours, offset))

                # Above & Below; Column

                if field_index in (0, 1, 2):
                    for offset in range(3):
                        neighbours.update(add_column_neighbours(grid, block_index, field_index, neighbours, offset))

                elif field_index in (3, 4, 5):
                    for offset in range(-1, 2):
                        neighbours.update(add_column_neighbours(grid, block_index, field_index, neighbours, offset))

                elif field_index in (6, 7, 8):
                    for offset in range(-2, 1):
                        neighbours.update(add_column_neighbours(grid, block_index, field_index, neighbours, offset))

                field.set_neighbours(list(neighbours))

    @staticmethod
    def add_neighbours2(grid):
        """
        Add a list of neighbors to each field in the grid.
        @param grid: 9x9 list of Fields
        """
        for row in range(9):
            for col in range(9):
                neighbours = set()

                # Add neighbours in the same row
                for c in range(9):
                    if c != col:
                        neighbours.add(grid[row][c])

                # Add neighbours in the same column
                for r in range(9):
                    if r != row:
                        neighbours.add(grid[r][col])

                # Add neighbours in the same 3x3 block
                start_row, start_col = 3 * (row // 3), 3 * (col // 3)
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        if (r, c) != (row, col):
                            neighbours.add(grid[r][c])

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
