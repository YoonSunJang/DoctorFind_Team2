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
from datetime import datetime
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
hour=pd.datetime.now().hour
minute=pd.datetime.now().minute
# print(hour,minute)
# endtime['진료종료시간_월']=endtime[endtime['진료종료시간_월']>int(str(hour)+str(minute))]
# print(endtime)
whattoday = datetime.today().weekday()
for x in range(0,7):
    if(whattoday==x):
        print(days[x]) #목
        endtime=endtime[endtime['진료종료시간_{}'.format(days[x])]>int(str(hour)+str(minute))]

# print(type(list(endtime.index)[0]))
endtime=endtime.loc[[0,1,2],:]
print(endtime)