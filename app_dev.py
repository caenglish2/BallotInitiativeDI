from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components
import pandas as pd
import requests
from io import StringIO
from datetime import date
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from sklearn.linear_model import LinearRegression


issue='property_tax'
state='CA'
county='Los Angeles'

data=pd.read_csv('data_train.csv')
data['clinton_margin']=data['CLINTON_%']-data['TRUMP_%']
max_income=data['PER_CAPITA_INCOME'].max()
data['PER_CAPITA_INCOME']=data['PER_CAPITA_INCOME']/max_income
data=data[data['%s'%issue]==1]

data_train=data.ix[:, ['clinton_margin','PER_CAPITA_INCOME']]
y_train=data['PERCENT'].astype(float)/100.0

pcc=[];scc=[];pcc_p=[];scc_p=[]

#Are the features correlated with the margin of victory?
for i in range(len(data_train.columns)):
	corr_p=pearsonr(data_train.ix[:,i],data['PERCENT'])
	corr_s=spearmanr(data_train.ix[:,i],data['PERCENT'])
	pcc.append(corr_p[0]);scc.append(corr_s[0])
	pcc_p.append(corr_s[1]);scc_p.append(corr_s[1])
#print(pcc, pcc_p)
#print(scc, scc_p)
#For my own benefit, check for co-linearity/correlated features (to be done when more ballot question data exists, it may just be wealthy counties in CA like Clinton)


#print(predictX)
GLR = LinearRegression()
GLR.fit(data_train, y_train)
GLR_R2=GLR.score(data_train, y_train)
#Ideally, we'd pickle the model (may require a model per catagory), but we're not there yet

location=str(state).upper()+"_"+str(county).upper()
county_lookup=pd.read_csv('data_county_lookup.csv')
county_lookup['clinton_margin']=county_lookup['CLINTON_%']-county_lookup['TRUMP_%']
county_lookup['PER_CAPITA_INCOME']=county_lookup['PER_CAPITA_INCOME']/max_income
PredictX=county_lookup[county_lookup['STATE_COUNTY']==location]
PredictX=PredictX.ix[:, ['clinton_margin','PER_CAPITA_INCOME']]

GLR_predict=GLR.predict(PredictX)
#print(GLR_predict)
print(PredictX.iloc[0,1])
