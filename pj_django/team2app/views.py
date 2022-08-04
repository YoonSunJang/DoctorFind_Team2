from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from asyncio.windows_events import NULL
from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
############################################몽고db 1.병원정보서비스 2022.6.xlsx ################################# psi


# from pymongo import mongo_client

# url = 'mongodb://localhost:27017/'
# mgClient = mongo_client.MongoClient(url)
# db = mgClient['0804_team2']
# col = db['0804_HospitalList']


# a= col.find()
# for x in a:
#     print("col: ",x)
        
        



############################################몽고db 1.병원정보서비스 2022.6.xlsx ################################# psi

def index(request):
    return render(request,'index.html')

def search(request):
    return render(request,'search.html')

def review(request):
    return render(request,'review.html')

def map(request):
    return render(request,'map.html')


def map_ok(request):
    number = request.POST["num1"]
    print("num:",number)
    return HttpResponseRedirect(reverse('map'))


def login(request):
    return render(request,'login.html')

