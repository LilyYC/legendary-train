def get_hash_symbol_indices(s):

    count = []
    for i in range(len(s)):
        if s[i] == '#':
            count.append(i)
    return count

def get_hash_symbol_indices1(s):
    count = []
    for i in range(len(s)):
        count.append(s.find('#', i),)
    return count[:-1]
 
def encode(message, encodings):
    """ (str, list of str) -> int
    Preconditions:
     - len(message) >= 1 and len(encodings) >= 1
     - each string in encodings has length 2
     - every character in message appears as the first character in exactly
       one of the encoding strings.
     - the second character in each encoding string is a character in the
       range '1' to '9'.
    Based on the information in encodings, convert each character in message
    to a digit and return those digits all together as a single integer.
    >>> encode('g', ['a1', 'h2', 'g3', 'j4', 'y5', 'n6'])
    3
    >>> encode('code', ['e1', 'c2', 'p3', 'd4', 'o5', 'n6'])
    2541
    """

    result = ''
    for ch in message:	
        a = encodings.find(ch)
        result = result + encodings[a][1]
    return int(result)