'This script craws the data from the screener and put them into database'

from selenium import webdriver
import re
import mysql.connector
driver = webdriver.Chrome()

re_pattern = '<tr class="trow\w_na">.*?<td.*?</td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?<td.*?<a.*?>(.+?)</a></td>.*?</tr>'

re_frame=re.compile(re_pattern,re.S)
company_list = re.findall(re_frame,page_content)


passwd = input("Please enter your password")
database = input("Input the database your are going to connect")



try:
	cnn = mysql.connector.connect(**config)
except mysql.connector.Error as e:
	print('connnect failed!{}'.format(e))

cursor = cnn.cursor()

create_table = 'create table sp500_100( Company_Name varchar(50), Ticker varchar(10), Region varchar(10), SP_Sector varchar(30), SP_Sub_Industry varchar(50), Last_Closing_Price varchar(10), Ranking Varchar(15), Capital_IQ_RECOM VARCHAR(10), Return_1yr varchar(10), Return_5yr varchar(10), PE varchar(30), LTD varchar(30));'


cursor.execute(create_table)


data_insert = 'Insert sp500_100 (Company_Name,Ticker,Region,SP_Sector,SP_Sub_Industry,Last_Closing_Price,Ranking,Capital_IQ_RECOM,Return_1yr,Return_5yr,PE,LTD) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


for company in company_list:
	try:
		cursor.execute(data_insert,company)
	except:
		print("Inserting data error!{}".format(e))	

cnn.commit()
cursor.close()
cnn.close()

	






