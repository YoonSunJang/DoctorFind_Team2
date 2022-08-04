from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from pymongo import mongo_client

url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['test0725']
col = db['HospitalList1']

a = col.find()
for x in a:
    print("col: ", x)

def index(request):
    return render(request,'index.html')

def search(request):
    return render(request,'search.html')

def review(request):
    return render(request,'review.html')

def map(request):
    return render(request,'map.html')

def login(request):
    return render(request,'login.html')

def healthinfo(request):
    return render(request,'healthinfo.html')