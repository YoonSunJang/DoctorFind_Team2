import pandas as pd

df = pd.read_excel('C:/Users/Kosmo/Desktop/jj3/1.병원정보서비스 2022.6.xlsx')
df.drop_duplicates()

index_id=[]
for x in range(1,len(df)+1):
    index_id.append(x)
df.insert(0,'_id',index_id)
print(df)

hospital_seoul=df.to_dict('records')


from pymongo import mongo_client

url = 'mongodb://localhost:27017/'
mgClient = mongo_client.MongoClient(url)
db = mgClient['0804_team2']
col = db['0804_HospitalList']
col.insert_many(hospital_seoul)
