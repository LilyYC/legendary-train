""" levels

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

    def levels(self):
        """ raturn a list of items in the tree
        >>> r2 = BinarySearchTree(75)
        >>> r2._left = BinarySearchTree(66)
        >>> r2._right = BinarySearchTree(80)
        >>> l2 = BinarySearchTree(20)
        >>> l2._left = BinarySearchTree(5)
        >>> l2._right = BinarySearchTree(25)
        >>> l1 = BinarySearchTree(50)
        >>> l1._left = l2
        >>> l1._right = r2
        >>> bst = BinarySearchTree(90)
        >>> bst._left = l1
        >>> bst._right = BinarySearchTree(None)
        >>> bst.levels()
        """
        if self.is_empty():
            return []
        elif self._left.is_empty() and self._right.is_empty():
            return [(1, [self._root])]
        elif self._right.is_empty():
            level = [(1, [self._root])]
            extend = self._left.levels()
            for i in range(len(extend)):
                level.append((i + 2, extend[i][1]))
            return level


        elif self._left.is_empty():
            level = [(1, [self._root])]
            extend = self._right.levels()
            for i in range(len(extend)):
                level.append((i + 2, extend[i][1]))
            return level
        else:
            level = [(1, [self._root])]
            extend1 = self._left.levels()
            extend2 = self._right.levels()
            for j in range(len(extend1)):
                level.append((j + 2, extend1[j][1]))
                level.append((j + 2, extend2[j][1]))
            return level


def recursion_error(x):
    if x is None:
        "Done"
    x = recursion_error(x)
    return x


if __name__ == '__main__':
    print(recursion_error(2))
