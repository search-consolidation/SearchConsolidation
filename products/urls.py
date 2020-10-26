from django.urls import path
from .views import ProductsView

urlpatterns = [
	path('', ProductsView, name='product'),
]