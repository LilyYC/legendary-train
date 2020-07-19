"""Assignment 2 - Blocky
This file contains the player class hierarchy.
"""

import random
from typing import Optional
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1
    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.
        Then identify what it is that <event> indicates needs to happen to
        <board> and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1
                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


class RandomPlayer(Player):
    """ A random player.

    A Random Player can do unlimited number of smashes.
    But forfeit the turn if a Random Player randomly chooses to smash the
    top-level block or a unit cell. And such action is not permitted to perform.
    """
    # === Private Attributes ===
    # _selected_block:
    #        The block a computer player randomly picked.
    _selected_block: Optional[Block]

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self._selected_block = None
        self._level = 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        # 1. Randomly choose a block.
        level = random.randint(0, board.max_depth)
        block = board.get_selected_block((random.randint(0, 750),
                                          random.randint(0, 750)), level)
        # 2. Highlight the chosen block and draw the board.
        self._selected_block = block
        self._selected_block.highlighted = True
        self.renderer.draw(board, self.id)
        # 3. Call pygame.time.wait(TIME_DELAY) to introduce a delay
        # so that the user can see what is happening.
        pygame.time.wait(TIME_DELAY)
        # 4.1 Randomly choose one of the 5 possible types of action
        act = random.randint(0, 4)
        # 4.2 do it on the chosen block.
        if act == 0:
            self._selected_block.swap(0)
        if act == 1:
            self._selected_block.swap(1)
        if act == 2:
            self._selected_block.rotate(3)
        if act == 3:
            self._selected_block.rotate(1)
        if act == 4:
            if 0 < self._selected_block.level < board.max_depth:
                if self._selected_block.smash():
                    pass
        # 5. Un-highlight the chosen block and draw the board again.
        self._selected_block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0


class SmartPlayer(Player):
    """ A smart player.

    A SmartPlayer is not allowed to do smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes == 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that a SmartPlayer currently selects.
    # _difficulty_level:
    #     The difficulty level is an integer >= 0, and dictates how many
    #     possible moves it compares when choosing a move to make.
    # _possible_moves:
    #     The number of possible_moves it compares when choosing a move.
    # == Representation Invariants concerning the private attributes ==
    #     _difficulty_level >= 0
    difficulty_level: int
    _possible_moves: int
    _selected_block: Optional['Block']

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 _difficulty_level: int) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self._selected_block = None
        self._possible_moves = 0
        self.difficulty_level = _difficulty_level
        if _difficulty_level == 0:
            self._possible_moves = 5
        elif _difficulty_level == 1:
            self._possible_moves = 10
        elif _difficulty_level == 2:
            self._possible_moves = 25
        elif _difficulty_level == 3:
            self._possible_moves = 50
        elif _difficulty_level == 4:
            self._possible_moves = 100
        else:
            self._possible_moves = 150

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.

        It will move a SmartPlayer from the best result one step further based
        on numbers of possible moves a Smartplayer can compare to based on
        the difficulty level.
        """
        temp_score = 0
        max_so_far_block = None
        max_so_far_move = 0
        # 1. Assess the right number of possible moves and pick the
        # best one among them.
        for _ in range(self._possible_moves):
            block = board.get_selected_block((random.randint(0, 750),
                                              random.randint(0, 750)),
                                             random.randint(0, board.max_depth))
            action = random.randint(0, 3)
            if action <= 1:
                block.swap(action)
                score = self.goal.score(board)
                if score >= temp_score:
                    temp_score = score
                    max_so_far_block = block
                    max_so_far_move = action
                block.swap(action)
            elif action == 3:
                block.rotate(3)
                score = self.goal.score(board)
                if score >= temp_score:
                    temp_score = score
                    max_so_far_block = block
                    max_so_far_move = action
                block.rotate(1)
            else:
                block.rotate(1)
                score = self.goal.score(board)
                if score >= temp_score:
                    temp_score = score
                    max_so_far_block = block
                    max_so_far_move = action
                block.rotate(3)
        # 2. Highlight the block involved in the chosen move, and draw the board
        self._selected_block = max_so_far_block
        self._selected_block.highlighted = True
        self.renderer.draw(board, self.id)
        # 3. Call pygame.time.wait(TIME_DELAY) to introduce a delay
        # so that the user can see what is happening.
        pygame.time.wait(TIME_DELAY)

        # 4 DO the chosen move.
        if max_so_far_move <= 2:
            max_so_far_block.swap(max_so_far_move)
        if max_so_far_block == 3:
            max_so_far_block.rotate(3)
        else:
            max_so_far_block.rotate(1)
        # 5. Un-highlight the block involved in the chosen move, and
        # draw the board again.
        self._selected_block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
