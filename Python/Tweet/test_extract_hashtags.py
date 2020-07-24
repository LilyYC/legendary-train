import unittest
import tweets


class TestExtractHashtags(unittest.TestCase):

    def test_no_hashtags(self):
        """ Test extract_hashtags with a tweet with no hashtags. """

        actual_hashtags = tweets.extract_hashtags('this is a tweet!')
        expected_hashtags = []
        self.assertEqual(actual_hashtags, expected_hashtags, 'empty list')

    def test_unique_hashtags(self):
        """ Test extract_hashtags with a tweet with unique hashtags. """
        
        actual_hashtags = tweets.extract_hashtags('#Life #keep #hi-')
        expected_hashtags = ['life', 'keep', 'hi']
        self.assertEqual(actual_hashtags, expected_hashtags, 'many hashtags')
    
    def test_repeated_hashtags(self):
        """ Test extract_hashtags with a tweet with repeated hashtags. """
        
        actual_hashtags = tweets.extract_hashtags('#Life #keep, #Life!')
        expected_hashtags = ['life', 'keep']
        self.assertEqual(actual_hashtags, expected_hashtags, 'unique hashtags') 


# Place your unit test definitions before this line.
if __name__ == '__main__':
    unittest.main(exit=False)
