from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.shortcuts import render
from django.template import loader
import pandas as pd
from pymongo import mongo_client

url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['healthinfo']
hsdb = col.find()
df = pd.DataFrame(list(hsdb))
    
def index(request):
    return render(request,'index.html')

def search(request):
    input1=request.GET.get("input1")
    input2=request.GET.get("input2")
    input3=request.GET.get("input3")
    print(input1)
    print(input2)
    print(input3)
    return render(request,'search.html')

def search_ok(request):
    # input1=request.POST['input1']
    # input2=request.POST['input2']
    # input3=request.POST['input3']
    name=request.POST['inputname']
    print(name)
    return HttpResponseRedirect(reverse('search'))

def review(request):
    return render(request,'review.html')

def map(request):
    return render(request,'map.html')

def login(request):
    return render(request,'login.html')


def healthinfo(request):
    template = loader.get_template('healthinfo.html')
    dr = df[['제목', '월']]
    dt = dr[dr['월']==1]
    dy = dt['제목'].to_list()
    # subhealth = df['제목']
    # contentshealth = df['내용']
    print(dy)
    context = {
        'dy' : dy,
    }
    return HttpResponse(template.render(context, request))

def signup(request):
    return render(request,'signup.html')
def event(request):
    return render(request,'event.html')

def mypage(request):
    return render(request,'mypage.html')
