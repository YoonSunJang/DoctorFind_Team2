from pymongo import mongo_client
url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['hospital_list']

import pandas as pd
df=col.find({},{'_id':0})
df=pd.DataFrame(df)

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
df[['진료과목','전화번호','총의사수','병원홈페이지(URL)','일요일 휴진안내','공휴일 휴진안내']].fillna('-')
print(df['진료과목'])
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

# df3 = df['subject'].str.split('과', n=df['subject'].str.count('과'), expand=False)
# print(df3)

# for x in df.index:
#     # df.loc[x,'subject'].replace('·','',inplace=True)
#     df.loc[x,'subject'].replace('과', '과/',regex=False)

# df['subject'].str.replace('·','', inplace=True)
print(df[df['mon','tue','wed','thur','fri','sat'].str.contains('~24')])
print(df[(df['mon'].str.contains('~24'))|(df['mon'].str.contains('~24'))|(df['mon'].str.contains('~24'))|(df['mon'].str.contains('~24'))|(df['mon'].str.contains('~24'))|(df['mon'].str.contains('~24'))])
# df3['subject']=df['subject'].replace('·','')
# df3['subject']=df['subject'].replace('과','과/')
# print(df['subject'])

