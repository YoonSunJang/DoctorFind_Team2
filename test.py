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
print(endtime.index)

#타입변환(응급실운영여부)
df.iloc[:,[9,10]]=df.iloc[:,[9,10]].astype(str)
# 진료시간
row=list(range(11,23))
df.iloc[:,row]=df.iloc[:,row].fillna(0)
df.iloc[:,row]=df.iloc[:,row].astype(int)
df.iloc[:,row]=df.iloc[:,row].astype(str)
days=['월','화','수','목','금','토']
df2=pd.DataFrame(columns = ['진료시간_월', '진료시간_화', '진료시간_수','진료시간_목','진료시간_금','진료시간_토'])


# endtime=pd.DataFrame(columns=['end_월','end_화','end_수','end_목','end_금','end_토'])
for x in df.index:
    for y in days:
        if df.loc[x,'진료시작시간_{}'.format(y)]=='0':
            df.loc[x,'진료시작시간_{}'.format(y)]='-'
        if df.loc[x,'진료종료시간_{}'.format(y)]=='0':
            df.loc[x,'진료종료시간_{}'.format(y)]='-'    
        else:
            df.loc[x,'진료시작시간_{}'.format(y)]=str(df.loc[x,'진료시작시간_{}'.format(y)])[:-2]+":"+str(df.loc[x,'진료시작시간_{}'.format(y)])[-2:]
            df.loc[x,'진료종료시간_{}'.format(y)]=str(df.loc[x,'진료종료시간_{}'.format(y)])[:-2]+":"+str(df.loc[x,'진료종료시간_{}'.format(y)])[-2:]
            # endtime.loc[x,'end_{}'.format(y)]=df.loc[x,'진료종료시간_{}'.format(y)]
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
from datetime import datetime
whattime = datetime.now()
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

search_list=search_list.loc[endtime.index,:]
print(search_list)
# for x in search_list.index:
#     if str(endtime.loc[x,'end_월'])>'18:00':
#         search_list=search_list.loc[x,'mon']
# print(search_list)
# for x in search_list.index:
#     idx=search_list['mon'].str.find('~')[x]
#     if idx==-1: pass
#     else:
#         a=str(search_list.loc[x,'mon'])[idx+1:]
#         search_list=search_list[search_list['emgday'].str.contains('Y')]
#         a>str('19:00')

