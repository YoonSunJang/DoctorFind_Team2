from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.shortcuts import render,redirect
from django.template import loader

from pymongo import mongo_client
url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col1 = db['hospital_list']
col2 = db['healthinfo'] #재용

import pandas as pd
hsdb = col2.find() #재용
df_hs = pd.DataFrame(list(hsdb)) #재용
df=col1.find({},{})
df=pd.DataFrame(df)
#진료종료시간(야간진료 18시이후 기준)
endtime=df.copy()
endtime['진료종료시간_월']=endtime['진료종료시간_월'].fillna(0)
endtime['진료종료시간_화']=endtime['진료종료시간_화'].fillna(0)
endtime['진료종료시간_수']=endtime['진료종료시간_수'].fillna(0)
endtime['진료종료시간_목']=endtime['진료종료시간_목'].fillna(0)
endtime['진료종료시간_금']=endtime['진료종료시간_금'].fillna(0)
endtime['진료종료시간_토']=endtime['진료종료시간_토'].fillna(0)
days=['월','화','수','목','금','토']

endtime1 = endtime[(endtime['진료종료시간_월']>1800) |(endtime['진료종료시간_화'] >1800) | (endtime['진료종료시간_수']>1800) |(endtime['진료종료시간_목']>1800) |(endtime['진료종료시간_금']>1800)]
#타입변환(응급실운영여부)
df.iloc[:,[10,11]]=df.iloc[:,[10,11]].astype(str)
# 진료시간
row=list(range(12,24))
df.iloc[:,row]=df.iloc[:,row].fillna(0)
df.iloc[:,row]=df.iloc[:,row].astype(int)
df.iloc[:,row]=df.iloc[:,row].astype(str)

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
        elif '-~' in df2.loc[x,'진료시간_{}'.format(y)]:
            df2.loc[x,'진료시간_{}'.format(y)]=df2.loc[x,'진료시간_{}'.format(y)].replace('-~','~')
        
df=df.drop(df.columns[row],axis=1)
df=pd.concat([df,df2],axis=1)
# 데이터정제
df['진료과목']=df['진료과목'].str.replace('과', '과/',regex=False)
df['진료과목']=df['진료과목'].str.rstrip("/")
df[['진료과목','전화번호','총의사수','병원홈페이지(URL)','일요일 휴진안내','공휴일 휴진안내']]=df[['진료과목','전화번호','총의사수','병원홈페이지(URL)','일요일 휴진안내','공휴일 휴진안내']].fillna('-')

#오늘 요일/현재시간 구하기
# from datetime import datetime
# def whatday():
#     whattoday = datetime.today().weekday()
#     whattime = datetime.now()
#     return whattoday,whattime

#df 열이름 변경
df.set_index('_id')
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
df=df.rename(columns={'일요일 휴진안내':'sunDoff'})
df=df.rename(columns={'공휴일 휴진안내':'holyoff'})
df=df.rename(columns={'_id':'num'})
search_list=df.copy()
search_lists=pd.DataFrame()  

def index(request):
    global viewplus, iname
    iname=request.GET.get("name")
    template = loader.get_template('index.html')
    now = datetime.now()
    thismonth = now.month
    dr = df_hs[['제목', '월', '내용']]
    dr = dr[dr['월']==thismonth]
    indt = dr.to_dict('records')
    indtdt = indt[1:4]
    indtdict = indt[0]
    infoheadline = indtdict['제목']
    try:
        review =  Review.objects.all().order_by('-id').values('subject')
        reviewheadline = review[0]['subject']
        reviewlinkheadline = Review.objects.filter(subject=reviewheadline).values('id').get()
        reviewlinkheadline = reviewlinkheadline['id']
        
    except:
        reviewheadline = "등록된 리뷰가 없습니다"
        reviewlinkheadline = "-"
    try:
        review1 = review[1]['subject']
        reviewlink1 = Review.objects.filter(subject=review1).values('id').get()
        reviewlink1 = reviewlink1['id']
    except:
        review1 = "등록된 리뷰가 없습니다"
        reviewlink1 = "-"
    try:
        review2 = review[2]['subject']
        reviewlink2 = Review.objects.filter(subject=review2).values('id').get()
        reviewlink2 = reviewlink2['id']
    except:
        review2 = "등록된 리뷰가 없습니다"
        reviewlink2 = "-"
    try:
        review3 = review[3]['subject']
        reviewlink3 = Review.objects.filter(subject=review3).values('id').get()
        reviewlink3 = reviewlink3['id']
    except:
        review3 = "등록된 리뷰가 없습니다"
        reviewlink3 = "-"
    try:
        event = Event.objects.all().order_by('-id').values('content')
        eventheadline = event[0]['content']
        event1 = event[1]['content']
        event2 = event[2]['content']
        event3 = event[3]['content']
        
        eventbanner = Event.objects.all().order_by('-id').values('img_address')
        eventbanner1 = eventbanner[0]['img_address']
        eventbanner2 = eventbanner[1]['img_address']
        eventbanner3 = eventbanner[2]['img_address']
        eventbanner4 = eventbanner[3]['img_address']
        eventbannertext = ""
        bannerlink1 = Event.objects.filter(img_address=eventbanner1).values('id').get()
        bannerlink2 = Event.objects.filter(img_address=eventbanner2).values('id').get()
        bannerlink3 = Event.objects.filter(img_address=eventbanner3).values('id').get()
        bannerlink4 = Event.objects.filter(img_address=eventbanner4).values('id').get()
        bannerlink1 = bannerlink1['id']
        bannerlink2 = bannerlink2['id']
        bannerlink3 = bannerlink3['id']
        bannerlink4 = bannerlink4['id']
    except:
        eventheadline = '등록된 이벤트가 없습니다'
        event1 = ""
        event2 = ""
        event3 = ""
        eventbanner1 = ""
        eventbanner2 = ""
        eventbanner3 = ""
        eventbanner4 = ""
        eventbannertext = "등록된 이벤트가 없습니다"
    eventlinkheadline = Event.objects.filter(content=eventheadline).values('id').get()
    event1link1 = Event.objects.filter(content=event1).values('id').get()
    event1link2 = Event.objects.filter(content=event2).values('id').get()
    event1link3 = Event.objects.filter(content=event3).values('id').get()
    eventlinkheadline = eventlinkheadline['id']
    event1link1 = event1link1['id']
    event1link2 = event1link2['id']
    event1link3 = event1link3['id']
    
    viewplus = request.GET.get("value")
    context = {
        'indtdt':indtdt, 'infoheadline' : infoheadline, 'reviewheadline':reviewheadline,
        'review1':review1, 'review2' : review2, 'review3': review3,
        'eventheadline' : eventheadline, 'event1':event1, 'event2':event2, 'event3':event3,
        'eventbanner1' : eventbanner1, 'eventbanner2' : eventbanner2, 'eventbanner3' : eventbanner3,
        'eventbanner4' : eventbanner4, 'eventbannertext' : eventbannertext,
        'bannerlink1': bannerlink1, 'bannerlink2': bannerlink2,'bannerlink3': bannerlink3,
        'bannerlink4': bannerlink4, 'eventlinkheadline' : eventlinkheadline, 'event1link1':event1link1, 'event1link2' :event1link2, 'event1link3':event1link3,
        'reviewlink1':reviewlink1,'reviewlink2':reviewlink2, 'reviewlink3':reviewlink3, 'reviewlinkheadline':reviewlinkheadline,
    }
    return HttpResponse(template.render(context, request))
    
    # 취합부분
    # review =  Review.objects.all().order_by('-id').values('subject')
    # # reviewheadline = review[0]['subject']
    # # print(reviewheadline)
    # # review1 = review[1]['subject']
    # # review2 = review[2]['subject']
    # # review3 = review[3]['subject']
    # event = Event.objects.all().order_by('-id').values('content')
    # eventheadline = event[0]['content']
    # event1 = event[1]['content']
    # event2 = event[2]['content']
    # event3 = event[3]['content']
    # eventbanner = Event.objects.filter(content=eventheadline).values('img_address').get()
    # eventbanner = eventbanner['img_address']
    # # context = {
    # #     'indtdt':indtdt, 'infoheadline' : infoheadline, 'reviewheadline':reviewheadline,
    # #     'review1':review1, 'review2' : review2, 'review3': review3,
    # #     'eventheadline' : eventheadline, 'event1':event1, 'event2':event2, 'event3':event3,
    # #     'eventbanner' : eventbanner,
    # # }
    # context = {
    #     'indtdt':indtdt, 'infoheadline' : infoheadline,
    #     'eventheadline' : eventheadline, 'event1':event1, 'event2':event2, 'event3':event3,
    #     'eventbanner' : eventbanner,
    # }
    # return HttpResponse(template.render(context, request))

def ing():
    global endtime
    hour=pd.datetime.now().hour
    minute=pd.datetime.now().minute
    whattoday = datetime.today().weekday()
    for x in range(0,7):
        if(whattoday==x):
            endtime=endtime[endtime['진료종료시간_{}'.format(days[x])]>int(str(hour)+str(minute))]

from django.core.paginator import Paginator
from datetime import datetime,timedelta
#검색
def search(request):
    global search_list, search_lists,endtime,iname
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
    
    if(input1==input2==input3==name==check4==check5==None):
        if(iname!=None):
            search_lists=search_list
            search_lists=search_lists[search_lists['hosname'].str.contains(iname)]
            iname=None
        else:
            pass
    else:
        search_lists=search_list     
        if(input1!='지역권 선택' and input2!='시/도 선택'):
            if(input3!='시/군/구 선택'):
                search_lists=search_lists[search_lists['address'].str.contains(input3)]
            search_lists=search_lists[search_lists['address'].str.contains(input2)]
        if(check1=='true'): #진료중
            ing()
            search_lists = search_lists[~search_lists["mon"].str.contains("-")]
            search_lists = search_lists[~search_lists["tue"].str.contains("-")]
            search_lists = search_lists[~search_lists["wed"].str.contains("-")]
            search_lists = search_lists[~search_lists["thur"].str.contains("-")]
            search_lists = search_lists[~search_lists["fri"].str.contains("-")]
            search_lists = search_lists[~search_lists["sat"].str.contains("-")]
            mergedata=pd.merge(search_lists,endtime,how='inner')
            search_lists=mergedata
            print(search_lists)
        if(check2=='true'): #야간진료 > 확인필요
            search_lists = search_lists[~search_lists["mon"].str.contains("-")]
            search_lists = search_lists[~search_lists["tue"].str.contains("-")]
            search_lists = search_lists[~search_lists["wed"].str.contains("-")]
            search_lists = search_lists[~search_lists["thur"].str.contains("-")]
            search_lists = search_lists[~search_lists["fri"].str.contains("-")]
            search_lists = search_lists[~search_lists["sat"].str.contains("-")]
            mergedata1=pd.merge(search_lists,endtime1,how='inner')
            search_lists=mergedata1
        if(check3=='true'): #공휴일진료
            search_lists = search_lists[~search_lists["holyoff"].str.contains("휴진")]
            search_lists = search_lists[~search_lists["holyoff"].str.contains("휴무")]
            search_lists = search_lists[~search_lists["holyoff"].str.contains("휴뮤")]
            search_lists = search_lists[~search_lists["holyoff"].str.contains("-")]
        if(check4=='true'): #응급실주간운영여부
            search_lists = search_lists[~search_lists["emgday"].str.contains("-")]
            search_lists=search_lists[search_lists['emgday'].str.contains('Y')]
        if(check5=='true'): #응급실야간운영여부
            search_lists = search_lists[~search_lists["emgnight"].str.contains("-")]
            search_lists=search_lists[search_lists['emgnight'].str.contains('Y')]
        if(name!=None):
            search_lists=search_lists[search_lists['hosname'].str.contains(name)]
    
    page=request.GET.get("page",1)
    paginator=Paginator(search_lists.to_dict('records'),10) # 페이지 표시 수
    pagelist=paginator.get_elided_page_range(page,on_each_side=2,on_ends=0)
    page_obj = paginator.get_page(page)
    context={
        'search_lists':search_lists.to_dict('records'),
        'search_list':search_list.to_dict('records'),
        'page_obj':page_obj,
        'today':whattoday,
        'pagelist':pagelist
    }
    return render(request,'search.html',context=context)

def search_ok(request):
    return HttpResponseRedirect(reverse('search'))

from .models import Member, Review, Event, Book, Myevent
from django.utils import timezone
def review(request):
    global viewplus
    template = loader.get_template('review.html')
    review =  Review.objects.all().values()
    viewplus = request.GET.get("value")
    # print(viewplus)    
    context = {
        'review': review, 
    }
    return HttpResponse(template.render(context, request))

def rwrite(request):
    global rating
    template = loader.get_template('rwrite.html')
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    rating = request.GET.get("value")
    # print(rating)
    context={
        'login_name':login_name,
    }
    return HttpResponse(template.render(context, request))  

def rwrite_ok(request):
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    subject = request.POST['subject']
    content = request.POST['content']
    hosname = request.POST['hosname']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    # rating = request.POST['rating']
    # views = request.POST['views']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    review = Review(writer=login_name,email=user_email,subject=subject,content=content,hosname=hosname,rdate=nowDatetime,views='1', rating=rating)
    review.save()
    return HttpResponseRedirect(reverse('review'))

def rcontent(request,id):
    template = loader.get_template('rcontent.html')
    review = Review.objects.get(id=id)
    user_email = request.session.get('login_ok_user')
    if viewplus is not None:
        review.views = review.views+1
        review.save()
    else:
        pass
    context = {
        'review' : review, 'user_email': user_email,
    }
    return HttpResponse(template.render(context,request))

from django.contrib import messages
def rdelete(request,id):
    review = Review.objects.get(id=id)
    user_email = request.session.get('login_ok_user')
    rid = Review.objects.filter(id=id).values('email').get()
    rid = rid['email']
    print(rid)
    if user_email==rid:
        review.delete()
        return HttpResponseRedirect(reverse('review'))
    else:
        messages.warning(request, "권한이 없습니다")
        return HttpResponseRedirect(reverse('review'))

def rupdate(request,id):
    global ratingup
    template = loader.get_template('rupdate.html')
    review = Review.objects.get(id=id)
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    ratingup = request.GET.get("value")
    context = {
        'review' : review, 'user_email' : user_email,
    }
    return HttpResponse(template.render(context,request))

def rupdate_ok(request,id):
    review = Review.objects.get(id=id)
    subject = request.POST['subject']
    content = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    review.subject=subject
    review.content=content
    review.rdate=nowDatetime
    review.rating=ratingup
    review.save()
    return HttpResponseRedirect(reverse('review'))

mdoc = col1.find()
df_m4 = pd.DataFrame(list(mdoc))
df_m4_1 = df_m4.dropna(subset=['y좌표','x좌표'])

df_m4_1 =  df_m4_1[['_id','요양기관명','y좌표','x좌표','주소']]
df_m4_1.set_index('_id')
map_list=df_m4_1.copy()
map_lists=pd.DataFrame()
print(map_lists)

def map(request):
    temlate = loader.get_template('map.html')
    context = {
    }
    global map_list, map_lists
    input1=request.GET.get("input1") #지역권
    input2=request.GET.get("input2") #시/도
    input3=request.GET.get("input3") #시/군/구
    name=request.GET.get("name") #병원이름
    print(input1)
    print(name)
    
    if (request.method == "POST"):        
        print("post가져옴")
        if ("inputname" in request.POST):
            mname=request.POST['inputname']
            where = {"요양기관명":{"$regex":""+str(mname)+""}}
            mdocs = col1.find(where)
            df_m = pd.DataFrame(list(mdocs))
            df_m2 = df_m.dropna(subset=['y좌표','x좌표'])
            
            df_m2 =  df_m2[['_id','요양기관명','y좌표','x좌표','주소']]
            num=len(df_m2)
        
            context = {
                'df_m2' : df_m2.to_dict('records'),
                'df_m22' : df_m2,
                'num':num,
                }
    if(request.method == "GET"): 
        print("ggggggggggggggggggggggggggggg")
        print("sd",input3)
        print("sd",name)
        if (input3 in request.GET):
            print("input3",input3)
            where = {"주소":{"$regex":""+str(input3)+""}}
            mdoc = col.find(where)
            df_m = pd.DataFrame(list(mdoc))
            print("dfm2 1 ",df_m2)
            df_m2 = df_m2.dropna(subset=['y좌표','x좌표'])
            print("dfm2 2 ",df_m2)
            df_m2 =  df_m2[['_id','요양기관명','y좌표','x좌표','주소']]
            print("dfm2 3 ",df_m2)
            num=len(df_m2)
            context = {
                'df_m2' : df_m2.to_dict('records'),
                'df_m22' : df_m2,
                'num':num,
                }
            # print("get가져옴")
            # print("hhhhhhhhhhhhhhhhhhhhhhhhhh")
            # print(input1)
            # if(input1==input2==input3==name==None):pass
            # else:
            #     map_lists=map_list
            #     if(name!=None):
            #         map_lists=map_lists[map_lists['요양기관명'].str.contains(name)]
            #         print("ㅇㅇㅇㅇ",input1)
            #     if(input1!='지역권 선택' and input2!='시/도 선택'):
            #         if(input3!='시/군/구 선택'):
            #             map_lists=map_lists[map_lists['주소'].str.contains(input3)]
            #         map_lists=map_lists[map_lists['주소'].str.contains(input2)]
            # context = {
            #     'map_list':map_list.to_dict('records'),
            # }
        
        
    
    return HttpResponse(temlate.render(context, request))

def login(request):
    return render(request,'login.html')

def login_ok(request):
    email = request.POST.get('email', None)
    pw = request.POST.get('pw', None)
    try:
        member=Member.objects.get(email=email)
    except Member.DoesNotExist:
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
        member = Member(
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
    dr = df_hs[['제목', '월', '내용']]
    dr1 = dr[dr['월']==1]
    dt1 = dr1.to_dict('records')
    dr2 = dr[dr['월']==2]
    dt2 = dr2.to_dict('records')
    dr3 = dr[dr['월']==3]
    dt3 = dr3.to_dict('records')
    dr4 = dr[dr['월']==4]
    dt4 = dr4.to_dict('records')
    dr5 = dr[dr['월']==5]
    dt5 = dr5.to_dict('records')
    dr6 = dr[dr['월']==6]
    dt6 = dr6.to_dict('records')
    dr7 = dr[dr['월']==7]
    dt7 = dr7.to_dict('records')
    dr8 = dr[dr['월']==8]
    dt8 = dr8.to_dict('records')
    dr9 = dr[dr['월']==9]
    dt9 = dr9.to_dict('records')
    dr10 = dr[dr['월']==10]
    dt10 = dr10.to_dict('records')
    dr11 = dr[dr['월']==11]
    dt11 = dr11.to_dict('records')
    dr12 = dr[dr['월']==12]
    dt12 = dr12.to_dict('records')
    context = {
    'dt1': dt1,'dt2': dt2,'dt3': dt3,'dt4': dt4,'dt5': dt5,'dt6': dt6,'dt7': dt7,'dt8': dt8,'dt9': dt9,'dt10': dt10,'dt11': dt11, 'dt12': dt12,
    }
    return HttpResponse(template.render(context, request))

def event(request):
    template = loader.get_template('event.html')
    event = Event.objects.all().values()
    context={
        'event':event
    }
    return HttpResponse(template.render(context, request))   

def econtent(request,id):
    template = loader.get_template('econtent.html')
    event = Event.objects.get(id=id)
    context = {
        'event' : event,
    }
    return HttpResponse(template.render(context,request)) 

def mypage(request):
    template= loader.get_template('mypage.html')
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    book_list = Book.objects.filter(email=user_email).values()
    user_addr = Member.objects.filter(email=user_email).values('addr').get()
    user_pw = Member.objects.filter(email=user_email).values('pw').get()
    user_phoneNum = Member.objects.filter(email=user_email).values('phoneNum').get()
    idcount = 1
    try:
        dibsedevent = Myevent.objects.filter(email=user_email).values()    
    except:
        dibsedevent = Myevent.objects.all().values()
        print(user_email)
        print(dibsedevent)
        print("딥스가 없는데요")
    context={ 'user_email' : user_email, 'login_name':login_name,
        'user_email' : user_email, 'dibsedevent':dibsedevent,
        'idcount':idcount,'book_list' : book_list,'user_addr':user_addr,'user_pw':user_pw,
        'user_phoneNum':user_phoneNum,

    }
    return HttpResponse(template.render(context,request)) 

def update_ok(request):
    user_email = request.session.get('login_ok_user')
    member = Member.objects.get(email=user_email)
    pw = request.POST['pw']
    addr = request.POST['addr']
    phoneNum = request.POST['phoneNum']
    member.pw = pw
    member.addr = addr
    member.phoneNum = phoneNum
    member.save()
    print("주소:",addr,"휴대폰번호:",phoneNum,"주소:",addr)
    return HttpResponseRedirect(reverse('mypage'))

hospital=pd.DataFrame()
def book(request,num):
    global search_lists,hospital
    hospital = search_lists[search_lists['num']==num]
    hospital.reset_index()
    hosname=hospital.iloc[0]['hosname']
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    user_phoneNum = Member.objects.filter(email=user_email).values('phoneNum').get()
    template = loader.get_template('book.html')
    today = datetime.today() + timedelta(1) #내일부터예약가능
    tomorrow=today.strftime("%Y-%m-%d")
    context={
        'tomorrow':tomorrow,
        'hosname':hosname,
        'num':num,
        'name':user_name,
        'phoneNum':user_phoneNum,
    }
    return HttpResponse(template.render(context, request))



def book_ok(request):
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    bdate=request.GET.get("bdate")
    btime=request.GET.get("btime")
    symptom=request.GET.get("symptom")
    content=request.GET.get("content")
    hosname=request.GET.get("hosname")
 
    if(bdate!=None and btime!=None):
        # new_bdate = datetime.strptime(bdate, '%Y-%m-%d')
        # new_time= datetime.strptime(btime, '%H:%M:%S')
        # newdate = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        # newdate = bdate+" "+btime
        new_bdate = bdate 
        new_btime = btime
        # symptom = request.POST.get('symptom','')
        # content = request.POST.get('content','')
        # hosname = request.POST.get('hosname','')
        print("symptom",symptom,"content",content,"hosname",hosname)
        print("user_email",user_email,"user_name",user_name['name'])
        book = Book(name=user_name['name'],email=user_email,hosname=hosname,symptom=symptom,content=content,bdate=new_bdate,btime=new_btime)
        book.save()
    return HttpResponseRedirect(reverse('search'))

def dibs(request, id):
    user_email = request.session.get('login_ok_user')
    eventhosname = Event.objects.filter(id=id).values('hospital_name').get()
    eventhosname = eventhosname['hospital_name']
    print(eventhosname)
    eventname = Event.objects.filter(id=id).values('event_name').get()
    eventname = eventname['event_name']
    print(eventname)
    myevent = Myevent(email=user_email, title=eventname, hosname=eventhosname)
    myevent.save()
    try:
        checkcheck = Myevent.objects.filter(title=eventname).values('title').get()
        print(checkcheck['title'])
        return redirect('../../econtent/'+str(id)+'')
    except:
        myevent = Myevent.objects.filter(title=eventname).all()
        myevent.delete()
        return redirect('../../econtent/'+str(id)+'')

def dibsdelete(request,title):
    myevent = Myevent.objects.filter(title=title).all()
    print("마이이벤트",myevent)
    myevent.delete()
    return HttpResponseRedirect(reverse('mypage'))

def bookdelete(request,id):
    mybook = Book.objects.filter(id=id).all()
    print("나의예약",mybook)
    mybook.delete()
    return HttpResponseRedirect(reverse('mypage'))  
    

