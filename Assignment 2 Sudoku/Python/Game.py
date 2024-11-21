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
                    if not grid[row][col].is_finalized():
                        neighbours = grid[row][col].get_neighbours()
                        for neighbour in neighbours:
                            if (grid[row][col], neighbour) not in seen_arcs:
                                priority2 = id(grid[row][col])
                                priority1 = id(neighbour)
                                heapq.heappush(priority_queue, (priority1, priority2, (grid[row][col], neighbour)))
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

            field1_domain = field1.get_domain().copy()
            field2_domain = field2.get_domain().copy() if not field2.is_finalized() else [field2.get_value()]

            for x_m in field1_domain:
                if all(x_m == x_n for x_n in field2_domain):
                    field1.remove_from_domain(x_m)
                    modified = True

            return modified


        # Loading Arcs
        queue, seen_arcs = fill_queue()

        while queue:
            (field1,field2) = heapq.heappop(queue)[-1]
            seen_arcs.remove((field1, field2))

            if revise(field1, field2):
                if field1.get_domain_size() == 0:
                    return False

                for neighbour in field1.get_other_neighbours(field2):
                    # Minimum remaining Values Heuristic:
                    #heuristic = neighbour.get_domain_size()

                    # Degree Heuristic:
                    heuristic = 0
                    for n in neighbour.get_neighbours():
                        if not n.is_finalized():
                            heuristic += 1

                    # Least constraining Heuristic:

                    if (neighbour, field1) not in seen_arcs:
                        heapq.heappush(queue, (heuristic, id(neighbour), id(field1), (neighbour, field1)))
                        seen_arcs.add((neighbour, field1))
        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function
        self.show_sudoku()
        grid = self.sudoku.get_board()

        for row in range(9):
            for col in range(9):
                if not grid[row][col].is_finalized():
                    return False
                elif any(grid[row][col] == neighbour.get_value() for neighbour in grid[row][col].get_neighbours()):
                    return False
        return True