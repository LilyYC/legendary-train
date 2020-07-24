<!DOCTYPE html>
<html>
<body>
<pre>TIE = &quot;Tie&quot;
HEADER_LENGTH = 6
ANONYMOUS = &#39;unknown&#39;

# A helper that splits the string into a list of words.
def get_pure_wordlist(tweet):  
    &quot;&quot;&quot; (str) -&gt; list of str
    
    Return a list of string containing all words ending with alphanumerics.
       
    &gt;&gt;&gt; get_pure_wordlist(&#39;Hello! @Leehom- @StarWay.&#39;)
    [&#39;hello&#39;, &#39;@leehom&#39;, &#39;@starway&#39;]
    &gt;&gt;&gt; get_pure_wordlist(&#39;@Here: @1223 @here: me&#39;)
    [&#39;@here&#39;, &#39;@1223&#39;, &#39;@here&#39;, &#39;me&#39;]
    &quot;&quot;&quot;
    
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
    &quot;&quot;&quot; (str) -&gt; list of str
    
    Precondition: 1 &lt;= len(tweet) &lt;= 140. 
    
    Return a list of string containing all of the mentions in the tweet.
    
    &gt;&gt;&gt; extract_mentions(&#39;Hello! @Leehom- @StarWay.&#39;)
    [&#39;leehom&#39;, &#39;starway&#39;]
    &gt;&gt;&gt; extract_mentions(&#39;@Here: @1223 @Gu&amp;a$ @here: me @...&#39;)
    [&#39;here&#39;, &#39;1223&#39;, &#39;gu&#39;, &#39;here&#39;, &#39;&#39;]
    &quot;&quot;&quot;
    
    result = []
    lst = get_pure_wordlist(tweet)
    for word in lst:
        # set initial index for index in word
        i = 1
        if word.startswith(&#39;@&#39;):
            # move index to the right if the ith character is alphanumeric
            while i &lt; len(word) and word[i].isalnum():
                i = i + 1    
            result.append(word[1:i])
    return result    

# 2.
def extract_hashtags(tweet):
    &quot;&quot;&quot; (str) -&gt; list of str
    
    Return  a list of strings containing all unique hashtags in the tweet.
    
    &gt;&gt;&gt; extract_hashtags(&#39;I love #autumn, #fall%3525 and want to #fall&#39;)
    [&#39;autumn&#39;, &#39;fall&#39;]
    &gt;&gt;&gt; extract_hashtags(&#39;#Life is so hard, #keep up with #life- #...&#39;)
    [&#39;life&#39;, &#39;keep&#39;, &#39;&#39;]
    &quot;&quot;&quot;
    
    result = []
   
    # loop over words from lowercase pure wordlist
    for word in get_pure_wordlist(tweet):
        i = 1
        if word.startswith(&#39;#&#39;) and len(word) &gt;= 2:
            while i &lt; len(word) and word[i].isalnum():
                i = i + 1    
            if word[1:i] not in result:
                result.append(word[1:i])
    return result

# 3.
def count_words(tweet, dic):
    &quot;&quot;&quot; (str, dict of {str: int}) -&gt; None
    
    Update the counts of words from the tweet in the dic.
    
    &gt;&gt;&gt; tweet = &quot;@utmandrew Don&#39;t you wish you? #MakeAmerican&quot;
    &gt;&gt;&gt; dic = {&#39;you&#39;: 1, &#39;fun&#39;: 4}
    &gt;&gt;&gt; count_words(tweet, dic)
    &gt;&gt;&gt; dic == {&#39;you&#39;: 3, &#39;wish&#39;: 1, &#39;fun&#39;: 4, &#39;dont&#39;: 1}
    True
    &quot;&quot;&quot;
    
    for word in get_pure_wordlist(tweet):
        for item in range(1, len(word) - 1):
            # remove non alphanumeric characters from each word
            if not word[item].isalnum():
                word = word[:item] +word[item + 1:]
        if word[0] != &#39;@&#39; and word[0] != &#39;#&#39; and not word.startswith(&#39;http&#39;):
            # add word that are not in dic, assign value 1
            if word not in dic: 
                dic[word] = 1
            # add value to the original value plus 1 for those already in dic    
            elif word in dic:
                dic[word] = dic[word] + 1
                
#4
def common_words(dic, N):
    &quot;&quot;&quot;(dict of {str: int}, int) -&gt; None
    
    Update the dic so that it contains only N most frequent words.

    &gt;&gt;&gt; dic = {&#39;I&#39;: 10, &#39;you&#39;: 5, &#39;miss&#39;: 8, &#39;here&#39;: 6, &#39;how&#39;: 6}
    &gt;&gt;&gt; common_words(dic, 3)
    &gt;&gt;&gt; dic == {&#39;I&#39;: 10, &#39;miss&#39;: 8} 
    True
    &gt;&gt;&gt; dic = {&#39;I&#39;:10, &#39;you&#39;: 5, &#39;miss&#39;: 8, &#39;here&#39;: 2, &#39;how&#39;: 6}
    &gt;&gt;&gt; common_words(dic, 6)
    &gt;&gt;&gt; dic == {&#39;I&#39;: 10, &#39;you&#39;: 5, &#39;miss&#39;: 8, &#39;here&#39;: 2, &#39;how&#39;: 6}
    True
    &quot;&quot;&quot;
    
    ndic = {} 
    # get a list of sorted words
    wordlist = sorted(dic, key = dic.get, reverse = True)
    # loop over the wordlist to find words that has frequency not equal to N+1
    if len(dic) &gt; N:
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
    &quot;&quot;&quot; (file open for reading) -&gt; dict of {str: list of tweet tuples}

    Return a dictionary with the names of the candidates
    as keys, and tweet tuple in the form of (candidate, tweet text, date, 
    source, favorite count, retweet count)as values
    &quot;&quot;&quot;
 
    dic = {}  
    key = &quot;&quot;
    content = []
    for line in file:
        # read the line of candidate name
        if line.endswith(&#39;:\n&#39;) and 2 &lt;= len(line.split()) &lt;= 4:
            key = line.strip()[: -1]
            # store the candadate as a key in dic
            dic[key] = [] 
        else: 
            # for lines before end of tweet
            if line != &quot;&lt;&lt;&lt;EOT\n&quot;:
                # store the header of a tweet
                if len(line.split(&#39;,&#39;)) == HEADER_LENGTH:
                    header = line.split(&#39;,&#39;)
                # for non-header, we accumulate the content
                content.append(line[:len(line)])
            else:
                # use a helper function to generate the tuple for the value
                help_read_tweet(dic, key, content)
                content = []
    return dic

def help_read_tweet(dic, key, content):
    &quot;&quot;&quot; (dic, str, list of str) --&gt; None
    
    Update the dictionary with dic, key as the key, and content as value.
    
    &gt;&gt;&gt; key = &#39;Donald Trump&#39;
    &gt;&gt;&gt; dic = {key: []}
    &gt;&gt;&gt; content = [&#39;7,1,Q NY,iPhone,1,5\\n&#39;, &#39;#MAGA\\n&#39;]
    &gt;&gt;&gt; help_read_tweet(dic, key, content)
    &gt;&gt;&gt; dic 
    {&#39;Donald Trump&#39;: [(&#39;Donald Trump&#39;, &#39;#MAGA\\n&#39;, 1, &#39;iPhone&#39;, 1, 5)]}
    &quot;&quot;&quot;
    
    txt = &quot;&quot;
    for s in content:
        if len(s.split(&#39;,&#39;)) == HEADER_LENGTH and s.split(&#39;,&#39;)[0].isnumeric():
            info = s.split(&#39;,&#39;)
        else:
            txt += s
    text = txt[:len(txt)]
    value = (key, text, int(info[1]), info[3], int(info[4]), int(info[5][:-1]))
    dic[key].append(value)
    
# 6.
def most_popular(dic, d1, d2):
    &quot;&quot;&quot; ((dict of {str: list of tweet tuples}, int, int) -&gt; str
    
    Precondition: d1 &lt;= d2
    
    Return the most popular candidate on Twitter between d1 and d2.  
    In the case of a tie, return the string &quot;Tie&quot;. 
    &quot;&quot;&quot;
    
    #accumulate counts for each candidate
    counts = 0
    # build a count dictionary for each candidate
    cdic = {}
    for candidate in dic:
        for tweet in dic[candidate]:
            # find tweet under the required time period
            if d1 &lt;= tweet[2] &lt;= d2:
                counts += tweet[-1] + tweet[-2]
        cdic[candidate] = counts
    popular_list = sorted(dic, key = dic.get, reverse = True)
    if dic[popular_list[0]] != dic[popular_list[1]]:
        return popular_list[0]    
    else:
        return TIE

# 7. 
def detect_author(dic, tweet):
    &quot;&quot;&quot;(dict of {str: list of tweet tuples}, str) -&gt; str
    
    Return the username of the most likely author of that tweet.
    
    If the tweet contains a hashtag that only one of the candidates uses, 
    then the likely author is the candidate that uses that hashtag. 
    
    If the tweet contains no hashtags or more than one hashtag
    that are uniquely used by a single candidate, 
    return the string &quot;Unknown.&quot;
    
    &gt;&gt;&gt; dic = {&#39;D&#39;: [(&#39;D&#39;, &#39;#a #i&#39;, 1, &#39;e&#39;, 0, 7)], &#39;M&#39;: [(&#39;M&#39;, &#39;#... #a&#39;,\
    1, &#39;e&#39;, 0, 7)]}
    &gt;&gt;&gt; tweet = &quot;hi! #i&quot;
    &gt;&gt;&gt; detect_author(dic, tweet)
    &#39;D&#39;
    &quot;&quot;&quot;
    
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
    &quot;&quot;&quot;(dict of {str: list of tweet tuples}, str) -&gt; dict of {str: list of str}
    
    Return a dictionary of all hashtags for each candidate in dic.
    
    &gt;&gt;&gt; dic = {&#39;D&#39;:[(&#39;D&#39;, &#39;F #i&#39;, 8, &#39;t&#39;, 2, 3), (&#39;D&#39;, &#39;#...&#39;, 1, &#39;e&#39;, 0, 7)]}
    &gt;&gt;&gt; all_hashtag(dic)
    {&#39;D&#39;: [&#39;i&#39;, &#39;&#39;]}
    &quot;&quot;&quot;

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
    &quot;&quot;&quot;dict of {str: list of str} -&gt; dict of {str: list of str}}
    
    Return a dictionary with hashtag as keys and candidate in dic as values.
    
    &gt;&gt;&gt; dic = {&#39;D&#39;: [&#39;a&#39;, &#39;1&#39;, &#39;2&#39;], &#39;M&#39;: [&#39;a&#39;, &#39;i&#39;], &#39;N&#39;: [&#39;1&#39;, &#39;0&#39;, &#39;&#39;]}
    &gt;&gt;&gt; unique_hashtag(dic) == {&#39;2&#39;: &#39;D&#39;, &#39;i&#39;: &#39;M&#39;, &#39;0&#39;: &#39;N&#39;, &#39;&#39;: &#39;N&#39;}
    True
    &quot;&quot;&quot;

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
    
if __name__ == &#39;__main__&#39;:
    import doctest
    doctest.testmod()</pre>
</body>
</html>
