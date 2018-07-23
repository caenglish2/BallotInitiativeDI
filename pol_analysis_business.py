# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 11:22:12 2018

@author: caenglish
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
from sklearn import linear_model
import numpy as np

#Load proposal data all the way back to 2012
data=pd.read_csv('CEDAallData_proposals4.csv')
data.drop(['DATE','CSD','Multi_MeasID','MEASTYPE','LTR','RECTYPE'],inplace=True,axis=1)

#Load information on how many voters of each party exist in each county
voter=pd.read_csv('CAcountry_voters.txt',sep='\t')
data_bus_tax=data[data['RECTYPENAME']=='Business Tax']

#Combine each data frame so D-R spread is placed according to the county of the vote
data_tax=pd.merge(data_bus_tax,voter, on='CNTYNAME', how='left')

#Let's do a linear regression to see if there is a relationship between which party has more voters in the county and whether they are more likely to vote for tax hikes at the polls
x=[];y=[]
for i in range(len(data_tax['DRspread'])):
    x.append([data_tax['DRspread'].iloc[i]])
    y.append((data_tax['Percent_sum'].iloc[i]-0.5)*100.0)

    
linear_regression = linear_model.LinearRegression()
linear_regression.fit(x,y)

    #Calculate correlation coefficients
corr_p=scipy.stats.pearsonr(data_tax['DRspread']/100.0, data_tax['Percent_sum'])
corr_s=scipy.stats.spearmanr(data_tax['DRspread']/100.0, data_tax['Percent_sum'])
print('Pearson CC: ',corr_p)
print('Spearman CC: ',corr_s)

#Plot the relationship or lack thereof
x_test=np.arange(-30,60,10).reshape(-1,1)

y_predict=linear_regression.predict(x_test)

plt.xlim(-30,50)
plt.xlabel('Democrat Voter Advantage Margin[%]')
plt.ylabel('Vote Success Margin[%]')
plt.scatter(x,y)
plt.plot(x_test,y_predict,linewidth=2)
plt.savefig('BusinessTax_Scatter.png',dpi=500)