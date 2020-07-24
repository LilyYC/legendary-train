class _Node:
    """A node in a linked list.

    Note that this is considered a "private class", one
    which is only meant to be used in this module by the
    LinkedList class, but not by client code.

    === Attributes ===
    @type item: object
        The data stored in this node.
    @type next: _Node | None
        The next node in the list, or None if there are
        no more nodes in the list.
    """

    def __init__(self, item):
        """Initialize a new node storing <item>, with no next node.

        @type self: _Node
        @type item: object
        @rtype: None
        """
        self.item = item
        self.next = None  # Initially pointing to nothing


class LinkedList:
    """A linked list implementation of the List ADT.
    """
    # === Private Attributes ===
    # @type _first: _Node | None
    #     The first node in the list, or None if the list is empty.

    def __init__(self, items):
        """Initialize a new linked list containing the given items.

        The first node in the linked list contains the first item
        in <items>.

        @type self: LinkedList
        @type items: list
        @rtype: None
        """
        if len(items) == 0:  # No items, and an empty list!
            self._first = None
        else:
            self._first = _Node(items[0])
            current_node = self._first
            for item in items[1:]:
                current_node.next = _Node(item)
                current_node = current_node.next

    ####   16  MT 1b
    def remove_last(self):
        """
        >>> LLR = LinkedList([1])
        >>> LLR.remove_last()
        >>> str(LLR)
        '[]'
        """
        previous = None
        current = self._first
        while current is not None and current.next is not None:
            previous = current
            current = current.next
        if current is not None:
            if previous is not None:
                previous.next = current.next
            else:
                self._first = current.next

    def merge_pairs(self):
        """
        >>> linky = LinkedList([1, 2, 30, 40, 5, 6, 7])
        >>> linky.merge_pairs()
        >>> str(linky)
        '[3 -> 70 -> 11 -> 7]'
        """
        curr = self._first
        while curr is not None and curr.next is not None:
            curr.item += curr.next.item
            curr.next = curr.next.next
            curr = curr.next




    # ------------------------------------------------------------------------
    # Non-mutating methods: these methods do not change the list
    # ------------------------------------------------------------------------
    def is_empty(self):
        """Return whether this linked list is empty.

        @type self: LinkedList
        @rtype: bool
        """
        return self._first is None

    def __len__(self):
        """Return the number of elements in this list.

        @type self: LinkedList
        @rtype: int
        """
        curr = self._first
        size = 0
        while curr is not None:
            size += 1
            curr = curr.next
        return size

    def __getitem__(self, index):
        """Return the item at position index in this list.

        Raise IndexError if <index> is >= the length of this list.

        @type self: LinkedList
        @type index: int
        @rtype: object
        """
        curr = self._first
        curr_index = 0

        # Iterate to (index)-th node
        while curr is not None and curr_index < index:
            curr = curr.next
            curr_index += 1

        if curr is None:
            raise IndexError
        else:
            return curr.item

    def __str__(self):
        """Return a string representation of this list.

        The string is in the form '[item1 -> item2 -> ... -> item-n]'.

        @type self: LinkedList
        @rtype: str

        >>> lst = LinkedList([1, 2, 3])
        >>> str(lst)
        '[1 -> 2 -> 3]'
        """
        items = []
        curr = self._first
        while curr is not None:
            items.append(str(curr.item))
            curr = curr.next
        return '[' + ' -> '.join(items) + ']'

    # ------------------------------------------------------------------------
    # Mutating methods: these methods modify the list
    # ------------------------------------------------------------------------

    def pop(self, index):
        """Remove node at position <index> and return its item.

        Raise IndexError if <index> is >= the length of <self>.
        Precondition: <index> >= 0.

        @type self: LinkedList
        @type index: int
        @rtype: object
        """
        if len(self) <= index:
            raise IndexError

        if index == 0:
            # TODO: Complete this part of the code!
            pass
        else:
            # Get the node at position (index - 1)
            curr_index = 0
            curr = self._first
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index = curr_index + 1

            if curr is None:
                raise IndexError
            else:
                if curr.next is None:
                    raise IndexError
                else:
                    # curr is the node at index - 1
                    popped_item = curr.next.item
                    curr.next = curr.next.next
                    return popped_item

    def insert(self, index, item):
        """Insert a new node containing item at position <index>.

        Raise IndexError if <index> is > the length of this list.
        Note that adding to the end of a linked list is okay.
        Precondition: <index> >= 0.

        @type self: LinkedList
        @type index: int
        @type item: object
        @rtype: None
        """
        if index > len(self):
            raise IndexError

        # Create new node containing the item
        new_node = _Node(item)

        if index == 0:
            new_node.next = self._first
            self._first = new_node
        else:
            # Get the node at position (index - 1)
            curr_index = 0
            curr = self._first
            while curr is not None and curr_index < index - 1:
                curr = curr.next
                curr_index = curr_index + 1

            if curr is None:
                raise IndexError
            else:
                new_node.next = curr.next
                curr.next = new_node

    # -------------------------------------------------------------------------
    # Lab Exercises
    # -------------------------------------------------------------------------
    def __contains__(self, item):
        """Return whether <item> is in this list.

        Use == to compare items.

        @type self: LinkedList
        @type item: object
        @rtype: bool

        >>> lst = LinkedList([1, 2, 3])
        >>> 2 in lst # Equivalent to lst.__contains__(2)
        True
        >>> 4 in lst
        False
        """
        pass

    def count(self, item):
        """Return the number of times <item> occurs in this list.

        Use == to compare items.

        @type self: LinkedList
        @type item: object
        @rtype: int

        >>> lst = LinkedList([1, 2, 1, 3, 2, 1])
        >>> lst.count(1)
        3
        >>> lst.count(2)
        2
        >>> lst.count(3)
        1
        """
        pass

    def __setitem__(self, index, item):
        """Store item at position <index> in this list.

        Raise IndexError if index is >= the length of self.

        @type self: LinkedList
        @type index: int
        @type item: object
        @rtype: None

        >>> lst = LinkedList([1, 2, 3])
        >>> lst[0] = 100  # Equivalent to lst.__setitem__(0, 100)
        >>> lst[1] = 200
        >>> lst[2] = 300
        >>> str(lst)
        '[100 -> 200 -> 300]'
        """
        # NOTE: Implement without using any other LinkedList methods.
        pass

    def delete_item(self, item):
        """Remove the FIRST occurrence of <item> in this list.

        Do nothing if this list does not contain <item>.

        @type self: LinkedList
        @type item: object
        @rtype: None

        >>> lst = LinkedList([1, 2, 3])
        >>> lst.delete_item(2)
        >>> str(lst)
        '[1 -> 3]'
        >>> lst.delete_item(2)
        >>> str(lst)
        '[1 -> 3]'
        >>> lst.delete_item(3)
        >>> str(lst)
        '[1]'
        >>> lst.delete_item(1)
        >>> str(lst)
        '[]'
        >>> lst.delete_item(1)
        >>> str(lst)
        '[]'
        """
        # NOTE: Implement without using any other LinkedList methods.
        pass

    # -------------------------------------------------------------------------
    # Additional Lab Exercises
    # -------------------------------------------------------------------------

    def map(self, f):
        """Return a new LinkedList whose nodes store items that are
        obtained by applying f to each item in this linked list.

        Does not change this linked list.

        @type self: LinkedList
        @type f: Function
        @rtype: None

        >>> func = str.upper
        >>> func('hi')
        'HI'
        >>> lst = LinkedList(['Hello', 'Goodbye'])
        >>> str(lst.map(func))
        '[HELLO -> GOODBYE]'
        >>> str(lst.map(len))
        '[5 -> 7]'
        """
        pass

    def __iter__(self):
        """Return a linked list iterator.

        Hint: the easiest way to implement __iter__ and __next__ is to
        make the linked list object responsible for its own iteration.

        In other words, __iter__(self) should simply return <self>.
        However, in order to make sure the loop always starts at the beginning
        of the list, you'll need a new private attribute for this class which
        keeps track of where in the list the iterator is currently at.

        @type self: LinkedList
        @rtype: LinkedList
        """
        pass

    def __next__(self):
        """Return the next item in the iteration.

        Raise StopIteration if there are no more items to return.

        Hint: If you have an attribute keeping track of the where the iteration
        is currently at in the list, it should be straight-forward to return
        the current item, and update the attribute to be the next node in
        the list.

        @type self: LinkedList
        @rtype: object

        >>> lst = LinkedList([1, 2, 3])
        >>> iter = lst.__iter__()
        >>> lst.__next__()
        1
        >>> lst.__next__()
        2
        >>> lst.__next__()
        3
        """
        pass
