def last_even(items):
   ''' (list of str) -> int
   
   
   '''   
   for i in range(len(items)):
      if items[i] % 2 == 0:
         i = i + 1
   return items[i-1]

def first_even(items):
   '''(list of str) -> int
   
   Return the first even number in the list of items, if there's no even numbers in the list, return -1
   
   first_even([7,34,2,3,4,5])
   34
   first_even([1, 9, 4, 77, 13, 6, 8])
   4
   first_even([2,4,6,8])
   2
   first_even([1,3,5,7,11,4329,141343])
   -1
   '''
       for i in x:
           if i%2 == 0:
               return i
       else:
           return -1