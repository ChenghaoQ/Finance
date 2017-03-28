from selenium import webdriver

raw_data_list = []



def listappend(pagesource):
	rep1 = re.compile(r'<font color="#CC0000">(.*?)<font color="#CC0000">',re.S)
	buff = re.findall(rep1,pagesource)[0]
	rep = re.compile(r'<tr bgcolor="#.*?">.*?</tr>',re.S)
	list_need_append = re.findall(rep,buff)
	raw_data_list.extend(list_need_append)
	print("ADD %d data into raw,new raw contains %d"%(len(list_need_append),len(raw_data_list)))

import pickle
f= open('raw_data.pkl','wb')
pickle.dump(raw_data_list,f)
f.close()



tdre =[[r'<b>(.+?)</b>'],
		[r'<font .*?><b>(.+?) ([0-9 ]*[0-9.$%/ ]+) (.*?)</b></font>'],
		[r'<font.*?>(.+?)</font>'],
		[r'<font.*?>(.+?)</font>']
]



header = ['Symbol','NAME','PERCENT','Cumulative','Perpetual','Convertible','Redeemable','Other','Original Call Date','Actual Date Called']

def yes_no(good,parsed):

	for each in good:
		print(each)
		formated = [each[0],each[1],each[2],'','','','',each[3],each[4],each[5]]
		header = ['Ticker','CUSIP','NAME','PERCENT','Cumulative','Perpetual','Convertible','Redeemable','IPO date','Call date', 'Other', 'IPO link']
		if 'Cumul' in each[3]:
			if ' Cumul' in each[3] or each[3].index('Cumul')==0:
				formated[3] = 'Yes'
			else:
				formated[3] = 'No'
		else:
			formated[3] = 'No'

		if 'Perp' in each[3]:
			if ' Perp' in each[3] or each[3].index('Perp')==0:
				formated[4] = 'Yes'
			else:
				formated[4] = 'No'
		else:
			formated[4] = 'No'

		if 'Conv' in each[3]:
			if ' Conv' in each[3] or each[3].index('Conv')==0:
				formated[5] = 'Yes'
			else:
				formated[5] = 'No'
		else:
			formated[5] = 'No'	

		if 'Red' in each[3]:
			if ' Red' in each[3] or each[3].index('Red')==0:
				formated[6] = 'Yes'
			else:
				formated[6] = 'No'	
		else:
			formated[6] = 'No'	

		parsed.append(formated)	




def get_td(cont):
	rep = re.compile(r'<td.*?>(.+?)</td>',re.S)
	tdlist = re.findall(rep,cont)
	print(len(tdlist))
	return tdlist

def tr_parser(raw,tdre):

	tdlist = get_td(raw)
	reslist = []
	for each in range(4):
		spe_parser(tdlist[each],tdre[each],reslist)

	return reslist
def spe_parser(tdcont,tdre,reslist):
	a=r'<font .*?><b>(.+?) ([0-9 ]*[0-9.$%/ ]+) (.*?)</b></font>'
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



def writedown(name,data):
	r = open('%s.pkl'%name,'wb')
	pickle.dump(data,r)
	r.close()


# data cleanning
exceptions=['QUIPS','TRUPS','TOPRS','QUICS','QUIBS','QUIDS','FELINE','PEPS','PIERS','PIES','STRIDES','WIRES','CORTS','TRUCS','BOND','SYNTHETIC','STRUCTURED','SPARQS','QUIB','PPLUS','PINES','SATURNS','PERQS','PCARS','MITTS','DEBENTURE','TRUST']
#'BOND' NOT included,'debentures'

def cleaner(keyword,data_list):
	global include
	holder = []
	a= len(exclude)
	for each in data_list:
		if keyword in each[1].upper() or keyword in each[-3].upper():
			exclude.append(each)
		else:
			holder.append(each)
	include = holder
	b = len(exclude)
	print("%s: %d inserted, now exclude %d,include has %d left"%(keyword,b-a,b,len(include)))






def writecsv(name,header,data):
	with open('%s.csv'%name,'w') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(header)
		f_csv.writerows(data)




'''In [334]: with open('671result.csv','w') as f:
     ...:     f_csv = csv.writer(f)
     ...:     f_csv.writerow(header)
     ...:     f_csv.writerows(pars)'''

















