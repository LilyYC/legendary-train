# Task 2: DNA palindromes
# 1. is_base_pair function

def is_base_pair(s1, s2):
    """ (str, str) -> bool
    
    Precondition: s1 and s2 both contain a single character from 'A', 'T', 'C'
    or 'G'.
    
    Return True iff s1 and s2 form a base pair.
    
    >>> is_base_pair('A','T')
    True
    >>> is_base_pair('G','T')
    False
    """
    
    cond1 = (s1 == 'A' and s2 == 'T')
    cond2 = (s1 == 'T' and s2 == 'A')
    cond3 = (s1 == 'G' and s2 == 'C')
    cond4 = (s1 == 'C' and s2 == 'G')
    
    if cond1 or cond2 or cond3 or cond4:
        return True
    else:
        return False
    
# 2. is_dna function

def is_dna(s1, s2):
    """ (str, str) -> bool
    
    Precondition: s1 and s2 have equal length and only contain characters from
    'A', 'T', 'C' or 'G'.
    
    Return True iff s1 and s2 form a properly base-paired DNA molecule.
    
    >>> is_dna('GATCGCC','CTAGCGG')
    True
    >>> is_dna('ATCAG','CGATC')
    False
    """
    
    count = 0
    for i in range(len(s1)):
        if is_base_pair(s1[i], s2[i]):
            count = count + 1
    return count == len(s1)

# 3. is_dna_palindrome function

def is_dna_palindrome(s1, s2):
    """ (str, str) -> bool	
    
    Precondition: s1 and s2 only contain characters from 'A', 'T', 'C' or 'G'.
                  is_dna(s1, s2) would return True. 
    
    Return True iff s1 and s2 form a DNA palindrome. 
    
    >>> is_dna_palindrome('GATC','CTAG')
    True
    >>> is_dna_palindrome('GCCTA','CGGAT')
    False
    """
    
    return s1 == s2[::-1]

#4. restruction_sites function

def restriction_sites(s1, s2):
    """ (str, str) -> list of int
    
    Precondition: s1 only contains characters from 'A', 'T', 'C' or 'G'.
                  s2 is a recognition sequence. 
    
    Return a list of all the indices where s2 appears in s1.
    
    >>> restriction_sites('GCTATCGAGGATCGA','TCGA')
    [4, 11]
    >>> restriction_sites('GGCCTAGAGGCCAGGCCGGC','GGCC')
    [0, 8, 13]
    """
    
    result = []
    a = s1.find(s2)
    
    if a != -1: 
        while len(result) < s1.count(s2):
            result.append(a)
            a = s1.find(s2, a + 1)
    return result

#5. match_enzymes function

def match_enzymes(s, lst1, lst2):
    """ (str, list of str, list of str) -> list of two-item [str, list of int]
    lists
    
    Precondition: s only contains characters from 'A', 'T', 'C' or 'G'.lst2 is 
    the corresponding list of recognition sequences of the restriction enzyme 
    names in lst1. len(lst1) == len(lst2).
    
    Return a list of two-item lists where the first item of each two-item list 
    is the name in lst1 and the second item is the list of indices (in s) of 
    the restriction sites in lst2.
                  
    >>> match_enzymes('GCTATCGAGATCAGGCC',['TaqI','Sau3A','HaeIII'],['TCGA',
    'GATC','GGCC'])
    [['TaqI',[4]], ['Sau3A',[8]], ['HaeIII',[13]]]
    >>> match_enzymes('AGCTCCAGCTAGCTAGTACT',['AluI','ScaI'],['AGCT','AGTACT'])
    [['AluI',[0, 6, 10]],['ScaI',[14]]]
    """
    
    result = []
    for i in range(len(lst1)):
        a = [lst1[i], restriction_sites(s, lst2[i])]
        result.append(a)
    return result

#6. one_cutters function

def one_cutters(s, lst1, lst2):
    """ (str, list of str, list of str) -> list of two-item [str, list of int]
    lists
    
    Precondition: s only contains characters from 'A', 'T', 'C' or 'G'.lst2 is 
    the corresponding list of recognition sequences of the restriction enzyme 
    names in lst1. len(lst1) == len(lst2).
    
    Return a list of two-item lists representing the 1-cutters for the s. The 
    first item of each two-item list is the name in lst1 and the second item is 
    the index (in s) of the one restriction site in lst2.
    
    >>> one_cutters('TCGAGATCGATCCCCC',['TaqI','Sau3A'],['TCGA','GATC'])
    []
    >>> one_cutters('TCGACCC',['TaqI','Sau3A'],['TCGA','GATC'])
    [['TaqI',[0]]]
    """
    
    result = []
    for i in range(len(lst1)):
        if s.count(lst2[i]) == 1:
            a = [lst1[i], restriction_sites(s, lst2[i])[0]]
            result.append(a)
    return result

#7. correct_mutations function

def correct_mutations(strands, clean, names, sequences):
    """ (list of str, str, list of str, list of str) -> NoneType
    
    Precondition: strands and clean only contain characters in 'A', 'T', 'C' or 
    'G'. clean contains exactly one 1-cutter from names and sequences. 
    sequences is the corresponding list of recognition sequences of names. 
    len(names) == len(sequences).
    
    Modify strands by replacing all bases starting at the 1-cutter in strands 
    with all bases starting at the 1-cutter in clean.
    
    >>> correct_mutations(['CCCAGCTGGG', 'CGTTTTTAAAAA'], 'AGAGCTTTT', ['AluI', 
    'BamHI'], ['AGCT', 'GGATCC'])
    >>> strands
    ['CCCAGCTTTT', 'CGTTTTTAAAAA']
    >>> correct_mutations(['AAGGCCCCCGGG', 'TTGGCCGGCC'], 'TAGGCCAA', ['HaeIII',
    'SmaI'], ['GGCC', 'CCCGGG'])
    >>> strands
    ['AAGGCCAA', 'TTGGCCGGCC']
    """
    
    result = []
    for item in sequences:
        for ch in strands:
            if item in clean and ch.count(item) == 1:
                a = ch[0:ch.find(item)] + clean[clean.find(item):]  
                result.append(a)
            else:
                result.append(ch)
                
    
    
                
                
            