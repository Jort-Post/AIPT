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
                    if field.is_finalized():
                        continue
                    neighbours = field.get_neighbours()
                    for neighbour in neighbours:
                        priority = field.get_domain_size()
                        # Problem: HeapQ compares second element if the first element is a tie with another value
                        # Since all our values have the same domain size, this will always happen.
                        priority_queue.append((field, neighbour))
                        #heapq.heappush(priority_queue, (priority, (field,neighbour)))
                        #priority_queue.put((priority, (field,neighbour)))
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

            if field2.is_finalized():
                field2_domain = [field2.get_value()]
            else:
                field2_domain = field2.get_domain().copy()

            for x_m in field1_domain:
                constraints_violated = 0
                for x_n in field2_domain:
                    if x_m == x_n:
                        constraints_violated += 1
                if constraints_violated == len(field2_domain):
                    field1.remove_from_domain(x_m)
                    modified = True

            return modified

        # Loading Arcs
        empty_queue = []
        queue = fill_queue(empty_queue)
        print(queue)

        while queue:
            #_, (field1, field2) = heapq.heappop(queue)
            field1, field2 = queue.pop(0)

            if revise(field1, field2):
                if field1.get_domain_size() == 0:
                    return False

                for neighbour in field1.get_other_neighbours(field2):
                    #if neighbour != field1:
                    if (neighbour, field1) not in queue:
                        #priority = neighbour.get_domain_size()
                        #heapq.heappush(queue, (priority,(neighbour,field1)))
                        #queue.put((priority, (neighbour, field1)))
                        queue.append((neighbour, field1))
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

        for block in self.sudoku.get_board():
            for field in block:
                for neighbour in field.get_neighbours():
                    if field.get_value() == neighbour.get_value():
                        return False
        return True
