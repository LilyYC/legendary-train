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

    if _name_=='_main_':
        import docttest
        docttest.testmod()
