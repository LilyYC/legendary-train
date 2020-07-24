""" Binary Search Trees Practice

"""
from typing import List, Optional, Tuple


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every node, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[object]
    # The left subtree, or None if the tree is empty
    _left: Optional['BinarySearchTree']
    # The right subtree, or None if the tree is empty
    _right: Optional['BinarySearchTree']

    # === Representation Invariants ===
    #  - If _root is None, then so are _left and _right.
    #    This represents an empty BST.
    #  - If _root is not None, then _left and _right are BinarySearchTrees.
    #  - (BST Property) All items in _left are <= _root,
    #    and all items in _right are >= _root.

    def __init__(self, root: Optional[object]) -> None:
        """Initialize a new BST with the given root value and no children.

        If <root> is None, make an empty tree, with subtrees that are None.
        If <root> is not None, make a tree with subtrees are empty trees.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    def __contains__(self, item: object) -> bool:
        """Return True if <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        else:
            return max(self._left.height(), self._right.height()) + 1

    def insert(self, item: object) -> None:
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other nodes.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        if self.is_empty():
            # Make new leaf node.
            # Note that self._left and self._right cannot be None if the
            # tree is non-empty! (This is one of our invariants.)
            self._root = item
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)
        elif item <= self._root:
            self._left.insert(item)
        else:
            self._right.insert(item)

    def num_less_than(self, item: object) -> int:
        """Return the number of items in this BST that are less than <item>.
        >>> bst1 = BinarySearchTree(None)
        >>> bst1.num_less_than(10)
        0
        >>> bst2 = BinarySearchTree(38)
        >>> bst2.num_less_than(1)
        0
        >>> bst2.num_less_than(40)
        1
        >>> b3 = BinarySearchTree(11)
        >>> b4 = BinarySearchTree(8)
        >>> b5 = BinarySearchTree(25)
        >>> b3._left = b4
        >>> b3._right = b5
        >>> bst2._left = b3
        >>> bst2.num_less_than(24)
        2
        """
        result = 0
        if self.is_empty():
            return result
        elif self._root < item:
            result += 1 + self._left.num_less_than(item) + self._right.\
                num_less_than(item)
            return result
        else:
            result += self._left.num_less_than(item)
            return result

    def items_at_depth(self, d: int) -> list:
        """Return a sorted list of all items in this BST at depth <d>.

        Precondition: d >= 1.

        Reminder: you should not have to use the built-in 'sort' method
        or do any sorting yourself.
        >>> bst1 = BinarySearchTree(90)
        >>> bst1._left = BinarySearchTree(20)
        >>> bst1._right = BinarySearchTree(10)
        >>> bst1.items_at_depth(2)
        [20, 10]
        >>> b1 = BinarySearchTree(25)
        >>> b1._left = BinarySearchTree(11)
        >>> b1._right = BinarySearchTree(30)
        >>> bst2 = BinarySearchTree(10)
        >>> bst2._left = BinarySearchTree(None)
        >>> bst2._right = b1
        >>> bst2.items_at_depth(2)
        [25]
        >>> bst2.height()
        3
        >>> bst2.items_at_depth(3)
        [11, 30]

        """
        result = []
        if self.is_empty() or d > self.height():
            return result
        elif d == 1:
            result.append(self._root)
            return result
        else:
            result.extend(self._left.items_at_depth(d - 1))
            result.extend(self._right.items_at_depth(d - 1))
            return result

    def levels(self) -> List[Tuple[int, list]]:
        """Return a list of items in the tree, separated by level.

        You may wish to use 'items_at_depth' as a helper method,
        but this also makes your code less efficient. Try doing
        this method twice, once with 'items_at_depth', and once
        without it!

        >>> b6 = BinarySearchTree(100)
        >>> b5 = BinarySearchTree(110)
        >>> b4 = BinarySearchTree(None)
        >>> b3 = BinarySearchTree(75)
        >>> b2 = BinarySearchTree(20)
        >>> b1 = BinarySearchTree(50)
        >>> bst = BinarySearchTree(90)
        >>> bst._left = b1
        >>> bst._right = b6
        >>> b1._left = b2
        >>> b1._right = b3
        >>> b6._left = b4
        >>> b6._right = b5
        >>> bst.levels()
        [(1, [90]), (2, [50, 100]), (3, [20, 75, 110])]
        >>> b6.levels()
        [(1, [100]), (2, [110])]

        """
        # result = []
        # if self.is_empty():
        #     return result
        # elif self.height() == 1:
        #     result.append((1, [self._root]))
        # else:
        #     for d in range(1, self.height() + 1):
        #         level = (d, self.items_at_depth(d))
        #         result.append(level)
        # return result

        # Another approach with no helper
        total_level = []
        if self.is_empty():
            return total_level
        else:
            total_level.append((1, [self._root]))
            left, right = self._left.levels(), self._right.levels()
            l_l = 0
            r_l = 0
            while l_l < len(left) and r_l < len(right):
                total_level.append((l_l + 2, left[l_l][1] + right[r_l][1]))
                l_l += 1
                r_l += 1
            while l_l < len(left):
                total_level.append((l_l + 2, left[l_l][1]))
                l_l += 1
            while r_l < len(right):
                total_level.append((r_l + 2, right[r_l][1]))
                r_l += 1
            return total_level

if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
