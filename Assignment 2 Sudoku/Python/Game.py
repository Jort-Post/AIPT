from queue import PriorityQueue


class Game:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def show_sudoku(self):
        print(self.sudoku)

    def solve(self) -> bool:
        """
        Implementation of the AC-3 algorithm
        @return: true if the constraints can be satisfied, false otherwise
        """
        # How to define constraints?
        # The queue needs to be filled with all arcs3
        # TODO: implement AC-3

        # CSP is a tuple of fields, field domains and all constraints between the fields

        # Self.board = grid



        # Loading Arcs
        # Loop over game board to get the grid with fields, then loop over the neighbours of each field to set a constraint as a tuple; (field, neighbour)
        queue = PriorityQueue()



        while not queue.empty():
            current = queue.get()


        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function

        # Check all columns and rows of 3x3 squares
        # Check all Columns of 9x9 square
        # Check all Rows of 9x9 Square
        return False
