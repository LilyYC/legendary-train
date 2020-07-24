SPECIAL_CASE_SCHOOL_1 = 'Fort McMurray Composite High'
SPECIAL_CASE_SCHOOL_2 = 'Father Mercredi High School'
SPECIAL_CASE_YEAR = '2016'
NO_EXAM = 'NE'
REJECT = 'reject'
ACCEPT = 'accept'
ACCEPT_WITH_Scholarship = 'accept with scholarship'

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

    return (SPECIAL_CASE_YEAR in record) and (SPECIAL_CASE_SCHOOL_1 in record or SPECIAL_CASE_SCHOOL_2 in record)

    
def get_final_mark(record, course_mark, exam_mark):
    """ (str, str, str) -> float
    
    Return the final_mark as an average of course_mark and exam_mark for non special case, or as course_mark for special case.
    
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,94,ENG,92,88,CHM,80,85,BArts', '90', '94')
    92.0
    >>>get_final_mark('Jacqueline Smith,Father Something High School,2015,MAT,90,NE,ENG,92,88,CHM,80,NE,BArts', '94', 'NE')
    47.0
    >>>get_final_mark('Jacqueline Smith,Fort McMurray Composite High,2016,MAT,90,NE,ENG,92,88,CHM,80,NE,BArts', '90', 'NE')
    90.0
    """
    
    if NO_EXAM not in exam_mark:
        return (int(course_mark) + int(exam_mark)) / 2
    elif not is_special_case(record):
        return float(course_mark) / 2
    else:
        return float(course_mark)
    
def get_both_marks(course_record, course_code):
    """(str, str) -> str
    
    Return the course_mark and exam_mark as a single string in the form:
    course_mark exam_mark
    when the course_record matches with the course_code.
    
    >>>get_both_marks('MAT,90,94', 'MAT')
    '90 94'
    >>>get_both_marks('MAT,90,94', 'ENG')
    ''
    """
    if course_code in course_record:
        return course_record[4:6] + ' ' + course_record[7:9]
    else:
        return ''
    
def extract_course(transcript, course_i):
    """(str, int) -> str
        
    Return the ith course transcript record as a single string in the form:
    course_code,course_mark,exam_mark     
    from the transcript
    
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
    
    return degree in record


def decide_admission(average, cutoff):
    """ (number, number) -> str
    
    Return accept, accept with scholarship or reject when average is above 
    cutoff, above threshold for scholarship or below cutoff
    
    >>>decide_admission(90, 80)
    'accept with scholarship'
    >>>decide_admission(70, 75)
    'reject'
    >>>decide_admission(82, 80)
    'accept'
    """
    
    if average < cutoff:
        return REJECT
    elif average < cutoff + 5:
        return ACCEPT
    else:
        return ACCEPT_WITH_Scholarship