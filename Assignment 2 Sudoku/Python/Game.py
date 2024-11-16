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
        # TODO: implement AC-3

        def fill_queue(queue):
            """
            Helper function to fill the queue with all arcs
            :param queue:
            :return:
            """
            grid = self.sudoku.get_board()
            for block in grid:
                for field in block:
                    neighbours = field.get_neigbours()
                    for neighbour in neighbours:
                        if field.is_finalized() and neighbour.is_finalized():
                            continue
                        else:
                            queue.put((field, neighbour))
            return queue

        def revise(field1, field2):




        # Loading Arcs
        queue = fill_queue(PriorityQueue())

        while not queue.empty():
            field1, field2 = queue.get()

            if field1.get_domain_size() == 0:
                return False





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
