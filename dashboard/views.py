import json
import pickle
import re

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from nltk import WordNetLemmatizer

from dashboard.models import Sentiment
from web.settings import BASE_DIR


def preprocess(textdata):
    processedText = []

    # Create Lemmatizer and Stemmer.
    word_lemm = WordNetLemmatizer()

    # Defining regex patterns.
    url_pattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    user_pattern = '@[^\s]+'
    alpha_pattern = "[^a-zA-Z0-9]"
    sequence_pattern = r"(.)\1\1+"
    seq_replace_pattern = r"\1\1"

    for tweet in textdata:
        # Defining dictionary containing all emojis with their meanings.
        emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
                  ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
                  ':-@': 'shocked', ':@': 'shocked', ':-$': 'confused', ':\\': 'annoyed',
                  ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
                  '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
                  '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
                  ';-)': 'wink', 'O:-)': 'angel', 'O*-)': 'angel', '(:-D': 'gossip', '=^.^=': 'cat'}

        ## Defining set containing all stopwords in Bahasa Indonesia.
        stopword_df = pd.read_csv(BASE_DIR / 'static/csv/stopwordbahasa.csv', header=None)
        stopwordlist = stopword_df[0].to_list()

        tweet = tweet.lower()

        # Replace all URls with 'URL'
        tweet = re.sub(url_pattern, ' URL', tweet)
        # Replace all emojis.
        for emoji in emojis.keys():
            tweet = tweet.replace(emoji, "EMOJI" + emojis[emoji])
            # Replace @USERNAME to 'USER'.
        tweet = re.sub(user_pattern, ' USER', tweet)
        # Replace all non alphabets.
        tweet = re.sub(alpha_pattern, " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(sequence_pattern, seq_replace_pattern, tweet)

        tweetwords = ''
        for word in tweet.split():
            # Checking if the word is a stopword.
            # if word not in stopwordlist:
            if len(word) > 1:
                # Lemmatizing the word.
                word = word_lemm.lemmatize(word)
                tweetwords += (word + ' ')

        processedText.append(tweetwords)

    return processedText


def load_model():
    file = open(BASE_DIR / 'static/models/vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()

    file = open(BASE_DIR / 'static/models/Sentiment-SVC.pickle', 'rb')
    model = pickle.load(file)
    file.close()

    return vectoriser, model


def predict(text):
    vectoriser, model = load_model()

    vector = vectoriser.transform(preprocess(text))
    sentiment = model.predict(vector)

    return sentiment.tolist()

# Create your views here.
def index(request):
    sentiment = Sentiment.objects.all()
    total_negative = sum(entry.total for entry in sentiment if entry.label == 'negative')
    total_neutral = sum(entry.total for entry in sentiment if entry.label == 'neutral')
    total_positive = sum(entry.total for entry in sentiment if entry.label == 'positive')

    return render(request, 'index.html', {
        'total_negative': total_negative,
        'total_neutral': total_neutral,
        'total_positive': total_positive
    })


def tools(request):
    return render(request, 'tools.html')


@csrf_exempt
def check(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        sentiment_label = ['Negative', 'Neutral', 'Positive']
        sentiment = predict([data['text']])[0]

        return JsonResponse({
            'result': sentiment_label[sentiment]
        })
