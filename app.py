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

app = Flask(__name__)

def plot(ticker, year_start, month_start, year_end, month_end):
  p = figure(title="Price history for %s"%ticker, x_axis_label='Date', y_axis_label='Adj. Close', x_axis_type="datetime")
  p.line(data_to_plot['Date'], data_to_plot['Adj. Close'], legend="%s"%ticker, line_width=2)
  script, div = components(p)
  return script, div

@app.route('/')
def index():
  return render_template('options_menu.html')

@app.route('/graph', methods=['POST','GET'])
def about():
  result = request.form
  issue=result['dropdown']
  state=result['state']
  county=result['county']
  pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict, vict_marg, per_capita_income=analysis(issue,state,county)
  return render_template('graph.html',
	pcc=str(pcc[0])[:4],pcc_p='%.4f'%float(pcc_p[0]),
	scc=str(scc[0])[:4],scc_p='%.4f'%float(scc_p[0]),
	pcc2=str(pcc[1])[:4],pcc_p2='%.4f'%float(pcc_p[1]),
	scc2=str(scc[1])[:4],scc_p2='%.4f'%float(scc_p[1]),
	GLM_predict=str(float(GLR_predict))[0:4],
	GLM_R2=str(GLR_R2)[:4],
	vict_marg=str(vict_marg)[:3], per_capita_income=int(per_capita_income))#,output=output)#, script=script, div=div)



def analysis(issue, state, county):

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

	#print(predictX)
	GLR = LinearRegression()
	GLR.fit(data_train, y_train)
	GLR_R2=GLR.score(data_train, y_train)

	location=str(state).upper()+"_"+str(county).upper()
	county_lookup=pd.read_csv('data_county_lookup.csv')
	county_lookup['clinton_margin']=county_lookup['CLINTON_%']-county_lookup['TRUMP_%']
	county_lookup['PER_CAPITA_INCOME']=county_lookup['PER_CAPITA_INCOME']/max_income
	PredictX=county_lookup[county_lookup['STATE_COUNTY']==location]
	PredictX=PredictX.ix[:, ['clinton_margin','PER_CAPITA_INCOME']]

	GLR_predict=GLR.predict(PredictX)
	#print(GLR_predict)
	print(PredictX['clinton_margin'], PredictX['PER_CAPITA_INCOME'])
	return pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict[0]*100.0, PredictX.iloc[0,0]*100.0, PredictX.iloc[0,1]*max_income



if __name__ == '__main__':
  app.run(port=33507)
