from __future__ import annotations
from abc import abstractmethod
import numpy as np
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    from heuristics import Heuristic
    from board import Board


class PlayerController:
    """Abstract class defining a player
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        self.player_id = player_id
        self.game_n = game_n
        self.heuristic = heuristic
        self.visited_nodes: int = 0  # runtime measure

    def get_eval_count(self) -> int:
        """
        Returns:
            int: The amount of times the heuristic was used to evaluate a board state
        """
        return self.heuristic.eval_count

    def get_visited_nodes(self) -> int:
        """
        Returns:
            int: The amount of nodes the algorithm has visited
        """
        return self.visited_nodes

    def __str__(self) -> str:
        """
        Returns:
            str: representation for representing the player on the board
        """
        if self.player_id == 1:
            return 'X'
        return 'O'
        

    @abstractmethod
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        pass


class MinMaxPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth
        self.visited_nodes: int = 0  # runtime measure


    def minimax(self, board: Board, player_id: int, depth: int):
        """ Minimax algorithm
        Args:
            board (Board): the current board
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            depth (int): the max search depth
        Returns:
            int: the best column to play in
        """
        # Add a node to the number of visited every time minimax is called
        self.visited_nodes += 1

        # Base case: if the algorithm reached the maximum depth or a winning state.
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n) > 0:
            # Return the heuristic value of this state (depending on the player)
            return self.heuristic.evaluate_board(3-player_id, board)

        # Maximizing player's turn (player 1)
        elif player_id == 1:
            # Initialize the best value to negative infinity and best move to None
            max_val = -np.inf
            max_move = None

            # Iterate through all possible moves
            for col in range(board.width):
                if board.is_valid(col):
                    # Create a new board state after making this move
                    child_id = 3 - player_id
                    child_board: Board = board.get_new_board(col, child_id)
                    # Recursively evaluate the child state
                    evaluation = self.minimax(child_board, child_id, depth - 1)

                    # Update the best move and max_value if this one is higher than the current one
                    if evaluation > max_val:
                        max_val = evaluation
                        max_move = col
            # Return the best move if at the root / top level, otherwise return the evaluation
            return max_move if depth == self.depth else max_val

        # Minimizing player's turn (player 2)
        else:
            # Initialize the best value to positive infinity and best move to None
            min_val = np.inf
            min_move = None

            # Iterate through all possible moves
            for col in range(board.width):
                if board.is_valid(col):
                    # Create a new board state after making this move
                    child_id = 3 - player_id
                    child_board: Board = board.get_new_board(col, child_id)
                    # Recursively evaluate the child state
                    evaluation = self.minimax(child_board, child_id, depth - 1)

                    # Update the best move and min_value if this one is lower than the current one
                    if evaluation < min_val:
                        min_val = evaluation
                        min_move = col
            # Return the best move if at the root / top level, otherwise return the evaluation
            return min_move if depth == self.depth else min_val

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        # Display current game state and player's turn
        print(f"Player {self.player_id} is making a move")
        print(f"Current board state:\n{board}")

        # Call the minimax algorithm to determine the best move
        best_move = self.minimax(board, self.player_id, self.depth)

        # Display the chosen move and the number of nodes evaluated
        print(f"Player {self.player_id} Chose move: {best_move}")
        print(f"and evaluated {self.visited_nodes} nodes")

        return best_move


class AlphaBetaPlayer(PlayerController):
    """Class for the minmax player using the minmax algorithm with alpha-beta pruning
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            depth (int): the max search depth
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)
        self.depth: int = depth
        self.visited_nodes: int = 0  # runtime measure

    def alpha_beta(self, board: Board, player_id: int, depth: int, alpha: float = -np.inf, beta: float = np.inf):
        """ Minimax algorithm with alpha-beta pruning
                Args:
                    board (Board): the current board
                    player_id (int): id of a player, can take values 1 or 2 (0 = empty)
                    depth (int): the max search depth
                    alpha (float): the best value which the maximizing player (currently) can guarantee at this level
                    beta (float): the best value which the minimizing player (currently) can guarantee at this level
        Returns:
                Returns:
                    int: the best column to play in
                """
        # Add a node to the number of visited every time minimax is called
        self.visited_nodes += 1

        # Base case: if the algorithm reached the maximum depth or a winning state.
        if depth == 0 or self.heuristic.winning(board.get_board_state(), self.game_n) > 0:
            # Return the heuristic value of this state (depending on the player)
            return self.heuristic.evaluate_board(3 - player_id, board)

        # Maximizing player's turn (player 1)
        elif player_id == 1:
            max_val = -np.inf
            max_move = None

            # Iterate through all possible moves
            for col in range(board.width):
                if board.is_valid(col):
                    # Create a new board state after making this move
                    child_id = 3 - player_id
                    child_board: Board = board.get_new_board(col, child_id)
                    # Recursively evaluate the child state
                    evaluation = self.alpha_beta(child_board, child_id, depth - 1, alpha, beta)

                    # Update the best move and max_valuation if this one is higher than the current one
                    if evaluation > max_val:
                        max_val = evaluation
                        max_move = col

                    # Update alpha and perform alpha-beta pruning if possible
                    alpha = alpha if alpha > evaluation else evaluation
                    if alpha >= beta:
                        break
            # Return the best move if at the root / top level, otherwise return the evaluation
            return max_move if depth == self.depth else max_val

        # Minimizing player's turn (player 2)
        else:
            min_val = np.inf
            min_move = None

            # Iterate through all possible moves
            for col in range(board.width):
                if board.is_valid(col):
                    # Create a new board state after making this move
                    child_id = 3 - player_id
                    child_board: Board = board.get_new_board(col, child_id)
                    # Recursively evaluate the child state
                    evaluation = self.alpha_beta(child_board, child_id, depth - 1, alpha, beta)

                    # Update the best move and min_valuation if this one is lower than the current one
                    if evaluation < min_val:
                        min_val = evaluation
                        min_move = col

                    # Update beta and perform alpha-beta pruning if possible
                    beta = beta if beta < evaluation else evaluation
                    if alpha > beta:
                        break

            # Return the best move if at the root / top level, otherwise return the evaluation
            return min_move if depth == self.depth else min_val

    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        # Display current game state and player's turn
        print(f"Player {self.player_id} is making a move")
        print(f"Current board state:\n{board}")

        # Call the minimax algorithm with alpha-beta pruning to determine the best move
        best_move = self.alpha_beta(board, self.player_id, self.depth)

        # Display the chosen move and the number of nodes evaluated
        print(f"Player {self.player_id} Chose move: {best_move}")
        print(f"and evaluated {self.visited_nodes} nodes")

        return best_move


class MonteCarloPlayer(PlayerController):
    def __init__(self, player_id: int, game_n: int, depth: int, heuristic: Heuristic) -> None:
        super().__init__(player_id,game_n,heuristic)
        self.depth: int = depth

    def get_all_moves(self, board: Board):
        moves = []
        for col in range(board.width):
            if board.is_valid(col):
                moves.append(col)
        return moves

    def simulate(self, board: Board, player_id: int):
        while True:
            winner = self.heuristic.winning(board.get_board_state(), self.game_n)
            if winner > 0 or winner == -1:
                return winner

            valid_moves = self.get_all_moves(board)
            move = random.choice(valid_moves)
            board.play(move, player_id)
            player_id = 3 - player_id

    # def backpropagate(self, result: int):

    # def expand(self, board: Board, player_id: int):

    # def uct():

    # def select(self, ):

    # def mcts(self, board: Board, player_id: int, iterations=1000):

        # for _ in range(iterations):






class HumanPlayer(PlayerController):
    """Class for the human player
    Inherits from Playercontroller
    """
    def __init__(self, player_id: int, game_n: int, heuristic: Heuristic) -> None:
        """
        Args:
            player_id (int): id of a player, can take values 1 or 2 (0 = empty)
            game_n (int): n in a row required to win
            heuristic (Heuristic): heuristic used by the player
        """
        super().__init__(player_id, game_n, heuristic)

    
    def make_move(self, board: Board) -> int:
        """Gets the column for the player to play in

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        print(board)

        if self.heuristic is not None:
            print(f'Heuristic {self.heuristic} calculated the best move is:', end=' ')
            print(self.heuristic.get_best_action(self.player_id, board) + 1, end='\n\n')

        col: int = self.ask_input(board)

        print(f'Selected column: {col}')
        return col - 1
    

    def ask_input(self, board: Board) -> int:
        """Gets the input from the user

        Args:
            board (Board): the current board

        Returns:
            int: column to play in
        """
        try:
            col: int = int(input(f'Player {self}\nWhich column would you like to play in?\n'))
            assert 0 < col <= board.width
            assert board.is_valid(col - 1)
            return col
        except ValueError: # If the input can't be converted to an integer
            print('Please enter a number that corresponds to a column.', end='\n\n')
            return self.ask_input(board)
        except AssertionError: # If the input matches a full or non-existing column
            print('Please enter a valid column.\nThis column is either full or doesn\'t exist!', end='\n\n')
            return self.ask_input(board)
        