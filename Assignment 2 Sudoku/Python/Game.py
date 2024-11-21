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

        def fill_queue():
            """
            Helper function to fill the queue with all arcs
            :param queue:
            :return:
            """
            grid = self.sudoku.get_board()
            seen_arcs = set()
            priority_queue = []

            for row in range(9):
                for col in range(9):
                    neighbours = grid[row][col].get_neighbours()
                    for neighbour in neighbours:
                        priority = grid[row][col].get_domain_size()
                        priority2 = id(grid[row][col])
                        priority3 = id(neighbour)
                        heapq.heappush(priority_queue, (priority, priority2, priority3, (grid[row][col], neighbour)))
                        seen_arcs.add((grid[row][col], neighbour))

            return priority_queue, seen_arcs
        def revise(field1, field2):
            """
            Helper function to revise constraints
            :param field1:
            :param field2:
            :return: modified
            """
            modified = False

            if field1.is_finalized():
                return modified

            field1_domain = field1.get_domain().copy()
            field2_domain = field2.get_domain().copy() if not field2.is_finalized() else [field2.get_value()]

            for x_m in field1_domain:
                #if all(x_m == x_n for x_n in field2_domain):
                if not any(x_m != x_n for x_n in field2_domain):
                    field1.remove_from_domain(x_m)
                    modified = True

            return modified


        # Loading Arcs
        queue, seen_arcs = fill_queue()

        while queue:
            _, _, _, (field1, field2) = heapq.heappop(queue)

            if revise(field1, field2):
                if field1.get_domain_size() == 0:
                    return False

                for neighbour in field1.get_other_neighbours(field2):
                    priority = neighbour.get_domain_size()
                    if (neighbour, field1) not in seen_arcs:
                        heapq.heappush(queue, (priority, (neighbour, field1)))
        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function
        self.show_sudoku()
        grid = self.sudoku.get_board()

        for block in self.sudoku.get_board():
            for field in block:
                if not field.is_finalized():
                    return False
        return True