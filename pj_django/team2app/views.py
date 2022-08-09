from locale import resetlocale
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

from pymongo import mongo_client
url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['test0805']

import pandas as pd


#오늘 요일/현재시간 구하기
# from datetime import datetime
# def whatday():
#     whattoday = datetime.today().weekday()
#     whattime = datetime.now()
#     return whattoday,whattime

#df 열이름 변경


def index(request):
    return render(request,'index.html')

from django.core.paginator import Paginator
from datetime import datetime
def search(request):
    global search_list, search_lists
    #검색
    input1=request.GET.get("input1") #지역권
    input2=request.GET.get("input2") #시/도
    input3=request.GET.get("input3") #시/군/구
    name=request.GET.get("name") #병원이름
    check1=request.GET.get("check1") #진료중
    check2=request.GET.get("check2") #야간진료
    check3=request.GET.get("check3") #공휴일진료
    check4=request.GET.get("check4") #응급실주간
    check5=request.GET.get("check5") #응급실야간
    # print("1")
    # print(input1)
    # print(input2)
    # print(input3)
    # print(name)
    # print("check1",check1)
    # print("check2",check2)
    # print("check3",check3)
    # print("check4",check4)
    # print("check5",check5)
    whattoday = datetime.today().weekday()
    whattime = datetime.now()
    if(input1==input2==input3==name==check4==check5==None):pass
    else:
        search_lists=search_list
        if(name!=None):
            search_lists=search_lists[search_lists['hosname'].str.contains(name)]
        if(input1!='지역권 선택' and input2!='시/도 선택'):
            if(input3!='시/군/구 선택'):
                search_lists=search_lists[search_lists['address'].str.contains(input3)]
            search_lists=search_lists[search_lists['address'].str.contains(input2)]
        if(check2=='true'): #야간진료
             search_lists=search_lists.loc[endtime.index,:]
        if(check4=='true'):
            search_lists=search_lists[search_lists['emgday'].str.contains('Y')]
        if(check5=='true'):
            search_lists=search_lists[search_lists['emgnight'].str.contains('Y')]
        
    print('search_lists',search_lists)
    page=request.GET.get("page",1)
    paginator=Paginator(search_lists.to_dict('records'),10) # 페이지 표시 수
    page_obj = paginator.get_page(page)
    context={
        'search_list':search_lists.to_dict('records'),
        'page_obj':page_obj,
        'today':whattoday,
    }

    return render(request,'search.html',context=context)

def search_ok(request):
    return HttpResponseRedirect(reverse('search'))

def review(request):
    return render(request,'review.html')
4
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
    
    df2 =  df2[['요양기관명','y좌표','x좌표']]
   
    num=len(df2)
    context = {
        'mlist': mlist,
        'lat' : lat,
        'long' : long,
        'df2' : df2.to_dict('records'),
        'num':num,
    }
    
    print("df2.to_dict('records')",df2.to_dict('records'))
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
############################################몽고db 1.병원정보서비스 2022.6.xlsx ################################# psi