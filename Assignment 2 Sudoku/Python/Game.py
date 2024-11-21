from queue import PriorityQueue
import heapq
class Game:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.constraints_revised = 0

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
            # List of 9x9 fields
            grid = self.sudoku.get_board()
            # Set of all arcs
            arcs = set()
            # queue of all arcs
            priority_queue = []

            # Loop over all rows in the grid
            for row in range(9):
                # Loop over all columns in a row
                for col in range(9):
                    # Continue iff other fields have influence over the final value of the current field
                    if not grid[row][col].is_finalized():
                        # Get all constraining neighbours of the current field
                        neighbours = grid[row][col].get_neighbours()
                        # Loop over all constraining neighbours
                        for neighbour in neighbours:
                            # Add the arc between two fields to the priority queue.
                            # The priority is based on one of the ids of the Fields since the order doesn't yet matter.

                            # There are two ids to make sure the heapq will never compare
                            # two Fields in case of a tie between priorities.
                            heapq.heappush(priority_queue, (id(neighbour), id(grid[row][col]), (grid[row][col], neighbour)))
                            # The arc is added to an unresolved_arcs set which will be used in AC3
                            arcs.add((grid[row][col], neighbour))

            return priority_queue, arcs
        def revise(field1, field2):
            """
            Helper function to revise a constraint
            :param field1:
            :param field2:
            :return: modified
            """
            # Domain of field1 is not modified by default
            modified = False
            self.constraints_revised += 1

            # Make a copy of the domain of field1 to ensure the function keeps looping over the same domain
            field1_domain = field1.get_domain().copy()
            # Field2 can have a non-zero value from the start (from the template), then it's domain is an empty list: []
            # to prevent looping over an empty list, make a list of the single value if field2 is finalized:
            field2_domain = field2.get_domain().copy() if not field2.is_finalized() else [field2.get_value()]

            # Loop over all possible values x_m in domain field1:
            for x_m in field1_domain:
                # Check if a value x_m violates the constraint with all values x_n from the domain of field2
                if all(x_m == x_n for x_n in field2_domain):
                    # If all values violate the constraint, x_m is not a valid final value and is removed
                    field1.remove_from_domain(x_m)
                    self.domains_changed += 1
                    # The domain of field1 has now changed, so modified flips true
                    modified = True

            return modified

        # Loading arcs in queue and unresolved_arcs
        queue, unresolved_arcs = fill_queue()

        # Loop over the queue while it is not empty:
        while queue:
            # Retrieve the arc from the queue without any priorities (the last value of each item in the queue):
            (field1, field2) = heapq.heappop(queue)[-1]
            # This arc will be resolved, so it is removed from the set:
            unresolved_arcs.remove((field1, field2))

            # Revise the arc between field1 and field2 and continue if the domain of field1 is modified:
            if revise(field1, field2):

                # If the domain of field1 is zero, there is no legal value field1 can take,
                # and therefore the sudoku cannot be solved
                if field1.get_domain_size() == 0:
                    return False

                # All neighbours of field1 need to be updated since the domain of field1 has changed

                # Loop over all neighbours of field1 except for neighbour field2:
                for neighbour in field1.get_other_neighbours(field2):
                    # if the arc from a neighbour of field1 to field1 is new, add it to the priority queue,
                    # based on a heuristic / priority:
                    if (neighbour, field1) not in unresolved_arcs:
                        # Minimum remaining Values Heuristic:
                        heuristic = neighbour.get_domain_size()

                        # Degree Heuristic:
                        #heuristic = 0
                        #for n in neighbour.get_neighbours():
                           # if not n.is_finalized():
                            #    heuristic += 1

                        # Most arcs to constrained fields Heuristic:
                        #heuristic = 0
                        #for n in neighbour.get_neighbours():
                           #if n.is_finalized():
                               #heuristic += 1


                        # Still include the ids of both fields just in case the heuristic happens to have a tie
                        # with another heuristic of an item in the queue.
                        heapq.heappush(queue, (heuristic, id(field1), id(neighbour), (neighbour, field1)))
                        # Add the new arc to the set of unresolved arcs
                        unresolved_arcs.add((neighbour, field1))

        # If the queue is empty, all constraints are resolved and a solution is found
        return True

    def valid_solution(self) -> bool:
        """
        Checks the validity of a sudoku solution
        @return: true if the sudoku solution is correct
        """
        # TODO: implement valid_solution function
        # Print the board after AC3 solved the sudoku
        self.show_sudoku()
        # Get the list of 9x9 fields
        grid = self.sudoku.get_board()

        print(f'Number of arcs revised: {self.constraints_revised}')

        # Loop over all rows in the sudoku
        for row in range(9):
            # Loop over all columns in a row
            for col in range(9):
                # Check if this field has a non-zero value, return false otherwise
                if not grid[row][col].is_finalized():
                    return False
                # Check if all neighbouring fields have a different value than the current field, return false otherwise
                elif any(grid[row][col] == neighbour.get_value() for neighbour in grid[row][col].get_neighbours()):
                    return False
        # If all values are non-zero and unique in comparison to their constraining neighbours values', the solution is valid
        return True
