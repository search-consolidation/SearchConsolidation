from django.shortcuts import render
from joblib import load
import os
from django.conf import settings

from Scrapers.controller import Controller

# with open(os.path.join(settings.BASE_DIR, 'news_classifier.joblib'), 'rb') as f:
model = load(os.path.join(settings.BASE_DIR, 'news_classifier.joblib'))
tfidf = load(os.path.join(settings.BASE_DIR, 'tfidf.joblib'))
cats = [
    'Atheism',
    'Graphics',
    'Hardware',
    'Hardware',
    'Software',
    'Software',
    'For Sale',
    'Politics',
    'Politics',
    'Sports',
    'Sports',
    'Security',
    'Electronics',
    'Medicine',
    'Space',
    'Religion',
    'War and Weapons',
    'Middle East',
    'Politics',
    'Religious Talks'
]

def predict(text):
	if text != None:
		vector = tfidf.transform([text])
		pred = model.predict(vector)
		return cats[pred[0]]

def NewsView(req):
	data = Controller().controller('headlines')
	data = data['NDTV'].values()
	for news in data:
		news['category'] = predict(news['text'])
	return render(
		req, 
		'news.html',
		{
			'toi': list(data),
			'author': 'Times of India'
		}
	)
