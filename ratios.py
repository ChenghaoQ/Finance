#!/usr/bin/env python3
#-*- coding: utf-8 -*-
'A test module for financial ratios'

__author__ = 'ChenghaoQ'

#Liquidity Ratios:Current ratio;Quick ratio;Cash ratio
def CurrentR(current_asset,current_liabilities):
	return current_asset/current_liabilities
def QuickR(current_asset,inventory,current_liabilities):
	return (current_asset-inventory)/current_liabilities
def CashR(cash_or_markable_securities,current_liabilities):
	return cash_or_markable_securities/current_liabilities
#Asset management ratios
#Inventory
def intu(sales,inventory):
	return sales/inventory
def dsir(sales,inventory):
	return inventory*365/sales

#Account receivable management
def ACP(ar,creditsales):
	return ar*365/creditsales
def actu(ar,creditsales):
	return creditsales/ar
def APP():
	pass

#Account payable
def APTR(cogs,acct_payable):
	return cogs/acct_payable
#Fixed Asset and working capital management
def FATR(sales,fixed_assets):
	return sales/fixed_assets
def STWCR(sales,working_capital):
	return sales/working_capital

#Total Asset management ratio

#Total asset turnover ratio
def TATR(sales,total_assets):
	return sales/total_assets
#Captial intensity ratio
def CIR(total_assets,sales):
	return total_assets/sales

#Debt mangement ratios
#Debt ratio
def DR(total_debt,total_asset):
	return total_debt/total_asset
#Debt to Equity ratio
def DTER(total_debt,total_equity):
	return total_debt/total_equity
#Equity Multiplier Ratio
def EMR(total_asset,total_equity):
	return total_asset/total_equity
#Coverage Ratios
#Time interest earned ratios
def TIE(EBIT,interest):
	return EBIT/interest
#The fixed charge coverage ratio
def FCCR(earning_availiable_to_fixed_charges,fixed_charges):
	return earning_availiable_to_fixed_charges/fixed_charges 
#Cash Coverage ratio
def CCR(EBIT,depreciation,fixed_charge):
	return (EBIT+depreciation)/fixed_charge

#Profitability ratios
#Profit Margin
def PM(net_income_stockholder,sales):
	return net_income_stockholders/sales
#Basic Earning Power Ratio
def BEPR():
	pass
#Return on Assets
def ROA(NI,total_asset):
	return NI/total_asset
#Return on Equity
def ROE(NI,total_equity):
	return NI/total_equity
#Dividend payout ratio
def DPR(dividends,NI):
	return dividends/NI
#Market Value ratio

#Price Earning ratio


