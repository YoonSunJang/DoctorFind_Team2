from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/search_ok/', views.search_ok, name='search_ok'),
    path('review/', views.review, name='review'),
    path('map/', views.map, name='map'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('healthinfo/', views.healthinfo, name='healthinfo'),
    path('event/', views.event, name='event'),
    path('mypage/', views.mypage, name='mypage'),
    path('rwrite/', views.rwrite, name='rwrite'),
    path('rwrite/rwrite_ok/', views.rwrite_ok, name='rwrite_ok'),
    path('event/event', views.event, name='event'),
    path('econtent/<int:id>', views.econtent, name='econtent'),

]