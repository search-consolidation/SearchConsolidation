from django.urls import path
from .views import NewsView

urlpatterns = [
	path('news', NewsView, name='news'),
	path('', NewsView, name='news'),
]