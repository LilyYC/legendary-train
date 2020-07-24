"""Tree Practice

=== Module description ===
- Task 1, which contains one Tree method to implement.
- Task 2, which asks you to implement two operations that allow you
  to convert between trees and nested lists.
- Task 3, which asks you to learn about and use a more restricted form of
  trees known as *binary trees*.
"""

from typing import Optional, List, Union


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and LinkedListRec
    from Lab 7; the only major difference is that _rest
    has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[object]
    # The list of all subtrees of this tree.
    _subtrees: List['Tree']

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    # - self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    # === Methods ===
    def __init__(self, root: object, subtrees: List['Tree']) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

##############################################################################
# Task 1: Another tree method
##############################################################################
    def __eq__(self, other: 'Tree') -> bool:
        """Return whether <self> and <other> are equal.

        Hint: you can use the standard structure for recursive functions on
        trees, except that you'll want to loop using an index:
          `for i in range(len(self._subtrees))`)

        This way, you can access the corresponding subtree in `other`.
        """
        if self.is_empty():
            return other.is_empty()
        elif len(self._subtrees) == 0:
            return self._root == other._root and len(other._subtrees) == 0
        elif len(self._subtrees) == len(other._subtrees):
            for subtree_index in range(len(self._subtrees)):
                if self._subtrees[subtree_index] != \
                        other._subtrees[subtree_index]:
                    return False
            return True


##############################################################################
# Task 2: Trees and nested lists
##############################################################################
    def to_nested_list(self) -> list:
        """Return the nested list representation of this tree.
        """
        nested_list = []
        if self.is_empty():
            return nested_list
        elif len(self._subtrees) == 0:
            nested_list.append(self._root)
            return nested_list
        else:
            nested_list.append(self._root)
            sub_list = []
            for subtree_index in range(len(self._subtrees)):
                sub_list.append(self._subtrees[subtree_index].to_nested_list())
            nested_list.extend(sub_list)
            return nested_list


def to_tree(obj: Union[int, List]) -> 'Tree':
    """Return the Tree which <obj> represents.

    You may not access Tree attributes directly. This function can be
    implemented only using the Tree initializer.    >>> tree3 = Tree(3, [])
    >>> tree2 = Tree(2, [tree3])
    >>> tree1 = Tree(1, [tree2])
    >>> nested_tree = tree1.to_nested_list() # [1, [2, [3]]]
    >>> type(to_tree(nested_tree))
    'Tree'
    >>> to_tree(nested_tree)._root
    1
    >>> to_tree(nested_tree)._subtrees
    2
    >>> tree3 = Tree(3, [])
    >>> tree2 = Tree(2, [tree3])
    >>> tree1 = Tree(1, [tree2])
    >>> tree1.to_nested_list()
    [1, [2, [3]]]
    """
    subtree = []
    if obj == []:
        return Tree(None, subtree)
    elif len(obj) == 1:
        root = obj[0]
        return Tree(root, subtree)
    else:
        root = obj[0]
        # tree = Tree(obj[0], subtree)   # obj is a List of int and list
        for item in range(1, len(obj)):
            subtree.append(to_tree(obj[item]))
        return Tree(root, subtree)


##############################################################################
# Task 3: Binary trees
##############################################################################
class BinaryTree:
    """A class representing a binary tree.

    A binary tree is either empty, or a root connected to
    a *left* binary tree and a *right* binary tree (which could be empty).
    """
    # === Private Attributes ===
    _root: Optional[object]
    _left: Optional['BinaryTree']
    _right: Optional['BinaryTree']

    # === Representation Invariants ===
    # _root, _left, _right are either ALL None, or none of them are None.
    #   If they are all None, this represents an empty BinaryTree.

    def __init__(self, root: Optional[object],
                 left: Optional['BinaryTree'],
                 right: Optional['BinaryTree']) -> None:
        """Initialise a new binary tree with the given values.

        If <root> is None, this represents an empty BinaryTree
        (<left> and <right> are ignored in this case).

        Precondition: if <root> is not None, then neither <left> nor <right>
                      are None.
        """
        if root is None:
            # store an empty BinaryTree
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = left
            self._right = right

    def is_empty(self) -> bool:
        """Return True if this binary tree is empty.

        Note that only empty binary trees can have left and right
        attributes set to None.
        """
        return self._root is None

    def preorder(self) -> list:
        """Return a list of this tree's items using a *preorder* traversal.
        """
        result = []
        if self.is_empty():
            return result
        else:
            result.append(self._root)
            result += self._left.preorder()
            result += self._right.preorder()
            return result

    def inorder(self) -> list:
        """Return a list of this tree's items using an *inorder* traversal.
        """
        result = []
        if self.is_empty():
            return result
        result += self._left.inorder()
        result.append(self._root)
        result += self._right.inorder()
        return result

    def postorder(self) -> list:
        """Return a list of this tree's items using a *postorder* traversal.
        """
        result = []
        if self.is_empty():
            return result
        result += self._left.postorder()
        result += self._right.postorder()
        result.append(self._root)
        return result

if __name__ == '__main__':
    import python_ta
    python_ta.check_all()
