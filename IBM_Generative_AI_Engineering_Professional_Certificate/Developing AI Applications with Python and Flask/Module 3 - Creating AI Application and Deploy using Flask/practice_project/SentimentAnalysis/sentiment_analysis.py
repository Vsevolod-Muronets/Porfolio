# TO DO
import requests
import json

def sentiment_analyzer(text_to_analyse):
    url = 'https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/SentimentPredict'
    header = {'grpc-metadata-mm-model-id': 'sentiment_aggregated-bert-workflow_lang_multi_stock'}
    myobj = { 'raw_document': {'text': text_to_analyse} }
    response = requests.post(url, json = myobj, headers=header)
    frmtd_resp = json.loads(response.text)

    if response.status_code == 200:
        label = frmtd_resp['documentSentiment']['label']
        score = frmtd_resp['documentSentiment']['score']
    elif response.status_code == 500:
        label = None
        score = None

    return {'label': label, 'score': score}