from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('search/search_ok/', views.search_ok, name='search_ok'),
    path('review/', views.review, name='review'),  
    path('map/', views.map, name='map'),
    path('map/map_ok/', views.map_ok, name='map_ok'),
    path('login/', views.login, name='login'),
    path('login/login_ok/', views.login_ok, name='login_ok'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('healthinfo/', views.healthinfo, name='healthinfo'),
    path('event/', views.event, name='event'),
    path('mypage/', views.mypage, name='mypage'),
    path('rwrite/', views.rwrite, name='rwrite'),
    path('rwrite/rwrite_ok/', views.rwrite_ok, name='rwrite_ok'),
    path('rcontent/<int:id>', views.rcontent, name='rcontent'),
    path('rdelete/<int:id>', views.rdelete, name='rdelete'),
    path('rupdate/<int:id>', views.rupdate, name='rupdate'),
    path('rupdate/rupdate_ok/<int:id>', views.rupdate_ok, name='rupdate_ok'),   
]