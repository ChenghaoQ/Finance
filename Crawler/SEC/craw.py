import requests as req
import re
import pandas as pd
import lxml
import html5lib
import os
from bs4 import BeautifulSoup
import IProxypool
import time
from multiprocessing import Process,Queue
from datetime import datetime as dt
import numpy as np
import pickle


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
	data = dict(Date=None,Type=None,NAV=None,Price = None,Turnover= None,Expense = None)
	reps = [['NAV',r'Net[ ]+asset[ ]+value[ a-z]*,[ a-z]*end[ a-z]+of[ a-z]+?[a-z]+','$'],
		['Price',r'Market[ ]+(?:price|value)[ a-z]*,[ a-z]*end[ ]+of[ ]+period','$'],
		['Turnover',r'portfolio turnover','%']]
		

	r = request_(doclink)
	rr =r.text.replace('&nbsp;',' ')

	if doctype == 'N-CSR':
		data['Date'] = raw_parser(rr,'a-date')
		data['Type'] = 'N-CSR'
	if doctype == 'N-CSRS':
		data['Date'] = raw_parser(rr,'s-date')
		data['Type'] = 'N-CSRS'


	soup = BeautifulSoup(r.text,'lxml')  
	alltr = soup.find_all("tr")
	
	tbls = set()
	turnovers = []
	for each in alltr:
		dec = re.sub(r'[^\x00-\x7F]','', each.decode())
		for ea in reps:
			rep = re.compile(ea[1],re.I|re.S)
			cont =re.findall(rep,dec)
			if not cont:
				continue
			else:
				
				sorp = re.compile(r'>([a-zA-Z0-9.%$, ]+)<',re.S)
				rawcont = re.findall(sorp,dec)
				raw = ' '.join([eac for eac in rawcont if not eac.isspace()])
				rawdata = raw_parser(raw,ea[2])
				if not data[ea[0]] and rawdata:
					data[ea[0]]=rawdata
				elif not rawdata:
					continue
				elif data[ea[0]] and data[ea[0]]!=rawdata:
					return 'too much'
				if ea[0] == 'Turnover':
					turnovers.append(each)
	if len(turnovers) == 1:
		for each in turnovers:
			partable = each.parent
			partr = partable.find_all("tr")



			expensetrs = [re.sub(r'[^\x00-\x7F]','', extr.decode()) for extr in partr if re.findall(re.compile(r'expense',re.I|re.S),extr.decode())]
			expdata = []
			for exp in expensetrs:
						
				expraw = [eac for eac in re.findall(sorp,exp) if not eac.isspace()]
				if expraw:
					expname = expraw[0]
					expjoin = ' '.join(expraw)
					#print('\n',expraw,expjoin,'\n')
					exppercent = raw_parser(' '.join(expraw),ea[2])
							
					expdata.append([expname,exppercent])
			if len(expdata) == 1:
				data['Expense'] = expdata[0][1]
			elif len(expdata) >1:
				for ed in expdata:
					print(ed)
					data[ed[0]]=ed[1]

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
			rep = re.compile(r'(\$[0-9. ]+)',re.S)
		if sign == 's-date':
			rep = re.compile(r'six[ ]*months[ ]*ended[ ]*([a-z]+[ ]+[0-9, ]+)',re.S|re.I)

		if sign == 'a-date':
			rep = re.compile(r'year[ ]*ended[ ]*([a-z]+[ ]+[0-9, ]+)',re.S|re.I)

		return re.findall(rep,string)[0]
	except:
		return None



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
		baseinfo = {'Ticker':ticker,'cik':cik,'Name':name}
		params={'CIK': cik, 'count': '100', 'type': 'N-CSR'}
		r =request_(searchpage,params)
		#search_result = contentdivparser(r.text)
		search_result = r.text
		
		if not check_if_in(search_result):
			print('cannot find result')
			missed['notfind'].append(companylist)
			continue
		print('Getting doc links')
		ncsr,ncsrs = get_doc_list(search_result)
		if not ncsr or not ncsrs:
			print('nothing return')
			missed['nothing'].append(companylist)
			continue

		ncsr = date_filter(ncsr)
		ncsrs = date_filter(ncsrs)
		if not ncsr or not ncsrs:
			print('print nothing new')
			missed['nothingnew'].append(companylist)
			continue
		ncsrlink = [get_doc(homepage+each[1],[each[0],each[2]]) for each in ncsr]
		ncsrslink = [get_doc(homepage+each[1],[each[0],each[2]]) for each in ncsrs]
		for each in ncsrlink+ncsrslink:
			a = get_data(each[2],each[0])
			if a == 'too much':
				missed['toomuch'].append(companylist)
				continue
			repodate ={'ReportDate':each[1]}
			a.update(repodate)
			a.update(baseinfo)
			print(a)
			if None in a.values():
				missed['None'].append(a)
				continue
			missed['result'].append(a)
				


def cik_worker(q,missed):
	find = {}
	nofind =[]
	n=1
	for each in miss:
		result = None
		for ea in ciklookup:
			try:
				rep = re.compile(r'%s'%each[1],re.I|re.S)
				result = re.findall(rep,ea[0])
				if result and each[1] not in find.keys():
				    find[each[1]] = [[each[0],result[0],ea[1]],]
				elif result and each[1] in find.keys():
				    find[each[1]].append([each[0],result[0],ea[1]])
			except TypeError:
					continue
		if not result:
			nofind.append(each)
		print("No.%d finished,%d left"%(n,len(miss)-n))
		n+=1
	



missed = {'nothing':[],'nothingnew':[],'notfind':[],'result':[],'toomuch':[],'None':[]}

#worker(co,missed)

#keywords: Net asset value, end of period  ,Market value(price), end of period 


#['BLU' 'Blue Chip Value Fund' '810439'] 



#sorp = re.compile(r'>([a-zA-Z0-9.%$ ]+)<',re.S)


trrp = re.comopile(r'<tr.*?</tr>',re.S)
sorp = re.compile(r'>([a-zA-Z0-9.%$, ]+)<',re.S)


rep = re.compile(r'Net[ ]+asset[ ]+value[, a-z]+end[ a-z]+of[ a-z]+?[a-z]+',re.S)














