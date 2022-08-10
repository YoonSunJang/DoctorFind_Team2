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
search_list=df[['hosname','address','telnumber','mon','tue','wed','thur','fri','sat','emgday','emgnight','url','subject','doctors','sunDoff','holyoff']]
search_lists=pd.DataFrame()  

def index(request):
    template = loader.get_template('index.html')
    now = datetime.now()
    thismonth = now.month
    dr = df_hs[['제목', '월', '내용']]
    dr = dr[dr['월']==thismonth]
    indt = dr.to_dict('records')
    indtdt = indt[1:4]
    indtdict = indt[0]
    infoheadline = indtdict['제목']
    #infoheadline = ""+str(thismonth)+"월의 건강정보"
    print(infoheadline)
    review =  Review.objects.all().order_by('-id').values('subject')
    reviewheadline = review[0]['subject']
    print(reviewheadline)
    review1 = review[1]['subject']
    review2 = review[2]['subject']
    review3 = review[3]['subject']
    event = Event.objects.all().order_by('-id').values('content')
    eventheadline = event[0]['content']
    event1 = event[1]['content']
    event2 = event[2]['content']
    event3 = event[3]['content']
    eventbanner = Event.objects.filter(content=eventheadline).values('img_address').get()
    eventbanner = eventbanner['img_address']
    context = {
        'indtdt':indtdt, 'infoheadline' : infoheadline, 'reviewheadline':reviewheadline,
        'review1':review1, 'review2' : review2, 'review3': review3,
        'eventheadline' : eventheadline, 'event1':event1, 'event2':event2, 'event3':event3,
        'eventbanner' : eventbanner,
    }
    return HttpResponse(template.render(context, request))

from django.core.paginator import Paginator
from datetime import datetime,timedelta
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

    print("1")
    print("input1",input1)
    print("input2",input2)
    print("input3",input3)
    print("name",name)
    print("c1",check1)
    print("c2",check2)
    print("c3",check3)
    
    whattoday = datetime.today().weekday()
    
    
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
    # if(input1==input2==input3==check4==check5==None):
    #     print('모두 none!! 처음 search에 접속시')
    # elif(input1=='지역권 선택' or input2=='시/도 선택' or input3=='시/군/구 선택'): #지역일부검색 또는 X
    #     print('지역선택안함, 이름 또는 옵션선택 또는 전체')
    #     search_lists=search_list
    #     if(name!=None):
    #         search_lists=search_lists[search_lists['hosname'].str.contains(name)]
    #     if(input1!='지역권 선택' and input2!='시/도 선택'):
    #         if(input3!='시/군/구 선택'):
    #             search_lists=search_lists[search_lists['address'].str.contains(input3)]
    #         search_lists=search_lists[search_lists['address'].str.contains(input2)]
    # elif(input1!=None and input2!=None and input3!=None): #지역검색O
    #     search_lists=search_list
    #     if(name!=None):
    #         search_lists=search_lists[search_lists['hosname'].str.contains(name)]
    #     if(input1!='지역권 선택' and input2!='시/도 선택'):
    #         if(input3!='시/군/구 선택'):
    #             search_lists=search_lists[search_lists['address'].str.contains(input3)]
    #         search_lists=search_lists[search_lists['address'].str.contains(input2)]
    #     if(check2=='true'): #야간진료 > 확인필요
    #          search_lists=search_lists.loc[endtime.index,:]
    #     if(check4=='true'): #응급실주간운영여부
    #         search_lists=search_lists[search_lists['emgday'].str.contains('Y')]
    #     if(check5=='true'): #응급실야간운영여부
    #         search_lists=search_lists[search_lists['emgnight'].str.contains('Y')]
    
    print('search_lists',search_lists)
    page=request.GET.get("page",1)
    paginator=Paginator(search_lists.to_dict('records'),10) # 페이지 표시 수
    pagelist=paginator.get_elided_page_range(page,on_each_side=2,on_ends=0)
    page_obj = paginator.get_page(page)
    context={
        'search_list':search_lists.to_dict('records'),
        'page_obj':page_obj,
        'today':whattoday,
        'pagelist':pagelist
    }
    return render(request,'search.html',context=context)

def search_ok(request):
    return HttpResponseRedirect(reverse('search'))

from .models import Member, Review, Event
from django.utils import timezone
def review(request):
    global viewplus
    temlate = loader.get_template('review.html')
    review =  Review.objects.all().values()
    viewplus = request.GET.get("value")
    print(viewplus)    
    context = {
        'review': review, 
    }
    return HttpResponse(temlate.render(context, request))

def rwrite(request):
    global rating
    temlate = loader.get_template('rwrite.html')
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    rating = request.GET.get("value")
    print(rating)
    context={
        'login_name':login_name,
    }
    return HttpResponse(temlate.render(context, request))  

def rwrite_ok(request):
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    subject = request.POST['subject']
    content = request.POST['content']
    hosname = request.POST['hosname']
    #rating = request.POST['rating']
    # views = request.POST['views']
    user_email = request.session.get('login_ok_user')
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

def rdelete(request,id):
    review = Review.objects.get(id=id)
    review.delete()
    return HttpResponseRedirect(reverse('review'))

def rupdate(request,id):
    global ratingup
    template = loader.get_template('rupdate.html')
    review = Review.objects.get(id=id)
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    ratingup = request.GET.get("value")
    print(ratingup)
    context = {
        'review' : review, 'user_email' : user_email,
    }
    return HttpResponse(template.render(context,request))

def rupdate_ok(request,id):
    template = loader.get_template('rupdate.html')
    review = Review.objects.get(id=id)
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
    review.rating = ratingup
    review.save()
    return HttpResponseRedirect(reverse('review'))

def map(request):
    return render(request,'map.html')
def map_ok(request):
    mname=request.POST['inputname']
    temlate = loader.get_template('map.html')
    where = {"요양기관명":{"$regex":""+str(mname)+""}}
    mdocs = col1.find(where)
    df_m = pd.DataFrame(list(mdocs))
    df_m2 = df_m.dropna(subset=['y좌표','x좌표'])
    mlist = df_m['요양기관명'].to_list()
    for doc in mlist:  
        print(doc)
        
    df_m2[['요양기관명','y좌표','x좌표']]
    lat = df_m2['x좌표'].mean()
    long = df_m2['y좌표'].mean()
    a=[]
    b=[]
    for i in df_m2.index:
        sub_lat = df_m2.at[i, 'x좌표']
        sub_long = df_m2.at[i, 'y좌표']
        title = df_m2.at[i, '요양기관명']
     # a.append(sub_long)
        # a.append(sub_lat)
        # b.append(sl)
    df_m2 =  df_m2[['요양기관명','y좌표','x좌표']]
   # df2['latlng'] =df2[cols].apply(lambda row: ', '.join(row.values.astype(str)),axis=1)

    #df2['latlng'] = df2['y좌표'] + ", " + df2['x좌표']

    #df2_2_3 = df2[['y좌표','x좌표']]
    m1 = df_m2['요양기관명']
    m2 = df_m2['y좌표']
    m3 = df_m2['x좌표']
    num=len(df_m2)
    #df2_2 = df2[title: '요양기관명', latlng: new kakao.maps.LatLng('y좌표', 'x좌표')]
    #{title: '카카오', latlng: new kakao.maps.LatLng(33.450705, 126.570677)}
    #df2_2 = df2
    #df2_2 = df2.rename(index = {'요양기관명':'title'}, inplace=True)
    #df2 = (df2['y좌표'],str.cat(df2['x좌표'], sep=', '))
    # df2_2 = df2[['y좌표','x좌표']]
    # df2_3 = df2[['요양기관명']]
    # df2_2_2 = ", ".join(df2_2)
    context = {
        'mlist': mlist,
        'sub_lat' : sub_lat,
        'sub_long' : sub_long,
        'title' : title,
        'lat' : lat,
        'long' : long,
        'xy' : (sub_lat, sub_long),
        'df_m2' : df_m2.to_dict('records'),
        'a' : a,
        'b' : b,
        'm1' : m1,
        'm2' : m2,
        'm3' : m3,
        'num':num,
        # 'df2_2':df2_2,
        # 'df2_3':df2_3,
        # 'df2_2_2':df2_2_2,
        # 'df2_2_3':df2_2_3,
    }
    print("df_m2.to_dict('records')",df_m2.to_dict('records'))
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
    temlate = loader.get_template('event.html')
    event = Event.objects.all().values()
    context={
        'event':event
    }
    return HttpResponse(temlate.render(context, request))   

from .models import Myevent
def econtent(request,id):
    template = loader.get_template('econtent.html')
    event = Event.objects.get(id=id)
    context = {
        'event' : event,
    }
    return HttpResponse(template.render(context,request)) 

def mypage(request):
    template = loader.get_template('mypage.html')
    user_email = request.session.get('login_ok_user')
    user_name = Member.objects.filter(email=user_email).values('name').get()
    login_name = user_name['name']
    idcount = 1
    try:
        dibsedevent = Myevent.objects.filter(email=user_email).values()    
    except:
        dibsedevent = Myevent.objects.all().values()
        print(user_email)
        print(dibsedevent)
        print("딥스가 없는데요")
    context={
        'user_email' : user_email, 'login_name':login_name, 'dibsedevent':dibsedevent,
        'idcount':idcount,
    }
    return HttpResponse(template.render(context,request)) 

def book(request):
    template = loader.get_template('book.html')
    today = datetime.today() + timedelta(1) #내일부터예약가능
    tomorrow=today.strftime("%Y-%m-%d")
    context={
        'tomorrow':tomorrow,
    }
    return HttpResponse(template.render(context, request))

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
    return HttpResponseRedirect(reverse('event'))

def dibsdelete(request,title):
    myevent = Myevent.objects.filter(title=title).all()
    print("마이이벤트",myevent)
    myevent.delete()
    return HttpResponseRedirect(reverse('mypage'))