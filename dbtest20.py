import pandas as pd

df = pd.read_excel('자료/건강보험심사평가원/1.병원정보서비스 2022.6.xlsx')
country_list = ['구로구', '광진구', '노원구']
df = df[df['시군구코드명'].isin(country_list)]
df.drop_duplicates()
df = df[['암호화요양기호','요양기관명','종별코드명','주소','전화번호','병원홈페이지(URL)','개설일자','총의사수','x좌표','y좌표']].copy()
# print(df)
df2 = pd.read_excel('자료/건강보험심사평가원/2.의료기관별상세정보서비스 02세부정보 2022.6.xlsx')
df.drop_duplicates()
df2 = df2[['암호화요양기호','응급실 주간운영여부','응급실 야간운영여부','진료시작시간_월','진료종료시간_월','진료시작시간_화','진료종료시간_화','진료시작시간_수','진료종료시간_수','진료시작시간_목','진료종료시간_목','진료시작시간_금','진료종료시간_금','진료시작시간_토','진료종료시간_토','일요일 휴진안내','공휴일 휴진안내']].copy()

mergedata=pd.merge(df,df2,how='left',on='암호화요양기호')
mergedata.reset_index()
mergedata.drop(['암호화요양기호'],axis='columns',inplace=True)

index_id=[]
for x in range(1,len(mergedata)+1):
    index_id.append(x)
mergedata.insert(0,'_id',index_id)
print(mergedata)

hospital_seoul=mergedata.to_dict('records')

from pymongo import mongo_client

url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['project5_team2']
col = db['test0805']
col.insert_many(hospital_seoul)