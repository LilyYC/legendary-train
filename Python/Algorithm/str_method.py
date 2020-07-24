def check_password(passwd):
    """ (str) -> bool

    A strong password has a length greater than or equal to 6, contains at
    least one lowercase letter, at least one uppercase letter, and at least
    one digit.  Return True iff passwd is considered strong.

    >>> check_password('I<3csc108')
    True
    >>> check_password('1aAsdail')
    True
    """
    count_upper, count_lower, count_digit = 0, 0, 0
    if len(passwd) < 6:
        return False
    elif len(passwd) >= 6:
        for ch in passwd:
            if ch.isupper():
                count_upper = count_upper + 1
            elif ch.islower():
                count_lower = count_lower + 1
            elif ch.isdigit():
                count_digit = count_digit + 1
        return count_upper >= 1 and count_lower >= 1 and count_digit >= 1
            
        
    
def upper_lower(s):
    """ (str) -> bool
    
    Return True if and only if there is at least one alphabetic character in s and the alphabetic characters in s
    are either all uppercase or all lowercase.
    
    >>> upper_lower('abc')
    True
    >>> upper_lower('abcXYZ')
    False
    >>> upper_lower('XYZ')
    True
    """
    if s.isupper() or s.islower():
        return True
    else:
        return False
    upper_lower('abc')
    

CHILD = 'child'
ADULT = 'adult'
SENIOR = 'senior'

def overdue_fees(days_late, age_group):
    """ (int, str) -> number
    
    Return the fees for a book that is days_late days late for a borrower
    in the age group age_group.
    
    less than 4 days late: 1 dollar per day

    4 to 6 days late: 2 dollars per day (for all days, including the first 3 days)

more than 6 days late: 3 dollars per day (for all days, including the first 6 days)

 A CHILD gets charged only half of the fees and 
 a SENIOR gets charged only one quarter of the fees. 
 An ADULT pays the full fee.
 
    >>> overdue_fees(2, SENIOR) # 2 days late, SENIOR borrower
    0.5
    >>> overdue_fees(5, ADULT) # 5 days late, ADULT borrower
    10
    """    
    if days_late < 4:
        if age_group == ADULT:
            return days_late
        if age_group == CHILD:
            return days_late / 2
        if age_group == SENIOR:
            return days_late / 4
    elif 4 <= days_late <= 6:
        if age_group == ADULT:
            return days_late * 2
        if age_group == CHILD:
             return days_late
        if age_group == SENIOR:
             return days_late / 2
    elif date_late > 6:
        if age_group == ADULT:
            return days_late * 3
        if age_group == CHILD:
         return days_late * 3 / 2
        if age_group == SENIOR:
         return days_late * 3 / 4
        
            