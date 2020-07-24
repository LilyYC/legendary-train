#Algorithm1

def reverse(s):
    """ (str) -> str

    Return s reversed.
    
    >>> reverse('hello')
    'olleh'
    """

    s_reversed = ''
    for ch in s:
        s_reversed = ch + s_reversed
    return s_reversed