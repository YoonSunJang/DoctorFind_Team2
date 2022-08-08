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
df_hs = pd.DataFrame(hsdb)
#df_hs['내용']=df_hs['내용'].str.replace(pat='\n', repl= '<br>' , regex=False)

print(df_hs)

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

# def healthinfo_ok(request):
#     global requ, dt
#     template = loader.get_template('healthinfo.html')
#     requ = request.GET.get("value")
#     print(int(requ))
#     dz = dr[dr['월']==int(requ)]
#     dt = dz.to_dict('records')
#     print(dt)
#     return HttpResponseRedirect(reverse('healthinfo'))

def signup(request):
    return render(request,'signup.html')
def event(request):
    return render(request,'event.html')

def mypage(request):
    return render(request,'mypage.html')
