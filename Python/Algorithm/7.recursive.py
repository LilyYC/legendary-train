"""Recursion

"""
from typing import Dict, List


##############################################################################
# Task 1: Something a little different
##############################################################################
# The file of English words to use. The one we've provided doesn't contain
# plural forms. Assume this list is in alphabetical order.
FILE = 'dict.txt'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def anagrams(phrase: str, limit: int) -> List[str]:
    """Return a list of up to <limit> anagrams of <phrase>.

    The anagrams are returned in alphabetical order.

    >>> anagrams('dormitory', 3)
    ['dirty room', 'dormitory', 'room dirty']
    """
    # use the debugger to inspect the contents of the following two
    # variables. This is particularly useful to see how the letter frequencies
    # are being represented.
    words = _generate_word_list(FILE)
    letter_count = _generate_letter_count(phrase)
    return _anagrams_helper(words, letter_count, limit)


def _generate_word_list(dict_file: str) -> List[str]:
    """Read in English words from <dict_file> and return them.

    The returned list is in alphabetical order.

    Precondition:
    """
    words = []
    with open(dict_file) as f:
        for line in f.readlines():
            words.append(line.strip().lower())
    return words


def _generate_letter_count(phrase: str) -> Dict[str, int]:
    """Return a dictionary counting the letter occurrences in <string>.

    All letters in <phrase> are converted to lower-case.
    The keys in the returned dictionary are the 26 lower-case letters,
    'a', 'b', 'c', etc.

    Precondition: <phrase> contains only letters.
    """
    lower = phrase.lower()
    letter_count = {}
    for char in LETTERS:
        letter_count[char] = lower.count(char)
    return letter_count


def _within_letter_count(word: str, letter_count: Dict[str, int]) -> bool:
    """Return whether <word> can be made using letters in <letter_count>."""
    for char in LETTERS:
        if word.count(char) > letter_count[char]:
            return False
    return True


def _anagrams_helper(words: List[str], letter_count: Dict[str, int],
                     limit: int) -> List[str]:
    """Return the first <limit> anagrams using the given letter counts
    and allowed words.

    Each anagram must use all the letters, with correct occurrences, given by
    <letter_count>, and must use only the words appearing in <words>.

    Note: we're using a helper function here so that you don't need to
    recompute <words> for each recursive call.

    If there are more than <limit> possible anagrams, return the <limit>
    anagrams that are first alphabetically.
    If there are fewer than <limit> possible anagrams, return all of them.

    The anagrams are returned in alphabetical order.

    Preconditions:
    - letter_count has 26 keys (one per lowercase letter),
      and each value is a non-negative integer.
    - limit >= 0
    """
    anagrams_list = []

    # 1. Base case: limit == 0.
    if limit == 0:
        return []

    # 2. Base case: no more letters in <letter_count>.
    # In this case, there is only one valid anagram: the empty string.
    elif all(value == 0 for value in letter_count.values()):
        return ['']

    for word in words:

        # 3. For each word, check whether it can be used with the given
        # letter count. (If not, go onto the next word.)
        if not _within_letter_count(word, letter_count):
            continue

        # 4. If the word can be used, recurse and create anagrams.
        # (i) Create a new dictionary that has the same values as
        # letter_count, with counts decreased based on the letters in <word>
        # this word is a potential valid component of an anagram

        anagram = word

        # decrease letter_count by 1 for each letter appears in the word
        new_dict = letter_count.copy()
        for letter in word:
            new_dict[letter] -= 1

        # (ii) Call _anagrams_helper recursively with the new, reduced
        # letter count.
        new_lst = _anagrams_helper(words, new_dict, limit)

        #  (iii) Combine <word> with the result of the recursive call to
        # update <anagrams_list> with the anagrams that start with <word>.
        # Don't forget to separate the words with a space.
        for new_word in new_lst:
            if new_word:
                anagram = word + ' ' + new_word
            anagrams_list.append(anagram)

            # 5. If the limit has been reached, stop the loop early!
            if len(anagrams_list) == limit:
                return anagrams_list

    # 6. Return the anagrams that can be made by the letters in letter_count.
    return anagrams_list

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['_generate_word_list']
    })
