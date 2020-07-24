import unittest
import tweets


class TestCommonWords(unittest.TestCase):

    def test_none_removed(self):
        """ Test common_words with N so that no words are removed. """

        words_to_counts = {'cat': 1}
        expected_result = {'cat': 1}
        tweets.common_words(words_to_counts, 1)
        self.assertEqual(words_to_counts, expected_result, 'none removed')

    def test_tie_removed(self):
        """ Test common_words with N so that tied words are removed. """
        
        dic = {'I': 10, 'you': 5, 'miss': 8, 'here': 6, 'how': 6}
        tweets.common_words(dic, 3)
        expect_result = {'I': 10, 'miss': 8} 
        self.assertEqual(dic, expect_result)
    
    def test_tie_remained(self):
        """ Test common_words so that tied words within N are remained. """
        
        dic = {'we': 6, 'how': 3, 'love':6, 'CS': 6}
        tweets.common_words(dic, 3)
        expect_result = {'we': 6, 'love':6, 'CS': 6}
        self.assertEqual(dic, expect_result)
    
    def test_no_ties(self):
        """ Test common_words with N with no ties. """
        
        dic = {'I':10, 'finally': 5, 'done': 8, 'haha': 2, 'nice': 6}
        tweets.common_words(dic, 4)
        expect_result = {'I':10, 'done': 8, 'nice': 6, 'finally': 5}
        self.assertEqual(dic, expect_result)

    def test_no_input(self):
        """ Test common_words with empty input. """
        
        dic = {}
        tweets.common_words(dic, 2)
        expect_result = {} 
        self.assertEqual(dic, expect_result)        


# Place your unit test definitions before this line.
if __name__ == '__main__':
    unittest.main(exit=False)
