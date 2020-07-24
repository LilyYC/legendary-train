class BTNode:
    def __init__(self, item, left=None, right=None):
        self.item = item
        self.left = left
        self.right = right

    def reverse(self):
        """
        >>> right = BTNode('is', 'fun')
        >>> left = BTNode('test')
        >>> tree = BTNode('this', left, right)
        >>> tree.reverse()
        >>> tree.item

        >>> tree.right.item

        """
        if self is None:
            pass
        elif self.left is None and self.right is None:
            self.item = self.item[::-1]
        elif self.left is not None:
            self.item = self.item[::-1]
            self.left.reverse()
        else:
            self.item = self.item[::-1]
            self.right.reverse()

def leaf_list(root):
    """
    >>> left1 = BTNode('fun')
    >>> right = BTNode('is', left1)
    >>> left = BTNode('test')
    >>> tree = BTNode('this', left, right)
    >>> leaf_list(tree)

    """
    result = []
    if root is None:
        return result
    elif root.left is None and root.right is None:
        result.append(root.item)
        return result
    else:
        if root.left is not None:
            result.extend(leaf_list(root.left))
        if root.right is not None:
            result.extend(leaf_list(root.right))
        return result

class LLNode:
    def __init__(self, item, link=None):
        self.item = item
        self.link = link

class Queue:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return not self.head

    def enqueue(self, item):
        """ Add item to the back of this queue.
        """
        if self.is_empty():
            self.head = LLNode(item)
        else:
            curr = self.head
            while not curr.link:
                curr = curr.link
            curr.link = LLNode(item)
