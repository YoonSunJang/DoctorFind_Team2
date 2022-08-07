from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import re

path = "C:/LJY/PyAdvanced/day06/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

dics=[]
idcount = 1
def crawling_data():
	global idcount, dics
	ds = {}
	while True:
		try:
			url = "https://www.g-health.kr/portal/index.do"
			driver.get(url)
			break
		except:
			time.sleep(1)

	while True:
		try:
			driver.find_element(By.XPATH, '/html/body/header/div[3]/nav/ul[1]/li[4]/a').click()
			break
		except:
			time.sleep(1)
	
	for i in range(1, 13):
		driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[1]/ul/li['+str(i)+']/a').click()
		for j in range(1,10):
			try:
				driver.find_element(By.CSS_SELECTOR, "body > div.site-body > div.container.sub-info.sub-info1 > div.health-calrendar > div.cal-contents > ul > li:nth-child("+str(j)+") > a").click()
				driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/table/thead' )
				subject = driver.find_element(By.TAG_NAME, 'th').text
				print(j)
				ds['_id']=idcount
				ds['월']=i
				ds['제목']=subject
				tbody = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[2]/table/tbody' )
				contents = tbody.find_element(By.TAG_NAME,'td').text
				ds['내용']=contents
				driver.back()
				idcount = idcount+1
				dics.append(ds)
				save_db(dics)
				dics = []
			except:
				break
	
	print(dics)

from pymongo import mongo_client
def save_db(dics):
    url = 'mongodb://localhost:27017/'
    mgClient = mongo_client.MongoClient(url)
    db = mgClient['project5_team2']
    col = db['healthinfo']
    col.insert_many(dics)

crawling_data()