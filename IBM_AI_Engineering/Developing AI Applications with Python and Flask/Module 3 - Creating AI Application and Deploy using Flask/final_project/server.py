'''This app is to run NLP emotion analysis of a given statement.
'''
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask('Emotion Detection')

@app.route('/')
def render_index_page():
    '''This function renders home page.
    '''
    return render_template('index.html')

@app.route('/emotionDetector')
def sent_detector():
    '''This function processes the input text with NLP
    and return the result of emotion analysis of the text if the
    input is not empty. Returns error message if the input is empty.
    '''
    resp = emotion_detector(request.args.get('textToAnalyze'))

    if resp['dominant_emotion'] is None:
        return 'Invalid text! Please try again!'

    return (
        f"For the given statement, the system response is "
        f"'anger': {resp['anger']}, 'disgust': {resp['disgust']}, "
        f"'fear': {resp['fear']}, 'joy': {resp['joy']} and 'sadness': "
        f"{resp['sadness']}. The dominant emotion is {resp['dominant_emotion']}."
    )

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
