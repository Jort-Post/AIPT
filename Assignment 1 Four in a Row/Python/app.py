from heuristics import Heuristic, SimpleHeuristic
from players import PlayerController, HumanPlayer, MinMaxPlayer, AlphaBetaPlayer, MonteCarloPlayer
from board import Board
from typing import List
import numpy as np
from numba import jit, float32, int32


def start_game(game_n: int, board: Board, players: List[PlayerController]) -> int:
    """Starting a game and handling the game logic

    Args:
        game_n (int): n in a row required to win
        board (Board): board to play on
        players (List[PlayerController]): players of the game

    Returns:
        int: id of the winning player, or -1 if the game ends in a draw
    """
    print('Start game!')
    current_player_index: int = 0 # index of the current player in the players list
    winner: int = 0

    # Main game loop
    while winner == 0:
        current_player: PlayerController = players[current_player_index]
        move: int = current_player.make_move(board)
        move_count = 0

        while not board.play(move, current_player.player_id):
            move = current_player.make_move(board)
            move_count += 1

        current_player_index = 1 - current_player_index
        winner = winning(board.get_board_state(), game_n)

    # Printing out winner, final board and number of evaluations after the game 
    print(board)

    if winner < 0:
        print('Game is a draw!')
    else:
        print(f'Player {current_player} won!')

    for p in players:
        print(f'Player {p} evaluated a boardstate {p.get_eval_count()} times!')
        print(f'Player {p} visited a total of {p.get_visited_nodes()} nodes!')
        print(f'Player {p} played {move_count} moves')

    return winner


@jit(nopython=True, cache=True)
def winning(state: np.ndarray, game_n: int) -> int:
    """Determines whether a player has won, and if so, which one

    Args:
        state (np.ndarray): the board to check
        game_n (int): n in a row required to win

    Returns:
        int: 1 or 2 if the respective player won, -1 if the game is a draw, 0 otherwise
    """
    player: int
    counter: int

    # Vertical check
    for col in state:
        counter = 0
        player = -1
        for field in col[::-1]:
            if field == 0:
                break
            elif field == player:
                counter += 1
                if counter >= game_n:
                    return player
            else:
                counter = 1 
                player = field
            
    # Horizontal check
    for row in state.T:
        counter = 0
        player = -1
        for field in row:
            if field == 0:
                counter = 0
                player = -1
            elif field == player:
                counter += 1
                if counter >= game_n:
                    return player
            else:
                counter = 1
                player = field

    # Ascending diagonal check
    for i, col in enumerate(state[:- game_n + 1]):
        for j, field in enumerate(col[game_n - 1:]):
            if field == 0:
                continue
            player = field
            for x in range(game_n):
                if state[i + x, j + game_n - 1 - x] != player:
                    player = -1
                    break
            if player != -1:
                return player
            
    # Descending diagonal check
    for i, col in enumerate(state[game_n - 1:]):
        for j, field in enumerate(col[game_n - 1:]):
            if field == 0:
                continue
            player = field
            for x in range(game_n):
                if state[i + game_n - 1 - x, j + game_n - 1 - x] != player:
                    player = -1
                    break
            if player != -1:
                return player
        
    # Check for a draw
    if np.all(state[:, 0]):
        return -1 # The board is full, game is a draw

    return 0 # Game is not over 
    

def get_players(game_n: int) -> List[PlayerController]:
    """Gets the two players

    Args:
        game_n (int): n in a row required to win

    Raises:
        AssertionError: if the players are incorrectly initialised

    Returns:
        List[PlayerController]: list with two players
    """
    heuristic1: Heuristic = SimpleHeuristic(game_n)
    heuristic2: Heuristic = SimpleHeuristic(game_n)

    human1: PlayerController = HumanPlayer(1, game_n, heuristic1)
    human2: PlayerController = HumanPlayer(2, game_n, heuristic2)

    bot1: PlayerController = MinMaxPlayer(1, game_n, 5, heuristic1)
    bot2: PlayerController = AlphaBetaPlayer(2, game_n, 5, heuristic2)


    # TODO: Implement other PlayerControllers (MinMaxPlayer and AlphaBetaPlayer)

    players: List[PlayerController] = [bot1, bot2]

    assert players[0].player_id in {1, 2}, 'The player_id of the first player must be either 1 or 2'
    assert players[1].player_id in {1, 2}, 'The player_id of the second player must be either 1 or 2'
    assert players[0].player_id != players[1].player_id, 'The players must have an unique player_id'
    assert players[0].heuristic is not players[1].heuristic, 'The players must have an unique heuristic'
    assert len(players) == 2, 'Not the correct amount of players'

    return players


if __name__ == '__main__':
    game_n: int = 5 # n in a row required to win
    width: int = 7  # width of the board
    height: int = 6 # height of the board

    # During the experiments you only change ONE variable
    # Test Baseline: game_n = 4, width = 7, height = 6, depth = 5
    # Then adjust ONE of the following:
    # Experiment with: game_n = 3, 4 and 5
    # Experiment with: depth = 3,5,8 and 10 if possible
    # Experiment with board sizes: 6x7, 12x14 and 3x4
    # Experiment with a custom heuristic
    # Switch player IDs

    # Check whether the game_n is possible
    assert 1 < game_n <= min(width, height), 'game_n is not possible'

    board: Board = Board(width, height)
    start_game(game_n, board, get_players(game_n))
    