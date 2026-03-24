# TO DO
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer
import unittest

class TestSentimentAnalysis(unittest.TestCase):
    def test_sentiment_analyzer(self):
        t_reslt1 = self.assertEqual(sentiment_analyzer('I love working with Python')['label'],'SENT_POSITIVE')
        t_reslt2 = self.assertEqual(sentiment_analyzer('I hate working with Python')['label'],'SENT_NEGATIVE')
        t_reslt3 = self.assertEqual(sentiment_analyzer('I am neutral on Python')['label'],'SENT_NEUTRAL')

if __name__ == '__main__':
    unittest.main()