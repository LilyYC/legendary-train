"""Assignment 2 - Blocky
=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        score = 0
        visited = []
        flatten_board = board.flatten()
        for _ in range(len(flatten_board[0])):
            visited.append([-1] * len(flatten_board[0]))
        for i in range(len(flatten_board[0])):
            for j in range(len(flatten_board[0])):
                curr_max = self._undiscovered_blob_size((i, j),
                                                        flatten_board, visited)
                if curr_max > score:
                    score = curr_max
        return score

    def description(self) -> str:
        """Return a description of this goal.
        """
        return "Create the largest connected blob of target colour."

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        current_blob = 0
        # If <pos> is out of bounds for <board>, return 0.
        x, y = pos[0], pos[1]
        if 0 <= x <= len(board[0]) - 1 and 0 <= y <= len(board[0]) - 1 and \
           visited[x][y] == -1:
            # print(pos)
            # print(visited)
            if board[x][y] == self.colour:
                current_blob += 1
                visited[x][y] = 1
                potential_positions = [(x + 1, y), (x, y + 1)]
                for potential_cell in potential_positions:
                    current_blob += self._undiscovered_blob_size(
                        (x + 1, y), board, visited)
                return current_blob
            else:
                # only when the cell's colour is visited and not target colour
                # turn the index on visited to zero
                visited[x][y] = 0
                return 0
        else:
            return 0


class PerimeterGoal(Goal):
    """A goal to create the most number of unit cells of target colour that
       are on the perimeter.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.

    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        Each block on the side counts one, on the corner counts two.

        The score is always greater than or equal to 0.
        """
        score = 0
        flat_board = board.flatten()
        board_dimension = len(flat_board[0])
        for i in range(board_dimension):  # 0, 1, ..., board_dimension - 1
            if flat_board[0][i] == self.colour:
                score += 1
            if flat_board[board_dimension - 1][i] == self.colour:
                score += 1
        for j in range(board_dimension):
            if flat_board[j][0] == self.colour:
                score += 1
            if flat_board[j][board_dimension - 1] == self.colour:
                score += 1
        return score

    def description(self):
        """Return a description of this goal.
        """
        return "create maximum unit cells of target colour on the perimeter."


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
