"""Assignment 2 - Blocky

=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from typing import Optional, Tuple, List
import random
import math
from renderer import COLOUR_LIST, TEMPTING_TURQUOISE, BLACK, colour_name


HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
FRAME_COLOUR = BLACK


class Block:
    """A square block in the Blocky game.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    colour:
        If this block is not subdivided, <colour> stores its colour.
        Otherwise, <colour> is None and this block's sublocks store their
        individual colours.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's colour is None
    - If this Block has no children,
        - its colour is not None
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: List['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 colour: Optional[Tuple[int, int, int]] = None,
                 children: Optional[List['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and colour,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
        # level
        self.level = level
        # colour
        self.colour = colour
        # children
        if children is None:
            self.children = []
        else:
            self.children = children
        # position
        self.position = (0, 0)
        self.max_depth = 0
        self.size = 0
        self.highlighted = False
        # parent
        self.parent = None
        if self.children:
            for kid in self.children:
                kid.parent = self

    def rectangles_to_draw(self) -> List[Tuple[Tuple[int, int, int],
                                               Tuple[int, int],
                                               Tuple[int, int],
                                               int]]:
        """Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's colour
            - one rectangle in the FRAME_COLOUR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOUR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the colour of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its colour. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOUR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.
        """
        result = []
        if self.highlighted:
            highlight_rec = \
                (HIGHLIGHT_COLOUR, self.position, (self.size, self.size), 5)
            result.append(highlight_rec)
        if not self.children:
            block_rec = (self.colour, self.position,
                         (self.size, self.size), 0)
            result.append(block_rec)
            frame_rec = (FRAME_COLOUR, self.position, (self.size, self.size), 3)
            result.append(frame_rec)
            return result
        else:
            for kid in self.children:
                result.extend(kid.rectangles_to_draw())
            return result

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        """
        if not self.children:
            return
        elif direction == 1:
            top_right, top_left = self.children[0], self.children[1]
            self.children[0], self.children[3] = self.children[3], top_right
            self.children[1], self.children[2] = self.children[2], top_left
            self.update_block_locations(self.position, self.size)
        elif direction == 0:
            top_right, low_right = self.children[0], self.children[3]
            self.children[0], self.children[1] = self.children[1], top_right
            self.children[3], self.children[2] = self.children[2], low_right
            self.update_block_locations(self.position, self.size)

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.
        """
        if self.children:
            top_left, top_right = self.children[1], self.children[0]
            low_left, low_right = self.children[2], self.children[3]
            if direction == 1:
                self.children[3], self.children[0] = top_right, top_left
                self.children[1], self.children[2] = low_left, low_right
                for kid in self.children:
                    kid.rotate(direction)
                self.update_block_locations(self.position, self.size)
            elif direction == 3:
                self.children[0], self.children[3] = low_right, low_left
                self.children[2], self.children[1] = top_left, top_right
                for kid in self.children:
                    kid.rotate(direction)
                self.update_block_locations(self.position, self.size)

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed,
        randomly generating four new child Blocks for it.
        (If it already had child Blocks, discard them.)

        Ensure that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it
        is not already at the level of the maximum depth.

        Return True if this Block was smashed and False otherwise.
        """
        if 0 < self.level < self.max_depth:
            self.colour = None
            self.children = []
            for _ in range(4):
                random_int = random.randint(0, 3)
                kid = Block(self.level + 1, COLOUR_LIST[random_int], None)
                self.children.append(kid)
                kid.parent = self
                kid.max_depth = self.max_depth
            self.update_block_locations(self.position, self.size)
            return True
        else:
            return False

    def update_block_locations(self, top_left: Tuple[int, int],
                               size: int) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        <top_left> is the (x, y) coordinates of the top left corner of
        this Block.  <size> is the height and width of this Block.
        """
        self.position = top_left
        self.size = size
        if self.children != []:
            self.children[0].position = \
                (top_left[0] + round(size / 2.0), top_left[1])
            self.children[1].position = top_left
            self.children[2].position = \
                (top_left[0], top_left[1] + round(size / 2.0))
            self.children[3].position = (top_left[0] + round(size / 2.0),
                                         top_left[1] + round(size / 2.0))
            for kid in self.children:
                kid.size = round(self.size / 2.0)
                kid.update_block_locations(kid.position, kid.size)

    def get_selected_block(self, location: Tuple[int, int], level: int) \
            -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        <location> is the (x, y) coordinates of the location on the window
        whose corresponding block is to be returned.
        <level> is the level of the desired Block.  Note that
        if a Block includes the location (x, y), and that Block is subdivided,
        then one of its four children will contain the location (x, y) also;
        this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth
        """
        # Base Case: no children, just a single block
        # self.level == 0 <= level
        if not self.children:
            return self
        if self.level == level:
            return self
        # Induction Step:
        selected = self.children[1]
        for kid in self.children:
            # if location is iincluded in child block update new_child
            x_range = [kid.position[0], kid.position[0] + kid.size]
            y_range = [kid.position[1], kid.position[1] + kid.size]
            if x_range[0] <= location[0] <= x_range[1] and y_range[0] <= \
                    location[1] <= y_range[1]:
                selected = kid
                if level == selected.level or selected.level == self.max_depth:
                    return selected
                else:
                    return selected.get_selected_block(location, level)
        return selected

    def flatten(self) -> List[List[Tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Return a list of lists L, where, for 0 <= i, j <
        2^{self.max_depth - self.level}
            - L[i] represents column i and
            - L[i][j] represents the unit cell at column i and row j.
        Each unit cell is represented by 3 ints for the colour
        of the block at the cell location[i][j]

        L[0][0] represents the unit cell in the upper left corner of the Block.

        """
        result = []
        dimension = 2 ** (self.max_depth - self.level)
        # Base Case： no children
        if not self.children:
            temp_lst = [self.colour] * int(dimension)
            result = [temp_lst] * int(dimension)
            return result
        else:
            children = [self.children[i].flatten() for i in range(4)]
            for i in range(int(dimension / 2)):
                result.append(children[1][i] + children[2][i])
            for i in range(int(dimension / 2)):
                result.append(children[0][i] + children[3][i])
            return result


def random_init(level: int, max_depth: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributes
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
        level <= max_depth
    """
    # If this Block is not already at the maximum allowed depth, it can
    # be subdivided. Use a random number to decide whether or not to
    # subdivide it further.
    # Use function random.random to generate a random number in the
    # interval [0, 1).
    # Subdivide if the random number is less than math.exp(-0.25 * level) ,
    #  where level is the level of the Block within the tree.

    colour = None
    children = []
    result = Block(level, colour, children)
    result.max_depth = max_depth
    # If a Block is not going to be subdivided, use a random integer
    # to pick a colour for it from the list of colours in renderer.COLOUR_LIST .
    if result.level == max_depth:
        random_int = random.randint(0, 3)
        result.colour = COLOUR_LIST[random_int]
        return result
    else:
        random_num = random.random()
        decision = (random_num < math.exp(-0.25 * result.level))
        if not decision:
            random_int = random.randint(0, 3)
            result.colour = COLOUR_LIST[random_int]
            return result
        else:
            level += 1
            result.children = []
            for _ in range(4):
                kid = random_init(level, max_depth)
                result.children.append(kid)
                kid.parent = result
            return result


def attributes_str(b: Block, verbose) -> str:
    """Return a str that is a concise representation of the attributes of <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Note: These are attributes that every Block has.
    """
    answer = f'pos={b.position}, size={b.size}, level={b.level}, '
    if verbose:
        answer += f'highlighted={b.highlighted}, max_depth={b.max_depth}'
    return answer


def print_block(b: Block, verbose=False) -> None:
    """Print a text representation of Block <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    print_block_indented(b, 0, verbose)


def print_block_indented(b: Block, indent: int, verbose) -> None:
    """Print a text representation of Block <b>, indented <indent> steps.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    if len(b.children) == 0:
        # b a leaf.  Print its colour and other attributes
        print(f'{"  " * indent}{colour_name(b.colour)}: ' +
              f'{attributes_str(b, verbose)}')
    else:
        # b is not a leaf, so it doesn't have a colour.  Print its
        # other attributes.  Then print its children.
        print(f'{"  " * indent}{attributes_str(b, verbose)}')
        for kid in b.children:
            print_block_indented(kid, indent + 1, verbose)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['print_block_indented'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer', 'math'
        ],
        'max-attributes': 15
    })

    # This tiny tree with one node will have no children, highlighted False,
    # and will have the provided values for level and colour; the initializer
    # sets all else (position, size, and max_depth) to 0.
    b0 = Block(0, COLOUR_LIST[2])
    # Now we update position and size throughout the tree.
    b0.update_block_locations((0, 0), 750)
    print("=== tiny tree ===")
    # We have not set max_depth to anything meaningful, so it still has the
    # value given by the initializer (0 and False).
    print_block(b0, True)

    b1 = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, COLOUR_LIST[2]),
        Block(1, children=[
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[1])
        ])
    ])
    b1.update_block_locations((0, 0), 750)
    print("\n=== handmade tree ===")
    # Similarly, max_depth is still 0 in this tree.  This violates the
    # representation invariants of the class, so we shouldn't use such a
    # tree in our real code, but we can use it to see what print_block
    # does with a slightly bigger tree.
    print_block(b1, True)

    # Now let's make a random tree.
    # random_init has the job of setting all attributes except position and
    # size, so this time max_depth is set throughout the tree to the provided
    # value (3 in this case).
    b2 = random_init(0, 3)
    # Now we update position and size throughout the tree.
    b2.update_block_locations((0, 0), 750)
    print("\n=== random tree ===")
    # All attributes should have sensible values when we print this tree.
    print_block(b2, True)
