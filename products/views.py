from django.shortcuts import render
import re

from .forms import QueryForm
from Scrapers.controller import Controller

def ProductsView(req):
	if req.method == 'POST':
		form = QueryForm(req.POST)
		data = Controller().controller('product', req.POST['query'])
		data = [] if data==None else [*data['Flipkart'], *data['Amazon']]
		data = sorted(data, key=lambda p: int(re.sub(r'[₹,]', '', p['price'])))
		
		return render(
			req, 
			'products.html', 
			{'data': data, 'form': form}
		)
	else:
		form = QueryForm()
		return render(
			req, 
			'products.html', 
			{'data': [], 'form':form}
		)
