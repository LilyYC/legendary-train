SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2016'

NO_EXAM = 'NE'

def is_special_case(record):
    """ (str) -> bool

    Return True iff the student represented by record is a special case.

    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    True
    >>> is_special_case('Jacqueline Smith,Father Something High School,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    >>> is_special_case('Jacqueline Smith,Fort McMurray Composite High,2015,MAT,90,94,ENG,92,88,CHM,80,85,BArts')
    False
    """

    if SPECIAL_CASE_YEAR in record and (SPECIAL_CASE_SCHOOL_1 in record or SPECIAL_CASE_SCHOOL_2 in record):
        return True
    else:
        return False
    
    
def get_final_mark(record, course_mark, exam_mark):
    """ (str, str, str) -> float
    
    Return the final mark based on a student's school record, course mark, and exam mark.
    
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '90', '94')
    92.0
    >>>get_final_mark('Jacqueline Smith,Father Something High School,2015,MAT,90,NE,ENG,92,88,CHM,80,NE,BArts', '94', 'NE')
    47.0
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,NE,ENG,92,88,CHM,80,NE,BArts', '90', 'NE')
    90.0
    """
    if NO_EXAM not in exam_mark:
        return (int(course_mark) + int(exam_mark)) / 2
    elif is_special_case(record) == False:
        return float(course_mark) / 2
    else:
        return float(course_mark)
    
def get_both_marks(course_record, course_code):
    """(str, str) -> str
    
    Return a string of coursemark and exammark if the course record matches with the course code.
    
    >>>get_both_marks('MAT,90,94', 'MAT')
    '90 94'
    >>>get_both_marks('MAT,90,94', 'ENG')
    ''
    """
    if course_code in course_record:
        return course_record[4:6] + ' ' + course_record[7:9]
    else:
        return ''
    
def extract_course(transcript, i):
    """(str, int) -> str
        
    Return the nth course transcript record from the course transcript
    
    Precondition: i >= 1
    >>>extract_course('MAT,90,94,ENG,92,88,CHM,80,85', 1)
    'MAT,90,94'
    >>>extract_course('MAT,90,94,ENG,92,88,CHM,80,NE', 3)
    'CHM,80,NE'
    """
    return transcript[(i-1) * 10 :(i-1) * 10 + 9]
    
def applied_to_degree(record, degree):
    """(str, str) -> bool
    
    Return True iff student represented by record applied to the degree
    
    >>>applied_to_degree('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BArts')
    True
    >>>applied_to_degree('Jacqueline Smith,Father Something High School,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', 'BSci')
    False
    """
    if degree in record:
        return True

def decide_admission(average, cutoff):
    """ (number, number) -> str
    
    Return accept, accept with scholarship and reject when average is above average, above threshold for scholarship and below average
    
    >>>decide_admission(90, 80)
    'accept with scholarship'
    >>>decide_admission(70, 75)
    'reject'
    >>>decide_admission(82, 80)
    'accept'
    """
    if average < cutoff:
        return 'reject'
    elif average < cutoff + 5:
        return 'accept'
    else:
        return 'accept with scholarship'
    