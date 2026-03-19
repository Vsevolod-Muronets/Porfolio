from EmotionDetection.emotion_detection import emotion_detector
import unittest

class TestEmotionDetection(unittest.TestCase):
    def test_emotion_detector(self):
        t_reslt1 = self.assertEqual(emotion_detector('I am glad this happened')['dominant_emotion'],'joy')
        t_reslt2 = self.assertEqual(emotion_detector('I am really mad about this')['dominant_emotion'],'anger')
        t_reslt3 = self.assertEqual(emotion_detector('I feel disgusted just hearing about this')['dominant_emotion'],'disgust')
        t_reslt4 = self.assertEqual(emotion_detector('I am so sad about this')['dominant_emotion'],'sadness')
        t_reslt5 = self.assertEqual(emotion_detector('I am really afraid that this will happen')['dominant_emotion'],'fear')

if __name__ == '__main__':
    unittest.main()