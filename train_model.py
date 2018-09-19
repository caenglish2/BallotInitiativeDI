#!/bin/python

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

import pandas as pd

data=pd.read_csv('data_test.txt')

data['clinton_margin']=data['TRUMP_%']-data['CLINTON_%']
#data_train=data.ix[:, ['clinton_margin','property_tax','sales_tax','business_tax','utility_tax','hotel_tax','bonds','ordinance','infrastructure','roads','parks','social_services','mental_health','substance_abuse','affordable_housing','emergency_services','fire','police','paramedic','spending_limit','cannabis','education','library','school','land_use']]

data=data[data['property_tax']==1]
print(data.head(100))
data_train=data.ix[:, ['clinton_margin']]


y_train=data['PERCENT'].astype(float)/100.0

y_train.to_csv('sample_train_data.dat')

#plt.scatter(data_train,y_train)
#plt.show()

pcc=pearsonr(data['clinton_margin'],data['PERCENT'])
scc=spearmanr(data['clinton_margin'],data['PERCENT'])

print(pcc[0], pcc[1])
print(scc[0], scc[1])

regr = LinearRegression()
regr.fit(data_train, y_train)
print('LR: ', regr.score(data_train,y_train))

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
y_rbf = svr_rbf.fit(data_train,y_train)
print('SVR-rbf: ', y_rbf.score(data_train,y_train)**2)

svr_lin = SVR(kernel='linear', C=1e3)
y_lin = svr_lin.fit(data_train,y_train)
print('SVR-lin', y_lin.score(data_train,y_train)**2)

svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_poly = svr_poly.fit(data_train,y_train)
print('SVR-poly', y_poly.score(data_train,y_train)**2)

regr_1 = DecisionTreeRegressor(max_depth=10)
regr_1.fit(data_train,y_train)
print('DTR: ', regr_1.score(data_train,y_train))

est = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,max_depth=1,random_state=0,loss='ls')
est.fit(data_train, y_train)
print('GBR: ', est.score(data_train,y_train))

nn=MLPRegressor()
nn.fit(data_train, y_train)
print('nn: ', est.score(data_train,y_train))
