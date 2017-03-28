import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
pd.set_option('display.width', 150)

tickers=['AMZN','NFLX','NVDA','ADBE','PCLN']
port_x = [0.2,0.1,0.15,0.35,0.2]
port_y = [0.2,0.3,0.25,0.15,0.1]
amzn = pd.read_csv('AMZN.csv')
# nflx = pd.read_csv('NFLX.csv')
# nvda = pd.read_csv('NVDA.csv')
# adbe = pd.read_csv('ADBE.csv')
# pcln = pd.read_csv('PCLN.csv')
raw_data = [pd.read_csv(each+'.csv') for each in tickers]
roc =[]
# for each in [amzn,nflx,nvda,adbe,pcln]:
for each in raw_data:
	roc.append((each['Close'].values/np.roll(each['Close'].values,-1)-1)[:-1][::-1]*100)

roc = np.array(roc).T

dates = pd.to_datetime(amzn['Date'][:-1][::-1])
rocdf = pd.DataFrame(roc,index=dates,columns=tickers)
#rocdf.describe()
expret = np.array(rocdf.mean())
#(amzn['Close'].values/np.roll(amzn['Close'].values,-1)-1)[:-1][::-1]

var_covar = np.dot((rocdf.values-expret).T,(rocdf.values-expret))

#portfolio x and y statistics; mean,variance,covariance,correlation
x_mean = np.dot(expret,port_x)
x_var = np.dot(np.dot(port_x,var_covar),port_x)

y_mean = np.dot(expret,port_y)
y_var = np.dot(np.dot(port_y,var_covar),port_y)

xy_covar = np.dot(np.dot(port_x,var_covar),port_y)
xy_corr = xy_covar/np.sqrt(x_var*y_var)

#Calculating returns of combinations of Porfolio x and Portfolio y
x_in_comb = 0.3
comb_mean = x_mean*x_in_comb+y_mean*(1-x_in_comb)
comb_var = x_in_comb**2*x_var+(1-x_in_comb)**2*y_var+2*x_in_comb*(1-x_in_comb)*xy_covar
comb_stddev = np.sqrt(comb_var)



def table_of_returns(x_in_comb):	
	comb_mean = x_mean*x_in_comb+y_mean*(1-x_in_comb)
	comb_var = x_in_comb**2*x_var+(1-x_in_comb)**2*y_var+2*x_in_comb*(1-x_in_comb)*xy_covar
	comb_stddev = np.sqrt(comb_var)
	return comb_stddev,comb_mean


np.set_printoptions(formatter={'float': '{: 0.5f}'.format})

portfolio=np.arange(-5.0,5.1,0.1)

result = np.array([table_of_returns(x) for x in portfolio])


#draw the envelop

df = pd.DataFrame(result,index=portfolio,columns=['Risk (stddev)','Return (mean)'])

plt.figure()
# yticks = np.arange(-0.002,0.013,0.003)
# xticks = np.arange(0,0.8,0.1)

plt.scatter(df['Risk (stddev)'],df['Return (mean)'],alpha = 0.5,color='#51ADD8',label = 'Envelop Portfolio')
plt.legend(loc='best')
plt.title('Return - Risk Envelop')
# plt.yticks(yticks,yticks)
# plt.xticks(xticks,xticks)


#add new constant to test the current
c1=0.0
c2=0.0022

env_p_x  = np.dot(np.linalg.inv(var_covar),expret-c1)

env_p_y  = np.dot(np.linalg.inv(var_covar),expret-c2)

portfolio_x = np.array([x/sum(env_p_x) for x in env_p_x])
portfolio_y = np.array([x/sum(env_p_y) for x in env_p_y])

Er_x = np.dot(env_p_x,expret)
Er_y = np.dot(env_p_y,expret)

sigma_x = np.sqrt(np.dot(np.dot(env_p_x.T,var_covar),env_p_y))
sigma_y = np.sqrt(np.dot(np.dot(env_p_y.T,var_covar),env_p_y))
env_covar_xy= np.dot(np.dot(portfolio_x,var_covar),portfolio_y)
x_in_single = 0.6
single_mean = Er_x*x_in_single+Er_y*(1-x_in_single)
single_sigma = np.sqrt(x_in_single**2*sigma_x**2+(1-x_in_single)**2*sigma_y**2+2*env_covar_xy*x_in_single*(1-x_in_single))

x_props = np.arange(-5.0,5.1,0.1)
def table_of_returns2(x_in_comb):	
	single_mean = Er_x*x_in_single+Er_y*(1-x_in_single)
	single_sigma = np.sqrt(x_in_single**2*sigma_x**2+(1-x_in_single)**2*sigma_y**2+2*env_covar_xy*x_in_single*(1-x_in_single))
	return single_sigma,single_mean
opt_result = np.array([table_of_returns(x) for x in x_props])

single_df = pd.DataFrame(opt_result,index=x_props,columns=['Risk','Return'])

plt.figure()
plt.clf()
single_df.plot(kind='scatter', x='Risk', y='Return',color='#f26e6e')
plt.legend(loc='best')
plt.title('Return - Risk opt Envelop')
plt.show()
