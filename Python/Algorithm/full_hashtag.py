def extract_hashtags(tweet):
    """ (str) -> list of str
    
    Precondition: 1 <= len(tweet) <= 140
    
    Return  a list of string containing all of the unique hashtags in the tweet.
    
    >>> extract_hashtags('I love #autumn, #Fall and want to #fall')
    ['autumn', 'Fall', 'fall']
    >>> extract_hashtags('#life is so hard, #keep up with #life- #life.')
    ['life', 'keep']
    """
    
    result = []
    for word in tweet.split():
        if word[0] == '#' and word[1:len(word)].isalnum():
            if word[1:] not in result:
                result.append(word[1:])
        elif word[0] == '#' and word[1:-1].isalnum():
            if word[1:len(word)-1] not in result:
                result.append(word[1:len(word)-1])
    return result

def all_hashtag(dic):
    """(dict of {str: list of tweet tuples}, str) -> dict of {str: list of str}
    
    Return all hashtags for each candidate in dic
    
    >>> dic = {'Dr. Jill Stein': [('Dr. Jill Stein', 'Cli #FollowTheMoney https://t.co/p3DXN0y5Kd', 1478039428, 'Hootsuite', 28, 33), ('Dr. Jill Stein', 'g. #...', 1476943692, 'Twitter for iPhone', 0, 797), ('Dr. Jill Stein', 'asdfa #OccupyTheDebates #debates', 1474955228, 'Twitter Web Client', 491, 379)]}
    >>> all_hashtag(dic)
    {'Dr. Jill Stein': ['FollowTheMoney', 'OccupyTheDebates', 'debates']}
    """
    
    ndic = {}
    hashtaglst = []
    for candidate in dic:
        for i in range(len(dic[candidate])):
            hashtag = extract_hashtags(dic[candidate][i][1])
            if hashtag not in hashtaglst:
                hashtaglst += hashtag
        ndic[candidate] = (hashtaglst)
        hashtaglst = []
    return ndic

    
if __name__ == '__main__':
    import doctest
    doctest.testmod()