yes = set(['yes','y'])
no = set(['no','n'])
	
def main():
	yes = 1# set(['yes','y'])
	no = set(['no','n'])
	print("This script is mean to calculate EPS,DPS,BVPS,MVPS")
	print("Which one would you prefer to calculate?:\n\n(1) EPS\n(2) DPS\n(3) BVPS\n(4) MVPS\n(5) Quit")
	select = int(input('Please make a selection: '))

	for  select in range(1,5):
#select !=1 or select != 2 or select !=3 or select !=4 or select != 5:

		if select ==  1:
			EPS()
			print("Would your like to choose again?\nType'yes'or'y'to continue,'no'to quit: ")
			keep = input()
			while  keep is yes:
				continue
			print("Which one would you prefer to calculate?:\n\n(1) EPS\n(2) DPS\n(3) BVPS\n(4) MVPS\n(5) Quit")
			select = int(input('Please make a selection: '))
		if  select ==  2:
			DPS()
			again = input("Would your like to choose again?\nType'yes'or'y'to continue,'no'or'n'to quit: ")
			if  keep is yes:
				continue
			print("Which one would you prefer to calculate?:\n\n(1) EPS\n(2) DPS\n(3) BVPS\n(4) MVPS\n(5) Quit")
			select = int(input('Please make a selection: '))
	
		if  select ==  3:
			BVPS()
			again = input("Would your like to choose again?\nType'yes'or'y'to continue,'no'or'n'to quit: ")
			if  again in yes:
				continue
			print("Which one would you prefer to calculate?:\n\n(1) EPS\n(2) DPS\n(3) BVPS\n(4) MVPS\n(5) Quit")
			select = int(input('Please make a selection: '))
		
		if select ==  4:
			MVPS()
			again = input("Would your like to choose again?\nType'yes'or'y'to continue,'no'or'n'to quit: ")
			if  again in yes:
				continue
			print("Which one would you prefer to calculate?:\n\n(1) EPS\n(2) DPS\n(3) BVPS\n(4) MVPS\n(5) Quit")
			select = int(input('Please make a selection: '))
		
		if select ==  5:
			break
	else:	
		int(input("Once again please: "))

	print('Thank you! Bye-Bye!')


def EPS():
	print("EPS indicate Earning Per Share, would you like to calculate it?\nType'yes'or'y'to continue,'no'or'n'to quit")
	choice = input()
	while  choice not in yes  and choice  not in no:
		print('Incorrect choice,please try again: ')
		choice = input() 	 
	if choice in yes:
		which = int(input('which one would you preferred to calculate?\n(1) Net income availabe to common stockholders\n(2)Total shares of common stock outstanding\n(3)EPS\nPlease select one: ')) 
		
		if which == 1:
			total_shares_outstanding = float(input('Please enter Total shares of common stock outstanding is: '))
			EPS = float(input('Please enter the EPS: $ '))
			net_income_stockholder=EPS * total_shares_outstanding
			print('The Net income available to common stockholders is: $ ',net_income_stockholder)
		elif which == 2:
			net_income_stockholder = float(input('Please enter Net income availabe to common stockholders :$ '))
			EPS = float(input('Please enter the EPS: $ '))
			total_shares_outstanding = net_income_stockholder/EPS
			print('The Total shares of common stock outstanding is:$ ',total_shares_outstanding)
		elif which == 3:
			net_income_stockholder = float(input('Please enter Net income availabe to common stockholders :$ '))
			total_shares_outstanding = float(input('Please enter Total shares of common stock outstanding is: '))
			EPS = net_income_stockholder/total_shares_outstanding
			print("The EPS after calculated is:$ ",EPS)

		else:
			print('please try again',choice is yes)
	else:
		return	
’‘’		
				
		
def DPS():
	print("DPS indicate Dividends Per Share, would you like to calculate it?\nType'yes'or'y'to continue,'no'or'n'to quit")
	choice = input()
	while  choice not in yes  and choice not in no:
		print('Incorrect choice,please try again: ')
		choice = input() 	 
	if choice in yes:
		which = int(input('which one would you want to calculate?\n(1)Common stock of dividends paid\n(2)Total shares of common stock outstanding\n(3)DPS\nPlease select one: '))
		
		if which == 1:
			total_shares_outstanding = float(input('Please enter the Total shares of common stock outstanding: '))
			DPS = float(input('Dividends per share is : $ '))
			common_dividends_paid=total_shares_outstanding*DPS
			print('The Common stock of dividends paid is :$ ',common_dividends_paid)
		elif which == 2:
			common_dividends_paid = float(input('Please enter the Common stock of dividends paid:$ '))
			DPS = float(input('Dividends per share is : $ '))

			total_shares_outstanding = common-dividends_paid / DPS
			print('The Total shares of common stock outstanding is:$ ',total_shares_outstanding)
		elif which == 3:
			total_shares_outstanding = float(input('Please enter the Total shares of common stock outstanding: '))
			common_dividends_paid = float(input('Please enter the Common stock of dividends paid:$ '))
			DPS = common_dividends_paid/total_shares_outstanding
			print("The DPS after calculated is:$ DPS",DPS)

		else:
			 print('please try again',choice is yes)
		
	else:
		return

def BVPS():
	print("VBPS indicate Book Value Per Share, would you like to calculate it?\nType'yes'or'y'to continue,'no'or'n'to quit")
	choice = input()
	while  choice not in yes  and choice not in no:
		print('Incorrect choice,please try again: ')
		choice = input() 	 
	if  choice in yes:		
		which = int(input('which one would you wnat to calculate?\n(1) common stock\n(2) paid in surplus\n(3) retained earnings\n(4) Total shares of common stock outstanding\n(5)BVPS\nPlease select one: '))
		if which == 1:
			paid_in_surplus = float(input('Please enter the value of paid in surplus: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			retained_earnings = float(input('Please enter the value of retained earnings: $ '))
			BVPS = float(input('Please enter the Book Value per share: $ '))
			common_stock_value = total_shares_outstanding * BVPS - paid_in_surplus - retained_earnings	
		elif which == 2:
			common_stock_value = float(input(' Please enter the value of common stock: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			retained_earnings = float(input('Please enter the value of retained earnings: $ ')) 
			BVPS = float(input('Please enter the Book Value per share: $ '))
			paid_in_surplus = total_shares_outstanding * BVPS - common_stock_value  - retained_earnings
			
		elif which == 3:
			common_stock_value = float(input(' Please enter the value of common stock: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			paid_in_surplus = float(input('Please enter the value of paid in surplus: $ '))		
			BVPS = float(input('Please enter the Book Value per share: $ '))
			retained_earnings = total_shares_outstanding * BVPS - paid_in_surplus - common_stock_value

		elif which == 4:
			common_stock_value = float(input(' Please enter the value of common stock: $ '))
			paid_in_surplus = float(input('Please enter the value of paid in surplus: $ '))
			retained_earnings = float(input('Please enter the value of retained earnings: $ '))
			BVPS = float(input('Please enter the Book Value per share: $ '))
			total_shares_outstanding = (common_stock_value + paid_in_surplus + retained_earnings)/BVPS


		elif which == 5:
			common_stock_value = float(input(' Please enter the value of common stock: $ '))
			paid_in_surplus = float(input('Please enter the value of paid in surplus: $ '))
			retained_earnings = float(input('Please enter the value of retained earnings: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			BVPS = (common_stock_value + paid_in_surplus + retained_earnings)/total_shares_outstanding
			print("The BVPS after calculated is:$ BVPS",BVPS)
		else:
	                print('please try again',choice is yes)

	
	else: 
		return

def MVPS():
	print("MVPS indicate Market Value Per Share, would you like to calculate it?\nType'yes'or'y'to continue,'no'or'n'to quit")
	choice = input()
	while  choice not in yes  and choice not in no:
		print('Incorrect choice,please try again: ')
		choice = input() 	 
	if choice in yes:
		which = int(input('which one do you want to calculate?\n(1)Net income available to common stockholders\n(2)Preferred Dividends\n(3)Total shares of common stock outstanding\nPlease select one: '))

		if which == 1:
			preferred_dividends = float(input('Please enter the amount of Preferred Dividends: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			MVPS = float(input('Market Value per share is: '))
			net_income_stockholder = total_shares_outstanding * MVPS + preferred_dividends 
			print('the Net income available to common stockholders:$ ',net_income_stockholder)
		elif which == 2:
			net_income_stockholder = float(input('Please enter the Net income available to common stockholders:$ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			MVPS = float(input('Market Value per share is: '))
			preferred_dividends = net_income_stockholder - total_shares_outstanding * MVPS
			print('the amount of Preferred Dividends: $ ',preferred_dividends)
		elif which == 3:
			net_income_stockholder = float(input('Please enter the Net income available to common stockholders:$ '))
			preferred_dividends = float(input('Please enter the amount of Preferred Dividends: $ '))
			MVPS = float(input('Market Value per share is: '))
			total_shares_outstanding = (net_income_stockholder-preferred_dividends)/MVPS
			print('The shares of common stock outstanding is: ',total_shares_outstanding)
		elif which == 4:
			net_income_stockholder = float(input('Please enter the Net income available to common stockholders:$ '))
			preferred_dividends = float(input('Please enter the amount of Preferred Dividends: $ '))
			total_shares_outstanding = float(input('Total shares of common stock outstanding is: '))
			MVPS =(net_income_stockholder-preferred_dividends)/total_shares_outstanding
			print("The MVPS after calculated is:$ MVPS",MVPS)

		else:
			print('please try again',choice is yes)
		
	else:
		return




main()
