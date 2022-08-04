import requests
from pymongo import MongoClient

db = client.my_db #my_db에 자신의 데이터베이스 이름을 넣어줍니다.


post = {
    "관측소 명" : "울산",
    "관측 시간" : "2021-07-07 15:00:00",
    "조위" : "61.0",
    "수온" : "21.5",
    "염분" : "30.3",
    "기온" : "23.5",
    "기압" : "1007.7",
    "풍향" : "272.0",
    "풍속" : "0.6",
    "돌풍" : "1.2"
}

posts = db.weather # weather가 내가 원하는 콜렉션 이름
post_id = posts.insert_one(post)