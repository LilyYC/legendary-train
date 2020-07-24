from typing import List, Union

##############################################################################
# Recursion Practice
  Task 1: nested lists
##############################################################################

def duplicate(nested_list: Union[list, int]) -> list:
    """Return a new nested list with all numbers in <nested_list> duplicated.

    Each integer in <nested_list> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <nested_list> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])
    [1, 1, [2, 2, 3, 3]]
    """
    new_list = []
    if isinstance(nested_list, int):
        new_list.append(nested_list)
        new_list.append(nested_list)
    else:
        for num in range(len(nested_list)):
            if isinstance(nested_list[num], int):
                new_list.append(nested_list[num])
                new_list.append(nested_list[num])
            else:
                new_list.append(duplicate(nested_list[num]))
    return new_list


def add_one(nested_list: Union[list, int]) -> None:
    """Add one to every number stored in <nested_list>.

    Do nothing if <nested_list> is an int.
    If <nested_list> is a list, *mutate* it to change the numbers stored.
    (Don't return anything in either case.)

    >>> lst0 = 1
    >>> add_one(lst0)
    >>> lst0
    1
    >>> lst1 = []
    >>> add_one(lst1)
    >>> lst1
    []
    >>> lst2 = [1, [2, 3], [[[5]]]]
    >>> add_one(lst2)
    >>> lst2
    [2, [3, 4], [[[6]]]]
    """
    if isinstance(nested_list, int):
        pass
    else:
        for i in range(len(nested_list)):
            if isinstance(nested_list[i], int):
                nested_list[i] += 1
            else:
                add_one(nested_list[i])


##############################################################################
# Task 2: Family trees
##############################################################################
class Person:
    """A person in a family tree.

    === Attributes ===
    name:
        The name of this person.
    children:
        The children of this person.
    """
    name: str
    children: List['Person']

    def __init__(self, new_name: str, new_children: List['Person']) -> None:
        """Create a new person with the given name and children.
        """
        self.name = new_name
        self.children = new_children

    def count_descendants(self) -> int:
        """Return the number of descendants of this person.
        """
        count = 0
        if self.children == []:
            return count
        else:
            for child in self.children:
                count = count + 1 + child.count_descendants()
            return count


if __name__ == '__main__':
    import python_ta

    python_ta.check_all()

    import doctest

    doctest.testmod()
