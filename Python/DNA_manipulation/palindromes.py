# Task 1: Regular Palindromes
# 1. is_palindrome function

def is_palindrome(s):
    """ (str) -> bool
    
    Precondition: String only contains lowercase alphabetic letters.
    
    Return True iff s is a palindrome.
    
    >>> is_palindrome('madam')
    True
    >>> is_palindrome('run')
    False
    """
    
    return s == s[::-1]

# 2. is_palindromic_phrase function

def is_palindromic_phrase(s):
    """ (str) -> bool
    
    Return True iff s is a palindrome, ignoring case and non-alphabetic 
    characters.
    
    >>> is_palindromic_phrase('Appl05-#$elppa')
    True
    >>> is_palindromic_phrase('Mada123r')
    False
    """
    
    result = ''
    for i in range(len(s)):
        if s[i].isalpha():
            result += s[i]
    return result.lower() == result.lower()[::-1]

# 3. get_odd_palindrome_at function

def get_odd_palindrome_at(s, index):
    """ (str, int) -> str
    
    Precondition: s contains only lowercase alphabetic characters.
    0 <= index < len(s)
    
    Return the longest odd-length palindrome in s that is centered at index. 
    
    >>> get_odd_palindrome_at('accccc', 2)
    'ccc'
    >>> get_odd_palindrome_at('accccc', 3)
    'ccccc'
    """
    
    result = s[index]
    for i in range(0, min(index, len(s) - index)):
        s1 = s[index - i: index + i + 1]
        if s1 == s1[::-1]:
            result = s1
    return result

        
       
       
       
       