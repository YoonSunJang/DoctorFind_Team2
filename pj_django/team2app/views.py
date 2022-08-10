from locale import resetlocale
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.shortcuts import render,redirect
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
col1 = db['hospital_list']
col2 = db['healthinfo'] #재용

import pandas as pd
hsdb = col2.find() #재용
df_hs = pd.DataFrame(list(hsdb)) #재용
df=col1.find({},{'_id':0})
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
df=df.rename(columns={'병원홈페이지(URL)':'url'})
df=df.rename(columns={'진료과목':'subject'})
df=df.rename(columns={'총의사수':'doctors'})
search_list=df[['hosname','address','telnumber','mon','tue','wed','thur','fri','sat','emgday','emgnight','url','subject','doctors']]
search_lists=pd.DataFrame()  

def index(request):
    return render(request,'index.html')

from django.core.paginator import Paginator
from datetime import datetime
#검색
def search(request):
    global search_list, search_lists
    input1=request.GET.get("input1") #지역권
    input2=request.GET.get("input2") #시/도
    input3=request.GET.get("input3") #시/군/구
    name=request.GET.get("name") #병원이름
    check1=request.GET.get("check1") #진료중
    check2=request.GET.get("check2") #야간진료
    check3=request.GET.get("check3") #공휴일진료
    check4=request.GET.get("check4") #응급실주간
    check5=request.GET.get("check5") #응급실야간

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
        if(check2=='true'): #야간진료 > 확인필요
             search_lists=search_lists.loc[endtime.index,:]
        if(check4=='true'): #응급실주간운영여부
            search_lists=search_lists[search_lists['emgday'].str.contains('Y')]
        if(check5=='true'): #응급실야간운영여부
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

from .models import Member1, Review1
from django.utils import timezone
def review(request):
    return render(request,'review.html')
    temlate = loader.get_template('review.html')
    review =  Review1.objects.all().values()
    context = {
        'review': review, 
    }
    return HttpResponse(temlate.render(context, request))
def rwrite(request):
    temlate = loader.get_template('rwrite.html')
    return HttpResponse(temlate.render({}, request))  

def rwrite_ok(request):
    subject = request.POST['subject']
    writer = request.POST['writer']
    content = request.POST['content']
    hosname = request.POST['hosname']
    # rating = request.POST['rating']
    # views = request.POST['views']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    review = Review1(writer=writer,email="bor@naver.com",subject=subject,content=content,hosname=hosname,rdate=nowDatetime,views='1')
    review.save()
    return HttpResponseRedirect(reverse('review'))

def rcontent(request,id):
    template = loader.get_template('rcontent.html')
    review = Review1.objects.get(id=id)
    context = {
        'review' : review,
    }
    return HttpResponse(template.render(context,request))

def rdelete(request,id):
    review = Review1.objects.get(id=id)
    review.delete()
    return HttpResponseRedirect(reverse('review'))

def rupdate(request,id):
    template = loader.get_template('rupdate.html')
    review = Review1.objects.get(id=id)
    context = {
        'review' : review,
    }
    return HttpResponse(template.render(context,request))

def rupdate_ok(request,id):
    template = loader.get_template('rupdate.html')
    review = Review1.objects.get(id=id)
    subject = request.POST['subject']
    # hosname = request.POST['hosname']
    # rating = request.POST['rating']
    content = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    review.subject=subject
    review.content=content
    # review.hosname=hosname
    # review.rating=rating
    review.rdate=nowDatetime
    review.save()
    return HttpResponseRedirect(reverse('review'))

def map(request):
    temlate = loader.get_template('map.html')
    context = {
    }
    print("11111111111111111111111111111111111111111111")
  
   
    return HttpResponse(temlate.render(context, request))




def login(request):
    return render(request,'login.html')

def login_ok(request):
    email = request.POST.get('email', None)
    pw = request.POST.get('pw', None)
    try:
        member=Member1.objects.get(email=email)
    except Member1.DoesNotExist:
        member = None
    # print("member", member)
    result = 0
    if member != None:
        print("해당 email회원 존재함")
        if member.pw == pw:
            print("비밀번호까지 일치")
            result = 2
            
            print("member.email", member.email)
            request.session['login_ok_user'] = member.email
        else:
            print("비밀번호 틀림")
            result = 1
    else:
        print("해당 email회원 존재하지 않음") 
        result = 0   
			
    template = loader.get_template("login_ok.html")
    context = {
        'result': result, 
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    if request.session.get('login_ok_user'):
        del request.session['login_ok_user']
    return redirect("../")
    

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phoneNum = request.POST['phoneNum']
        pw = request.POST['pw']
        addr = request.POST['addr']
        # print("이름:", name, "아이디(email):", email, "전화번호", phone, "비번", pw, "주소", addr)
        
        member = Member1(
            name=name,
            email=email,
            phoneNum=phoneNum,
            pw=pw,
            addr=addr
        )
        member.save()
        return HttpResponseRedirect('../login')
    else:
        return render(request,'signup.html')

def healthinfo(request):
    template = loader.get_template('healthinfo.html')
    dr = df_hs[['제목', '월']]
    dt = dr[dr['월']==1]
    dy = dt['제목'].to_list()
    # subhealth = df['제목']
    # contentshealth = df['내용']
    # print(dy)
    context = {
        'dy' : dy,
    }
    return HttpResponse(template.render(context, request))

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