#import Selenium and get the page source

raw_data_list = []

def listappend(pagesource):
	rep1 = re.compile(r'<font color="#CC0000">(.*?)<font color="#CC0000">',re.S)
	buff = re.findall(rep1,pagesource)[0]
	rep = re.compile(r'<tr bgcolor="#.*?">.*?</tr>',re.S)
	list_need_append = re.findall(rep,buffer)
	raw_data_list.extend(list_need_append)
	print("ADD %d data into raw,new raw contains %d"%(len(list_need_append),len(raw_data_list)))
	


good = []
miss = []
def first_slt(raw,good,miss):
	rep = re.compile(r'<tr bgcolor="#.*?">.*?<td>.*?<font .*?>.*?<b>(.+?)</b></a><br />([a-zA-Z0-9]+).*?</font>.*?</td>.*?<td>.*?<font .*?><b>(.+?), ([0-9.%]+) (.*?)</b></font>.*?<font size="2">.*?<font .*?>.*?(\d{1,2}/\d\d/\d\d|[a-zA-Z ]+)</font>.*?<a href="(.+?)" target="SECEDGAR"><b>.*?</b></a>.*?[a-zA-Z ]+.*?(\d{1,2}/\d\d/\d\d|[a-zA-Z ]+).*?</font>.*?</td>.*?</tr>',re.S)
	counter = 0
	for each in raw:
		counter += 1
		print("Processing No.%d"%counter,end='')
		buff = re.findall(rep,each)
		if buff:
			good.append(buff[0])
			print("good add 1,Len of good%d"%len(good))
		if not buff:
			miss.append(each)
			print("miss add 1,Len of miss%d"%len(miss))


 c= ('AEH',
 '007924301',
 'AEGON N.V.',
 '6.375%',
 'Perpetual Capital Securities',
 '5/26/05',
 'http://www.sec.gov/Archives/edgar/data/769218/000104746905016016/a2158930z424b5.htm',
 '6/15/15')

 #'MNESP'
#'602720203'
parsed= []
def yes_no(good,parsed):

	for each in good:
		print(each)
		formated = [each[0],each[1],each[2],each[3],'','','','',each[5],each[7],each[4],each[6]]
		header = ['Ticker','CUSIP','NAME','PERCENT','Cumulative','Perpetual','Convertible','Redeemable','IPO date','Call date', 'Other', 'IPO link']
		if 'Cumul' in each[4]:
			if ' Cumul' in each[4] or each[4].index('Cumul')==0:
				formated[4] = 'Yes'
			else:
				formated[4] = 'No'
		else:
			formated[4] = 'No'

		if 'Perp' in each[4]:
			if ' Perp' in each[4] or each[4].index('Perp')==0:
				formated[5] = 'Yes'
			else:
				formated[5] = 'No'
		else:
			formated[5] = 'No'

		if 'Conv' in each[4]:
			if ' Conv' in each[4] or each[4].index('Conv')==0:
				formated[6] = 'Yes'
			else:
				formated[6] = 'No'
		else:
			formated[6] = 'No'	

		if 'Red' in each[4]:
			if ' Red' in each[4] or each[4].index('Red')==0:
				formated[7] = 'Yes'
			else:
				formated[7] = 'No'	
		else:
			formated[7] = 'No'	
		if each[-1][0] in '1234567890' or 'time' in each[-1]:
			formated[7] = 'Yes'

		parsed.append(formated)	


from bs4.element import Tag
from bs4 import BeautifulSoup

'''def tree_dict(roottag):
	L={}
 	for each in roottag:
 		print(each.name)
 		if isinstance(each,Tag):
 			subdir=tree_dict(each)
 			if each.name in L:
 				L[each.name].append(subdir)
 			else:
 				L[each.name]=[subdir,]
 		else:
 			L[each.name]=each

 	retur'.n L'''

tdre =[
 		[r'<b>(.+?)</b>',
		r'<br />([a-zA-Z0-9]+).*?</font>'],
		[r'<font .*?><b>(.+?), ([0-9.$%/ ]+|[a-zA-z]+) (.*?)</b></font>',
		 r'>IPO.*?(\d{1,2}/\d\d/\d\d|[a-zA-Z ]+).*?</font>',
		 r'<a href="(.+?)".*?>',
		 r'Call Date.*?(\d{1,2}/\d\d/\d\d|[a-zA-Z ]+).*?</font>'
		]
]


def get_td(cont):
	rep = re.compile(r'<td.*?>(.+?)</td>',re.S)
	tdlist = re.findall(rep,cont)
	print(len(tdlist))
	return tdlist

def tr_parser(raw,tdre):

	tdlist = get_td(raw)
	reslist = []
	for each in range(2):
		spe_parser(tdlist[each],tdre[each],reslist)

	return reslist
def spe_parser(tdcont,tdre,reslist):
	a=r'<font .*?><b>(.+?), ([0-9.$%/ ]+|[a-zA-z]+) (.*?)</b></font>'
	for each in tdre:
		rep = re.compile(each,re.S)
		cont = re.findall(rep,tdcont)
		if cont:
			if isinstance(cont[0],tuple):
				reslist.extend(cont[0])
			else:
				reslist.append(cont[0])
		else:
			if each == a:
				print(True)
				reslist.extend(['N/A','N/A','N/A'])
			else:
				reslist.append('N/A')



def main_parser(raw_list,tdre):
	result = []
	for each in raw_list:
		result.append(tr_parser(each,tdre))
	return result


def search(raw,ticker):
	for each in raw:
		if ticker in each:
			soup = BeautifulSoup(each,'html.parser')
			print(soup.prettify())


def companyname(datalist):
	name = [each[2] for each in datalist]
	print(datalist)
	company = set()
	for each in datalist:
		
		repl = each.replace('.','').replace(',','').replace('&amp;','&')
		splt = repl.split(' ')
				
		company.add(' '.join(splt[:4]))

	return list(company)






# row232 ENRJP	292758307	EnerJex Resources	10.00%	Yes	Yes	No	Yes	6/17/14	6/16/17	Series A Cumul Redeemable Perpetual Preferred Stock

