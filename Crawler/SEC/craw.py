import requests as req
import re
import pandas as pd
#import lxml
#import html5lib
import os
#from bs4 import BeautifulSoup
import IProxypool
import time
from multiprocessing import Process,Queue
from datetime import datetime as dt


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


homepage = 'http://www.sec.gov'
#encoding =ISO-8859-1
enco = 'ISO-8859-1'
searchpage =homepage+'/cgi-bin/browse-edgar'
#finish
def contentdivparser(content):
	repattern = re.compile(r'<div id="contentDiv">(.+?)<div id="footer">',re.S)
	parsed = re.findall(repattern,content)[0]
	return parsed if parsed else None
#finish
def check_if_in(parsed):
 
	if 'Companies with names matching' in parsed:
		return False
	if 'No matching companies' in parsed:
		return False
	return True



#finish
def date_filter(doclist,start='2013-04-30',end='2032-05-22'):
	start = dt.strptime(start, "%Y-%m-%d")

	end = dt.strptime(end, "%Y-%m-%d")
	newlist = []
	for each in doclist:

		date = dt.strptime(each[2], "%Y-%m-%d")
		if date > start and date < end:
			newlist.append(each)
	return newlist



#finish
def get_doc_list(doclistcont):
	#doclistcont is content table of search result
	#datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
	
	rp =re.compile(r'<tr.*?<td.*?>(.+?)</td>.*?href="(.+?)".*?<td>(\d\d\d\d-\d\d-\d\d)</td>.*?</tr>',re.S)
	result = re.findall(rp,doclistcont)
	ncsr = [each for each in result if 'N-CSR' ==each[0]]
	ncsrs = [each for each in result if 'N-CSRS' ==each[0]]
	return ncsr,ncsrs

#finish
def get_doc(doclink,param):

	r = request_(doclink)

	soup = BeautifulSoup(r.text,'html.parser')
	for each in soup.table:
		try:
			if 'N-CSR' in each.text or 'N-CSRS' in each.text:
				a=each
				break
		except:
			pass
	rep = re.compile(r'href="(.+?)"',re.S)
	doc = re.findall(rep,a.decode())[0]
	return [param[0],param[1],homepage+doc]

def get_data(doclink,doctype):
	
	r = request_(doclink)
	data={}
	if doctype == 'N-CSR':
		data['Date'] = raw_parser(r.text,'a-date')
		data['Type'] = 'N-CSR'
	if doctype == 'N-CSRS':
		data['Date'] = raw_parser(r.text,'s-date')
		data['Type'] = 'N-CSRS'

	soup = BeautifulSoup(r.text,'lxml')  
	rawtablist = soup.find_all("table")
	
	tbls = set()
	for each in rawtablist:
		dec = dec = re.sub(r'[^\x00-\x7F]','', each.decode())
		if 'Net asset value, end of period' in dec:
			tbls.add(dec)
		if 'turnover' in dec:
			tbls.add(dec)

	tblist = [pd.read_html(each,encoding = 'ISO-8859-1')[0].replace(np.nan,' ') for each in tbls]
	raw_data_str = []
	for each in tblist:
		for ea in each.values:

			raw_str = ' '.join([str(each) for each in ea if each !=' '])
			if 'Net asset value, end of period'.upper() in raw_str.upper():
				raw_data_str.append(raw_str)
				data['NAV'] = raw_parser(raw_str,'$')
			if 'Market value, end of period'.upper() in raw_str.upper():
				data['Price'] = raw_parser(raw_str,'$')
				raw_data_str.append(raw_str)
			if 'Market price, end of period'.upper() in raw_str.upper():
				data['Price'] = raw_parser(raw_str,'$')
				raw_data_str.append(raw_str)
			if 'turnover'.upper() in raw_str.upper():
				data['Turnover'] = raw_parser(raw_str,'%')
				raw_data_str.append(raw_str)
	print('*'*10, len(raw_data_str))

	return data 



# - - - - - - - - - Tools - - - - - - - - -

#finish
def request_(link,param=None):
	
	proxy = None
	global proxypool
	global headers
	while True:
		try:
			r = req.get(link,param,headers = headers,proxies= proxy)
			break
		except:
			print('Except')
			if proxypool:
				proxy = get_a_proxy(proxypool)
				print('Except2')
			else:
				proxypool = IProxypool.Proxypool()
				proxy = get_a_proxy(proxypool)
				time.sleep(60)
	return r


#finish
def raw_parser(string,sign):
	try:
		if sign == '%':
			rep = re.compile(r'([0-9. ]+%)',re.S)
		if sign == '$':
			rep = re.compile(r'(\$ [0-9.]+)',re.S)
		if sign == 's-date':
			rep = re.compile(r'six months ended ([A-Za-z]+ [0-9, ]+)',re.S)
		if sign == 'a-date':
			rep = re.compile(r'year ended ([A-Za-z]+ [0-9, ]+)',re.S)



		return re.findall(rep,string)[0]
	except:
		print(string)

def raw_parser(string,sign):
	try:
		if sign == '%':
			rep = re.compile(r'([0-9. ]+%)',re.S)
		if sign == '$':
			rep = re.compile(r'(\$[0-9. ]+)',re.S)
		if sign == 's-date':
			rep = re.compile(r'six months ended ([A-Za-z]+ [0-9, ]+)',re.S)
		if sign == 'a-date':
			rep = re.compile(r'year ended ([A-Za-z]+ [0-9, ]+)',re.S)



		return re.findall(rep,string)[0]
	except:
		print(string)

def worker(q,missed):
	
	homepage = 'http://www.sec.gov'
	searchpage =homepage+'/cgi-bin/browse-edgar'	

	while True:
		try:
			companylist = q.get(timeout=2)

			
		except Empty:
			break
		print('* '*15,companylist,'* '*15)
		ticker = companylist[0]
		cik = companylist[2]
		name = companylist[1]
		
		params={'CIK': cik, 'count': '100', 'type': 'N-CSR'}
		r =request_(searchpage,params)
		#search_result = contentdivparser(r.text)
		search_result = r.text
		if not check_if_in(search_result):
			continue
		print('Getting doc links')
		ncsr,ncsrs = get_doc_list(search_result)
		if not ncsr or not ncsrs:
			missed['nothing'].append(companylist)
			continue


		ncsr = date_filter(ncsr)
		ncsrs = date_filter(ncsrs)
		if not ncsr or not ncsrs:
			missed['nothingnew'].append(companylist)
			continue
		ncsrlink = [get_doc(homepage+each[1],[each[0],each[2]]) for each in ncsr]
		ncsrslink = [get_doc(homepage+each[1],[each[0],each[2]]) for each in ncsrs]
		for each in ncsrlink:
			print(get_data(each[2],each[0]))



missed = {'nothing':[],'nothingnew':[]}

#worker(co,missed)

#keywords: Net asset value, end of period  ,Market value(price), end of period 


#['BLU' 'Blue Chip Value Fund' '810439'] 



#sorp = re.compile(r'>([a-zA-Z0-9.%$ ]+)<',re.S)



sorp = re.compile(r'>([a-zA-Z0-9.%$, ]+)<',re.S)


rep = re.compile(r'Net[ ]+asset[ ]+value[, a-z]+end[ a-z]+of[ a-z]+?[a-z]+',re.S)














