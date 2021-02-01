from django.shortcuts import render
from summarizer import Summarizer
import requests
from newspaper import fulltext

from .forms import QueryForm
from Scrapers.controller import Controller

summarizer = Summarizer()

def getArticleText(url):
    return fulltext(requests.get(url).text)

def getSummary(text):
    result = summarizer(text, min_length=20, ratio=0.25)
    return "".join(result)

def NewsView(req):
    if req.method == 'POST':
        form = QueryForm(req.POST)
        data = Controller().controller('headlines', req.POST['query'])
        data = data['GoogleNews']
        main = data[0]
        summary = getSummary(getArticleText(data[0]['link']))
        main['summary'] = summary
        return render(
            req, 
            'news.html',
            {
                'main': main,
                'data': list(data[1:]),
                'form': form
            }
        )
    else:
        form = QueryForm()
        return render (req, 'news.html', {'form': form})
