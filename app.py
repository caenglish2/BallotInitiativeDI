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
  pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict, vict_marg, per_capita_income, uninsured_rate, some_college, N=analysis(issue,state,county)
  return render_template('graph.html',
	pcc=str(pcc[0])[:5],pcc_p='%.4f'%float(pcc_p[0]),
	scc=str(scc[0])[:5],scc_p='%.4f'%float(scc_p[0]),
	pcc2=str(pcc[1])[:5],pcc_p2='%.4f'%float(pcc_p[1]),
	scc2=str(scc[1])[:5],scc_p2='%.4f'%float(scc_p[1]),
	pcc3=str(pcc[2])[:5],pcc_p3='%.4f'%float(pcc_p[2]),
	scc3=str(scc[2])[:5],scc_p3='%.4f'%float(scc_p[2]),
	pcc4=str(pcc[3])[:5],pcc_p4='%.4f'%float(pcc_p[3]),
	scc4=str(scc[3])[:5],scc_p4='%.4f'%float(scc_p[3]),
	GLM_predict=str(float(GLR_predict))[0:5],
	GLM_R2=str(GLR_R2)[:4],
	vict_marg=str('%.1f'%vict_marg), per_capita_income=int(per_capita_income),
	uninsured_rate=str(float(uninsured_rate)*100.0)[:5],N=N,
	some_college=str(float(some_college)*100.0)[:5])



def analysis(issue, state, county):

	data=pd.read_csv('data_train.csv')
	data['clinton_margin']=data['CLINTON_%']-data['TRUMP_%']
	max_income=data['PER_CAPITA_INCOME'].max()
	data['PER_CAPITA_INCOME']=data['PER_CAPITA_INCOME']/max_income
	data=data[data['Issue']==issue]
	data_train=data.ix[:, ['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE']]
	data['PERCENT']=data['Yes'].astype(int)/(data['Yes'].astype(int)+data['No'].astype(int)).astype(float)
	y_train=data['PERCENT'].astype(float)

	pcc=[];scc=[];pcc_p=[];scc_p=[]
	#Are the features correlated with the margin of victory?
	for i in range(len(data_train.columns)):
		corr_p=pearsonr(data_train.ix[:,i],data['PERCENT'])
		corr_s=spearmanr(data_train.ix[:,i],data['PERCENT'])
		pcc.append(corr_p[0]);scc.append(corr_s[0])
		pcc_p.append(corr_p[1]);scc_p.append(corr_s[1])
		print(corr_p, corr_s)

	GLR = LinearRegression()
	GLR.fit(data_train, y_train)
	N=len(data_train)
	GLR_R2=GLR.score(data_train, y_train)

	location=str(state).upper()+"_"+str(county).upper()
	county_lookup=pd.read_csv('data_county_lookup.csv')
	county_lookup['clinton_margin']=county_lookup['CLINTON_%']-county_lookup['TRUMP_%']
	county_lookup['PER_CAPITA_INCOME']=county_lookup['PER_CAPITA_INCOME']/max_income
	PredictX=county_lookup[county_lookup['STATE_COUNTY']==location]
	PredictX=PredictX.ix[:, ['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE']]

	GLR_predict=GLR.predict(PredictX)
	#print(GLR_predict)
	#print(PredictX['clinton_margin'], PredictX['PER_CAPITA_INCOME'])
	return pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict[0]*100.0, PredictX.iloc[0,0]*100.0, PredictX.iloc[0,1]*max_income, PredictX.iloc[0,2], PredictX.iloc[0,3], N



if __name__ == '__main__':
  app.run(port=33507)
