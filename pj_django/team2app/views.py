from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.shortcuts import render
from django.template import loader

from pymongo import mongo_client
url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['test0805']

import pandas as pd
df=col.find({},{'_id':0})
df=pd.DataFrame(df)
#진료종료시간(야간진료 18시이후 기준)
endtime=df.copy()
endtime['진료종료시간_월']=endtime['진료종료시간_월'].fillna(0)
endtime['진료종료시간_화']=endtime['진료종료시간_화'].fillna(0)
endtime['진료종료시간_수']=endtime['진료종료시간_수'].fillna(0)
endtime['진료종료시간_목']=endtime['진료종료시간_목'].fillna(0)
endtime['진료종료시간_금']=endtime['진료종료시간_금'].fillna(0)
endtime['진료종료시간_토']=endtime['진료종료시간_토'].fillna(0)
endtime = endtime[(endtime['진료종료시간_월']>1800) |(endtime['진료종료시간_화'] >1800) | (endtime['진료종료시간_수']>1800) |(endtime['진료종료시간_목']>1800) |(endtime['진료종료시간_금']>1800)]
#타입변환(응급실운영여부)
df.iloc[:,[9,10]]=df.iloc[:,[9,10]].astype(str)
# 진료시간
row=list(range(11,23))
df.iloc[:,row]=df.iloc[:,row].fillna(0)
df.iloc[:,row]=df.iloc[:,row].astype(int)
df.iloc[:,row]=df.iloc[:,row].astype(str)
days=['월','화','수','목','금','토']
df2=pd.DataFrame(columns = ['진료시간_월', '진료시간_화', '진료시간_수','진료시간_목','진료시간_금','진료시간_토'])
for x in df.index:
    for y in days:
        if df.loc[x,'진료시작시간_{}'.format(y)]=='0':
            df.loc[x,'진료시작시간_{}'.format(y)]='-'
        if df.loc[x,'진료종료시간_{}'.format(y)]=='0':
            df.loc[x,'진료종료시간_{}'.format(y)]='-'    
        else:
            df.loc[x,'진료시작시간_{}'.format(y)]=str(df.loc[x,'진료시작시간_{}'.format(y)])[:-2]+":"+str(df.loc[x,'진료시작시간_{}'.format(y)])[-2:]
            df.loc[x,'진료종료시간_{}'.format(y)]=str(df.loc[x,'진료종료시간_{}'.format(y)])[:-2]+":"+str(df.loc[x,'진료종료시간_{}'.format(y)])[-2:]
        df2.loc[x,'진료시간_{}'.format(y)]=str(y)+" "+str(df.loc[x,'진료시작시간_{}'.format(y)])+"~"+str(df.loc[x,'진료종료시간_{}'.format(y)])
        if '-~-' in df2.loc[x,'진료시간_{}'.format(y)]:
            df2.loc[x,'진료시간_{}'.format(y)]=df2.loc[x,'진료시간_{}'.format(y)].replace('-~-','-')
df=df.drop(df.columns[row],axis=1)
df=pd.concat([df,df2],axis=1)
#오늘 요일/현재시간 구하기
# from datetime import datetime
# def whatday():
#     whattoday = datetime.today().weekday()
#     whattime = datetime.now()
#     return whattoday,whattime

#df 열이름 변경
df=df.rename(columns={'요양기관명':'hosname'})
df=df.rename(columns={'주소':'address'})
df=df.rename(columns={'전화번호':'telnumber'})
df=df.rename(columns={'진료시간_월':'mon'})
df=df.rename(columns={'진료시간_화':'tue'})
df=df.rename(columns={'진료시간_수':'wed'})
df=df.rename(columns={'진료시간_목':'thur'})
df=df.rename(columns={'진료시간_금':'fri'})
df=df.rename(columns={'진료시간_토':'sat'})
df=df.rename(columns={'응급실 주간운영여부':'emgday'})
df=df.rename(columns={'응급실 야간운영여부':'emgnight'})
search_list=df[['hosname','address','telnumber','mon','tue','wed','thur','fri','sat','emgday','emgnight']]
search_lists=pd.DataFrame()  

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

def map(request):
    return render(request,'map.html')

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


from django.urls import reverse 
from django.utils import timezone
from .models import Review,Event

def review(request):
    temlate = loader.get_template('review.html')
    address =  Review.objects.all().values()
    context = {
        'address': address
    }
    return HttpResponse(temlate.render(context, request))


def rwrite(request):
    temlate = loader.get_template('rwrite.html')
    return HttpResponse(temlate.render({}, request))   

def rwrite(request):
    temlate = loader.get_template('rwrite.html')
    return HttpResponse(temlate.render({}, request))   

def rwrite_ok(request):
    title = request.POST['subject']
    writer = request.POST['users']
    content = request.POST['content']
    inquiry = request.POST['inquiry']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    address = Review(subject=title, users=writer ,content=content, rdate=nowDatetime ,inquiry=inquiry)
    print(address)
    address.save()
    return HttpResponseRedirect(reverse('review'))

# def event(request, id):
#     hospitalname = request.POST['title']
#     eventname = request.POST['writer']
#     nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#     img_address = request.POST['']
#     content = request.POST['content']
#     address = Event(subject=hospitalname, users=eventname, rdate=nowDatetime,img=img_address,con=content)
#     address.save()
#     return HttpResponseRedirect(reverse('event')) #입력글쓰기 필요 X


def event(request):
    temlate = loader.get_template('event.html')
    event = Event.objects.all().values()
    context={
        'event':event
    }
    return HttpResponse(temlate.render(context, request))   

def econtent(request,id):
    template = loader.get_template('econtent.html')
    event = Event.objects.get(id=id)
    context = {
        'event' : event,
    }
    return HttpResponse(template.render(context,request))