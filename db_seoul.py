import pandas as pd

country_list = ['서울']
hospital = pd.read_excel('자료/1.병원정보서비스.xlsx')
hospital = hospital[hospital['시도코드명'].isin(country_list)]
hospital= hospital[['암호화요양기호','요양기관명','종별코드명','주소','전화번호','병원홈페이지(URL)','개설일자','총의사수','x좌표','y좌표']].copy()
pharmacy = pd.read_excel('자료/2.약국정보서비스.xlsx')
pharmacy = pharmacy[pharmacy['시도코드명'].isin(country_list)]
pharmacy= pharmacy[['암호화요양기호','요양기관명','종별코드명','주소','전화번호','개설일자','x좌표','y좌표']].copy()

df1 = pd.read_excel('자료/3.의료기관별세부정보.xlsx')
df1 = df1[['암호화요양기호','응급실 주간운영여부','응급실 야간운영여부','진료시작시간_월','진료종료시간_월','진료시작시간_화','진료종료시간_화','진료시작시간_수','진료종료시간_수','진료시작시간_목','진료종료시간_목','진료시작시간_금','진료종료시간_금','진료시작시간_토','진료종료시간_토','일요일 휴진안내','공휴일 휴진안내']].copy()
df2 = pd.read_excel('자료/4.의료기관별진료과목정보.xlsx')
df2 = df2[['암호화요양기호','진료과목코드명']].copy()
sub_code=df2.groupby('암호화요양기호')['진료과목코드명'].apply(lambda x: x.sum()).reset_index(name='진료과목')
# print(sub_code)

mergedata1=pd.merge(df1,sub_code,how='left',on='암호화요양기호')
mergedata2=pd.merge(hospital,mergedata1,how='left',on='암호화요양기호')
mergedata3=pd.merge(pharmacy,mergedata1,how='left',on='암호화요양기호')

result2 = pd.concat([mergedata2,mergedata3], ignore_index=True)

# mergedata2.append(mergedata3,sort=False)

result2.reset_index()
result2.drop(['암호화요양기호'],axis='columns',inplace=True)
# print(mergedata2)

index_id=[]
for x in range(1,len(result2)+1):
    index_id.append(x)
result2.insert(0,'_id',index_id)

all_list=result2.to_dict('records')

from pymongo import mongo_client
url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['All_list']
col.insert_many(all_list)