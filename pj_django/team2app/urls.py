from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/search_ok/', views.search_ok, name='search_ok'),
    path('review/', views.review, name='review'),
    path('rwrite/', views.rwrite, name='rwrite'),
    path('map/', views.map, name='map'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('healthinfo/', views.healthinfo, name='healthinfo'),
    path('event/', views.event, name='event'),
    path('mypage/', views.mypage, name='mypage'),
]