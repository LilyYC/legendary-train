 def only_evens(lst):
    """ (list of list of int) -> list of list of int
 # write your code here (be sure to read above for a suggested approach)
    Return a list of the lists in lst that contain only even integers. 
   
    >>> only_evens([[1, 2, 4], [4, 0, 6], [22, 4, 3], [2]])
    [[4, 0, 6], [2]]
    """
    
    even_lists = []
    
    for sublist in lst:
    	if only_even1(sublist) == True:
	    even_lists.append(sublist)
    return even_lists