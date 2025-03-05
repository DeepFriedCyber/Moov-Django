# property_search/urls.py

from django.urls import path
from . import views

app_name = 'property_search'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.PropertySearchView.as_view(), name='search'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
]