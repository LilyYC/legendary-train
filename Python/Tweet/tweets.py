TIE = "Tie"
HEADER_LENGTH = 6
ANONYMOUS = 'unknown'

# A helper that splits the string into a list of words.
def get_pure_wordlist(tweet):  
    """ (str) -> list of str
    
    Return a list of string containing all words ending with alphanumerics.
       
    >>> get_pure_wordlist('Hello! @Leehom- @StarWay.')
    ['hello', '@leehom', '@starway']
    >>> get_pure_wordlist('@Here: @1223 @here: me')
    ['@here', '@1223', '@here', 'me']
    """
    
    result = []
    wordlist = tweet.split()
    for word in wordlist:
        if not word[-1].isalnum():
            result.append(word.lower()[:len(word) - 1])
        else:
            result.append(word.lower())
    return result

# 1.
def extract_mentions(tweet):
    """ (str) -> list of str
    
    Precondition: 1 <= len(tweet) <= 140. 
    
    Return a list of string containing all of the mentions in the tweet.
    
    >>> extract_mentions('Hello! @Leehom- @StarWay.')
    ['leehom', 'starway']
    >>> extract_mentions('@Here: @1223 @Gu&a$ @here: me @...')
    ['here', '1223', 'gu', 'here', '']
    """
    
    result = []
    lst = get_pure_wordlist(tweet)
    for word in lst:
        # set initial index for index in word
        i = 1
        if word.startswith('@'):
            # move index to the right if the ith character is alphanumeric
            while i < len(word) and word[i].isalnum():
                i = i + 1    
            result.append(word[1:i])
    return result    

# 2.
def extract_hashtags(tweet):
    """ (str) -> list of str
    
    Return  a list of strings containing all unique hashtags in the tweet.
    
    >>> extract_hashtags('I love #autumn, #fall%3525 and want to #fall')
    ['autumn', 'fall']
    >>> extract_hashtags('#Life is so hard, #keep up with #life- #...')
    ['life', 'keep', '']
    """
    
    result = []
   
    # loop over words from lowercase pure wordlist
    for word in get_pure_wordlist(tweet):
        i = 1
        if word.startswith('#') and len(word) >= 2:
            while i < len(word) and word[i].isalnum():
                i = i + 1    
            if word[1:i] not in result:
                result.append(word[1:i])
    return result

# 3.
def count_words(tweet, dic):
    """ (str, dict of {str: int}) -> None
    
    Update the counts of words from the tweet in the dic.
    
    >>> tweet = "@utmandrew Don't you wish you? #MakeAmerican"
    >>> dic = {'you': 1, 'fun': 4}
    >>> count_words(tweet, dic)
    >>> dic == {'you': 3, 'wish': 1, 'fun': 4, 'dont': 1}
    True
    """
    
    for word in get_pure_wordlist(tweet):
        for item in range(1, len(word) - 1):
            # remove non alphanumeric characters from each word
            if not word[item].isalnum():
                word = word[:item] +word[item + 1:]
        if word[0] != '@' and word[0] != '#' and not word.startswith('http'):
            # add word that are not in dic, assign value 1
            if word not in dic: 
                dic[word] = 1
            # add value to the original value plus 1 for those already in dic    
            elif word in dic:
                dic[word] = dic[word] + 1
                
#4
def common_words(dic, N):
    """(dict of {str: int}, int) -> None
    
    Update the dic so that it contains only N most frequent words.

    >>> dic = {'I': 10, 'you': 5, 'miss': 8, 'here': 6, 'how': 6}
    >>> common_words(dic, 3)
    >>> dic == {'I': 10, 'miss': 8} 
    True
    >>> dic = {'I':10, 'you': 5, 'miss': 8, 'here': 2, 'how': 6}
    >>> common_words(dic, 6)
    >>> dic == {'I': 10, 'you': 5, 'miss': 8, 'here': 2, 'how': 6}
    True
    """
    
    ndic = {} 
    # get a list of sorted words
    wordlist = sorted(dic, key = dic.get, reverse = True)
    # loop over the wordlist to find words that has frequency not equal to N+1
    if len(dic) > N:
        for i in range(N):
            if dic[wordlist[i]] != dic[wordlist[N]]:
                # if the frequency is not equal to N+1 th, put it into ndic
                ndic[wordlist[i]] = dic[wordlist[i]]  
        # when the foor loop is over, clear dic        
        dic.clear()
        # update the dic by ndic that is generated above
        dic.update(ndic) 
        
# 5. 
def read_tweets(file):
    """ (file open for reading) -> dict of {str: list of tweet tuples}

    Return a dictionary with the names of the candidates
    as keys, and tweet tuple in the form of (candidate, tweet text, date, 
    source, favorite count, retweet count)as values
    """
 
    dic = {}  
    key = ""
    content = []
    for line in file:
        # read the line of candidate name
        if line.endswith(':\n') and 2 <= len(line.split()) <= 4:
            key = line.strip()[: -1]
            # store the candadate as a key in dic
            dic[key] = [] 
        else: 
            # for lines before end of tweet
            if line != "<<<EOT\n":
                # store the header of a tweet
                if len(line.split(',')) == HEADER_LENGTH:
                    header = line.split(',')
                # for non-header, we accumulate the content
                content.append(line[:len(line)])
            else:
                # use a helper function to generate the tuple for the value
                help_read_tweet(dic, key, content)
                content = []
    return dic

def help_read_tweet(dic, key, content):
    """ (dic, str, list of str) --> None
    
    Update the dictionary with dic, key as the key, and content as value.
    
    >>> key = 'Donald Trump'
    >>> dic = {key: []}
    >>> content = ['7,1,Q NY,iPhone,1,5\\n', '#MAGA\\n']
    >>> help_read_tweet(dic, key, content)
    >>> dic 
    {'Donald Trump': [('Donald Trump', '#MAGA\\n', 1, 'iPhone', 1, 5)]}
    """
    
    txt = ""
    for s in content:
        if len(s.split(',')) == HEADER_LENGTH and s.split(',')[0].isnumeric():
            info = s.split(',')
        else:
            txt += s
    text = txt[:len(txt)]
    value = (key, text, int(info[1]), info[3], int(info[4]), int(info[5][:-1]))
    dic[key].append(value)
    
# 6.
def most_popular(dic, d1, d2):
    """ ((dict of {str: list of tweet tuples}, int, int) -> str
    
    Precondition: d1 <= d2
    
    Return the most popular candidate on Twitter between d1 and d2.  
    In the case of a tie, return the string "Tie". 
    """
    
    #accumulate counts for each candidate
    counts = 0
    # build a count dictionary for each candidate
    cdic = {}
    for candidate in dic:
        for tweet in dic[candidate]:
            # find tweet under the required time period
            if d1 <= tweet[2] <= d2:
                counts += tweet[-1] + tweet[-2]
        cdic[candidate] = counts
    popular_list = sorted(dic, key = dic.get, reverse = True)
    if dic[popular_list[0]] != dic[popular_list[1]]:
        return popular_list[0]    
    else:
        return TIE

# 7. 
def detect_author(dic, tweet):
    """(dict of {str: list of tweet tuples}, str) -> str
    
    Return the username of the most likely author of that tweet.
    
    If the tweet contains a hashtag that only one of the candidates uses, 
    then the likely author is the candidate that uses that hashtag. 
    
    If the tweet contains no hashtags or more than one hashtag
    that are uniquely used by a single candidate, 
    return the string "Unknown."
    
    >>> dic = {'D': [('D', '#a #i', 1, 'e', 0, 7)], 'M': [('M', '#... #a',\
    1, 'e', 0, 7)]}
    >>> tweet = "hi! #i"
    >>> detect_author(dic, tweet)
    'D'
    """
    
    tweet_ht = extract_hashtags(tweet)
    count = 0
    # count hashtag in tweet
    for i in range(len(tweet_ht)):
        if tweet_ht[i] in unique_hashtag(all_hashtag(dic)):
            count += 1
    for ht in tweet_ht:
        # if hashtag is a unique hashtag in dic and counts only once in tweet
        while ht in unique_hashtag(all_hashtag(dic)) and count == 1:
            return unique_hashtag(all_hashtag(dic))[ht]   
    return ANONYMOUS
           
def all_hashtag(dic):
    """(dict of {str: list of tweet tuples}, str) -> dict of {str: list of str}
    
    Return a dictionary of all hashtags for each candidate in dic.
    
    >>> dic = {'D':[('D', 'F #i', 8, 't', 2, 3), ('D', '#...', 1, 'e', 0, 7)]}
    >>> all_hashtag(dic)
    {'D': ['i', '']}
    """

    ndic = {}
    hashtaglst = []
    for candidate in dic:
        for i in range(len(dic[candidate])):
            tweet = dic[candidate][i] 
            hashtag = extract_hashtags(tweet[1])
            if hashtag not in hashtaglst:
                hashtaglst += hashtag
        ndic[candidate] = (hashtaglst)
        hashtaglst = []
    return ndic

# helper function that finds all unique hashtages for each candidate
def unique_hashtag(dic):
    """dict of {str: list of str} -> dict of {str: list of str}}
    
    Return a dictionary with hashtag as keys and candidate in dic as values.
    
    >>> dic = {'D': ['a', '1', '2'], 'M': ['a', 'i'], 'N': ['1', '0', '']}
    >>> unique_hashtag(dic) == {'2': 'D', 'i': 'M', '0': 'N', '': 'N'}
    True
    """

    unique_ht = {}
    extract_unique = {}
    # First reverse the dictionary
    for candidate in dic:
        for i in range(len(dic[candidate])):
            hashtag = dic[candidate][i]
            if  hashtag not in unique_ht:
                unique_ht[hashtag] = [candidate]
            else:
                unique_ht[hashtag].append(candidate)
    # To extract unique hashtag from the reversed dictionary
    for ht in unique_ht:
        if len(unique_ht[ht]) == 1:
            extract_unique[ht] = unique_ht[ht][0]
    return extract_unique
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
