from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('review/', views.review, name='review'),
    path('map/', views.map, name='map'),
    path('login/', views.login, name='login'),
]