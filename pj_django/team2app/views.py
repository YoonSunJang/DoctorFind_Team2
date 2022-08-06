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
import pandas as pd
def index(request):
    return render(request,'index.html')

def search(request):
    input1=request.GET.get("input1")
    input2=request.GET.get("input2")
    input3=request.GET.get("input3")
    name=request.GET.get("name")
    print(1)
    if(input1==input2==input3==name==None):pass
    else:
        print(input1)
        print(input2)
        print(input3)
        print(name)
    print(2)
    return render(request,'search.html')

def search_ok(request):
    return HttpResponseRedirect(reverse('search'))

def review(request):
    return render(request,'review.html')

def rwrite(request):
    return render(request,'rwrite.html')

def map(request):
    return render(request,'map.html')


def map_ok(request):
    mname=request.POST['inputname']
    temlate = loader.get_template('map.html')
    where = {"요양기관명":{"$regex":""+str(mname)+""}}
    mdocs = col.find(where)
    df = pd.DataFrame(list(mdocs))
    df2 = df.dropna(subset=['y좌표','x좌표'])
    mlist = df['요양기관명'].to_list()
    for doc in mlist:  
        print(doc)
        
    df2[['요양기관명','y좌표','x좌표']]
    lat = df2['x좌표'].mean()
    long = df2['y좌표'].mean()
    a=[]
    b=[]
    for i in df2.index:
        sub_lat = df2.at[i, 'x좌표']
        sub_long = df2.at[i, 'y좌표']
        title = df2.at[i, '요양기관명']
        
        #print([sub_long, sub_lat],title)
        a.append(sub_lat)
        b.append(sub_long)
    df2 =  df2[['요양기관명','y좌표','x좌표']]
    
    m1 =  df2['요양기관명']
    m2 = df2['y좌표']
    m3 = df2['x좌표']
    num=len(df2)
    
    context = {
        'mlist': mlist,
        'sub_lat' : sub_lat,
        'sub_long' : sub_long,
        'title' : title,
        'lat' : lat,
        'long' : long,
        'xy' : (sub_lat, sub_long),
        'df2' : df2.to_dict('records'),
        'a' : a,
        'b' : b,
        'm1' : m1,
        'm2' : m2,
        'm3' : m3,
        'num':num,
       
        
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