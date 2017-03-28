import requests as req
import re
import pandas as pd
import lxml
import html5lib
from queue import Queue,Empty
import os
from threading import Thread
from bs4 import BeautifulSoup
import IProxypool
import time
from multiprocessing import Process,Queue
proxypool = IProxypool.Proxypool()
[Companylist.put(each) for each in comps]


Companylist = Queue()


errorlink = []
missed =[]

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

homepage = 'http://www.sec.gov'
#encoding =ISO-8859-1
enco = 'ISO-8859-1'
searchpage =homepage+'/cgi-bin/browse-edgar'


params = {'company':'AGNC Investment Corp','type':'10-Q','count':'100'}





def contentdivparser(content):
	repattern = re.compile(r'<div id="contentDiv">(.+?)<div id="footer">',re.S)
	parsed = re.findall(repattern,content)[0]
	return parsed if parsed else None

def check_if_in(parsed):
 
	if 'Companies with names matching' in parsed:
		return False
	if 'No matching companies' in parsed:
		return False
	return True

def search_10q(parsed):
	rep = re.compile(r'href="/Archives(.+?)"',re.S)
	docs = re.findall(rep,parsed)
	doclinks = [homepage+'/Archives'+each for each in docs]
	return doclinks if doclinks else None
def search_date(parsed):
	rep = re.compile(r'<td>(\d\d\d\d-\d\d-\d\d)</td>',re.S)
	dates = re.findall(rep,parsed)
	return dates



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




def get_10q(doclink):

	r = request_(doclink)

	soup = BeautifulSoup(r.text,'html.parser')
	for each in soup.table:
		try:
			if '10-Q' in each.text:
				a=each
		except:
			pass
	rep = re.compile(r'href="(.+?)"',re.S)
	tenq = re.findall(rep,a.decode())[0]
	return homepage+tenq


def create_folder(name):
	csvname = 'EXCEL'+os.sep+name
	txtname = 'TEXT'+os.sep+name
	htmname = 'HTML'+os.sep+name
	if os.path.exists(csvname):
		pass
	else:
		os.mkdir(csvname)
	if os.path.exists(txtname):
		pass
	else:
		os.mkdir(txtname)
	if os.path.exists(htmname):
		pass
	else:
		os.mkdir(htmname)

def worker(q,missed):


	while True:
		try:
			company = q.get(timeout=2)
		except Empty:
			break

		homepage = 'http://www.sec.gov'

		searchpage =homepage+'/cgi-bin/browse-edgar'

		# s = req.Session()

		
		create_folder(company)

		param = {'company':company,'type':'10-Q','count':'100'}

		print('* '*15,'Searching %s'%company,'* '*15,)
		switcher = True
		r =request_(searchpage,param)
	
		search_result = contentdivparser(r.text)
		if not check_if_in(search_result):
			missed.append(company)
			continue
		print('Getting doc links')
		doclinks = search_10q(search_result)
		print('Getting dates')
		dates = search_date(search_result)
		print('Getting 10-Q links')
		tenq_links = [get_10q(each) for each in doclinks]
		print('Pre-output')
		if len(dates) == len(tenq_links):
			pre_output = list(zip(tenq_links,dates))
		else:
			pre_output = list(zip(tenq_links,range(len(tenq_links))))

		[table_output(tenq,dates,company) for tenq,dates in pre_output]

def save_html(tblcont,dates,company):
	head = ['<html><head></head><body>']
	tail = ['</body></html>']
	output = ' '.join(head+tblcont+tail)
	f = open('HTML/%s/%s.htm'%(company,dates),'w')
	f.write(output)
	f.close()
def save_txt(cont,dates,company):
	output = cont
	f = open('TEXT/%s/%s.txt'%(company,dates),'w')
	f.write(output)
	f.close()

def save_csv(tblcont,dates,company):
	cnt=0
	csvname = 'EXCEL/%s/%s'%(company,dates)
	if os.path.exists(csvname):
		pass
	else:
		os.mkdir(csvname)
	for each in tblcont:
		df = pd.read_html(each,encoding = 'ISO-8859-1')
		for ea in df:
			ea.to_csv('EXCEL/%s/%s/%d.csv'%(company,dates,cnt),encoding = 'ISO-8859-1')
			cnt+=1




def table_output(tenqlink,dates,company):
	print("parsing %s 10-Q on %s"%(company,dates))
	r = request_(tenqlink)
	if r.status_code != 200:
		return
	if '.htm' in tenqlink:
		tables = []
		soup = BeautifulSoup(r.text,'lxml')
		tablist = soup.find_all('table')
		for each in tablist:
			dec = re.sub(r'[^\x00-\x7F]','', each.decode())
			if 'Preferred stock' in dec or 'preferred stock' in dec:
				tables.append(dec)
		save_html(tables,dates,company)
		save_csv(tables,dates,company)


	elif '.txt' in tenqlink:
		save_txt(r.text,dates,company)
	else:
		print(tenqlink)
		errorlink.append(tenqlink)
		return




def main():
	global missed
	global Companylist
	procs = [Process(target = worker,args=(Companylist,missed)) for t in range(6)]
	[p.start() for p in procs]
	[p.join() for p in procs]
	print('Finished')



def get_a_proxy(pool):
        if pool:
                proxy = {"http":"http://%s:%s"%(pool[0][0],pool[0][1])}
                print("线程切换到ip地址:%s"%(pool[0][0]))
                del pool[0]        
                return proxy 



