from multiprocessing import context
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from asyncio.windows_events import NULL
from re import template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

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


def map_ok(request):
    mname=request.POST['inputname']
    temlate = loader.get_template('map.html')
    where = {"요양기관명":{"$regex":""+str(mname)+""}}
    mdocs = col.find(where)
    for doc in mdocs:  
        #dox = mdocs.at[doc, '요양기관명']
        print(doc)
    context = {
        'doc': doc, 
    }
    return HttpResponse(temlate.render(context, request))

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def healthinfo(request):
    return render(request,'healthinfo.html')

def event(request):
    return render(request,'event.html')

def mypage(request):
    return render(request,'mypage.html')


############################################몽고db 1.병원정보서비스 2022.6.xlsx ################################# psi
from pymongo import mongo_client

url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['0804_team2']
col = db['0804_HospitalList']
# map_dics=[]
# map_ds={}
# map_ds['x좌표']=input  #######인서트
# map_dics.append(map_ds)
# col.insert_many(map_dics)




# a= col.find()
# for x in a:
#     print("col: ",x)
############################################몽고db 1.병원정보서비스 2022.6.xlsx ################################# psi