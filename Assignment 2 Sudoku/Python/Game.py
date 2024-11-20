from queue import PriorityQueue
import heapq
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

        def fill_queue(priority_queue):
            """
            Helper function to fill the queue with all arcs
            :param queue:
            :return:
            """
            grid = self.sudoku.get_board()
            for block in grid:
                for field in block:
                    if not field.is_finalized():
                        neighbours = field.get_neighbours()
                        for neighbour in neighbours:
                            if neighbour.is_finalized():
                                priority = field.get_domain_size()
                                heapq.heappush(priority_queue, (priority, (field, neighbour)))
            return priority_queue

        def revise(field1, field2):
            """
            Helper function to revise constraints
            :param field1:
            :param field2:
            :return: modified
            """
            modified = False
            field1_domain = field1.get_domain().copy()

            if field1.is_finalized():
                return modified

            else:
                # HERE IS THE PROBLEM!!!!!:
                field2_domain = field2.get_domain().copy()
                for x_m in field1_domain:
                    if all(x_m == x_n for x_n in field2_domain):
                        field1.remove_from_domain(x_m)
                        modified = True

            return modified


        # Loading Arcs
        empty_queue = []
        queue = fill_queue(empty_queue)

        while queue:
            _, (field1, field2) = heapq.heappop(queue)

            if revise(field1, field2):
                if field1.get_domain_size() == 0:
                    return False

                for neighbour in field1.get_other_neighbours(field2):
                    if (neighbour, field1) not in queue:
                        priority = neighbour.get_domain_size()
                        heapq.heappush(queue, (priority,(neighbour, field1)))
        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function
        print(self.sudoku)
        grid = self.sudoku.get_board()

        for block in self.sudoku.get_board():
            for field in block:
                if not field.is_finalized():
                    return False
        return True