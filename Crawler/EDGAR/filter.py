

bank_keywords = ['MORGAN','CITI','lynch','GOLDMAN','BANK']


def filter(each):
	global n
	found = False
	for bk in ['MORGAN','CITI','lynch','GOLDMAN','BANK','BANCORP']:
		if bk.upper() in each.upper():
			bank.append(each)
			return
	for ea in right:
		if each.upper() in ea[0].upper():
			companylist.append(ea)
			found = True
	if found == False:
		notin.append(each)
	n+=1
	print(n)




#txt parser


rep = re.compile(r'<TABLE>(.*?)</TABLE>',re.S)

tlist = re.findall(rep,txt) 

tr=tlist[3].split('\n')  
newtr=[]
In [260]: for each in tr:           
     ...:     split = each.split('   ')
     ...:     splt = [ea for ea in split if ea !='']
     ...:     newtr.append(splt)

