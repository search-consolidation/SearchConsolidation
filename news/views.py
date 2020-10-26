from django.shortcuts import render
from Scrapers.controller import Controller

def NewsView(req):
	data = Controller().controller('headlines')
	return render(
		req, 
		'news.html', 
		{
			'toi': data['TimesofIndia'].values(),
			'author': 'Times of India'
		}
	)
