def search_closet(items, colour):
    '''
    
    >>> search_closet(['red summer jacket', 'orange spring jacket', 'red shoes', 'green hat'], 'red')
    ['red summer jacket', 'red shoes']
    >>> search_closet(['red shirt', 'green pants'], 'blue')
    []
    >>> search_closet([], 'mauve')
    []
    
    '''
    matching_colour = []

    for i in range(len(items)):
        if items[i].startswith(colour): 
            matching_colour.append(items[i])
   
    return matching_colour