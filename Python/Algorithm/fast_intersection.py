# Final Practice


def f_i(lst1: list, lst2: list) -> list:
    """

    return a list of common items
    >>> f_i([1, 2, 3, 5, 10], [3, 6, 8, 10])
    [3, 10]
    >>> f_i([2, 4, 12], [1, 2, 3, 5, 12, 23])
    [2, 12]
    """

    index1, index2 = 0, 0
    result = []
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] > lst2[index2]:
            index2 += 1
        else:
            if lst1[index1] == lst2[index2]:
                result.append(lst1[index1])
            index1 += 1
            index2 = 0
    return result


def width(lst_, max_depth):
    """
    >>> list_ = [0,1]
    >>> width(list_,1)
    2
    >>> list_ = [[0, 1], 2, [3, [[], 4]]]
    >>> width(list_,4)
    4
    """
    if isinstance(lst_, int):
        return 1
    elif max_depth == 1:
        return len(lst_)
    else:
        curr_depth = 0
        curr_width = 0
        while curr_depth < max_depth:
            temp_width = get_width_at_d(lst_, curr_depth)
            if temp_width > curr_width:
                curr_width = temp_width
            curr_depth += 1
        return curr_width


def get_width_at_d(lst, d: int) -> int:
    """
    >>> get_width_at_d([1, 2], 1)
    2
    >>> get_width_at_d([[1, 2, 3], [2,4]], 2)
    5
    """
    if d == 0 or isinstance(lst, int):
        return 0
    elif d == 1:
        return len(lst)
    else:
        count = 0
        for sublist in lst:
            count += get_width_at_d(sublist, d-1)
        return count
