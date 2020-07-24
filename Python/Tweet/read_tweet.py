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
        if line.endswith(':\n') and 2 <= len(line.split()) <= 3:
            key = line.strip()[: -1]
            dic[key] = []
        else: 
            if line != "<<<EOT\n":
                # then we accumulate the content
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
    >>> content = ['791651860889427968,1477593886,Queens NY,Twitter for iPhone \
    ,10775,4475\n', 'JOIN ME! #MAGA\n', 'TODAY:\n', 'Springfield, OH \n', 'Tol \
    edo, OH \n', 'Geneva, OH \n', 'FRIDAY:\n', 'Manchester, NH \n', 'Lisbon, \
    ME \n', 'Cedar Rapids, IA\n', 'https://t.co/kv624y9UOm\n', '\n']
    >>> help_read_tweet(dic, key, content)
    >>> dic 
    {'Donald Trump': [('Donald Trump', 'JOIN ME! #MAGA\n TODAY:\n Springfield,\
    OH \n Toledo, OH \n Geneva, OH \n FRIDAY:\n Manchester, NH \n Lisbon, \
    ME \n Cedar Rapids, IA\n https://t.co/kv624y9UOm\n \n')]}    
    """
    
    for s in content:
        if len(s.split(',')) == HEADER_LENGTH and s.split(',')[0].isnumeric():
            info = s.split(',')
        else:
            txt = s + ' '
    text = txt[:len(txt)]
    value = (key, text, int(info[1]), info[3], int(info[4]), int(info[5][:-1]))
    dic[key].append(value)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
