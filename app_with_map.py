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

from bokeh.io import show, output_file
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure


from bokeh.sampledata.unemployment import data as unemployment

app = Flask(__name__)

def plot(location, predictions,state_name):
	from bokeh.sampledata.us_counties import data as counties
	palette.reverse()
	counties = {code: county for code, county in counties.items() if county["state"] in [state_name]}
	county_xs = [county["lons"] for county in counties.values()]
	county_ys = [county["lats"] for county in counties.values()]
	county_names = [county['name'] for county in counties.values()]#Make sure names match with data

	county_rates = [unemployment[county_id] for county_id in counties]#These would be the predictions
	color_mapper = LogColorMapper(palette=palette)

	data=dict(x=county_xs,y=county_ys,name=county_names,rate=predictions,)
	TOOLS = "pan,wheel_zoom,reset,hover,save"

	p = figure(title="Vote Preference Predictions", tools=TOOLS,
	#x_axis_location=None, y_axis_location=None,tooltips=[("Name", "@name"), ("Unemployment rate)", "@rate%"), ("(Long, Lat)", "($x, $y)")])
	x_axis_location=None, y_axis_location=None,tooltips=[("Name", "@name"), ("Yes vote (percent)", "@rate%")])

	p.grid.grid_line_color = None
	p.hover.point_policy = "follow_mouse"

	p.patches('x', 'y', source=data,fill_color={'field': 'rate', 'transform': color_mapper},fill_alpha=0.7, line_color="white", line_width=0.5)
	show(p)
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
  pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict, vict_marg, per_capita_income, uninsured_rate, some_college, N, script, div=analysis(issue,state,county)
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
	some_college=str(float(some_college)*100.0)[:5],script=script,div=div)

def analysis(issue, state, county):

	data=pd.read_csv('data_train.csv')
	data['clinton_margin']=data['CLINTON_%']-data['TRUMP_%']
	max_income=data['PER_CAPITA_INCOME'].max()
	data['PER_CAPITA_INCOME']=data['PER_CAPITA_INCOME']/max_income
	data=data[data['Issue']==issue]
	data_train=data.ix[:, ['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE','AFAMERPER','WHITESPER','ASIANPER','HISPANICPER']]
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

	from bokeh.sampledata.us_counties import data as counties
	statename_to_abbr = {'District of Columbia': 'DC','Alabama': 'AL','Montana': 'MT','Alaska': 'AK','Nebraska': 'NE','Arizona': 'AZ','Nevada': 'NV','Arkansas': 'AR','NewHampshire': 'NH','California': 'CA','NewJersey': 'NJ','Colorado': 'CO','NewMexico': 'NM','Connecticut': 'CT','NewYork': 'NY','Delaware': 'DE','NorthCarolina': 'NC','Florida': 'FL','NorthDakota': 'ND','Georgia': 'GA','Ohio': 'OH','Hawaii': 'HI','Oklahoma': 'OK','Idaho': 'ID','Oregon': 'OR','Illinois': 'IL','Pennsylvania': 'PA','Indiana': 'IN','RhodeIsland': 'RI','Iowa': 'IA','SouthCarolina': 'SC','Kansas': 'KS','SouthDakota': 'SD','Kentucky': 'KY','Tennessee': 'TN','Louisiana': 'LA','Texas': 'TX','Maine': 'ME','Utah': 'UT','Maryland': 'MD','Vermont': 'VT','Massachusetts': 'MA','Virginia': 'VA','Michigan': 'MI','Washington': 'WA','Minnesota': 'MN','WestVirginia': 'WV','Mississippi': 'MS','Wisconsin': 'WI','Missouri': 'MO','Wyoming': 'WY'}
	keys=counties.keys()
	locations=[]
	for i in keys:
		if i[0]==46:#Need to add 2-AK, 11-DC (no data),15 HI - Maui, 19-IO no data, 21 KY -no data, 22-LA check unreasonable results for total (same with MA), 26 -MI need data, MN - need data, 30 - MT need data, 32 NV - need data, 33 - NH need data, NM - need data, 38 - ND need data, 40 -OK need data, 46 -SD meeds data, 51, VA - need data (download), 53 WA need data
			#print(i)
			name=counties[i]['detailed name'].split(',')
			name[0]=name[0].replace(' ','').replace('County','').replace('Parish','')
			name[1]=name[1].replace(' ','')
			location=statename_to_abbr[name[1]]+'_'+name[0].replace('County','').replace('.','').upper()
			locations.append(location)

	#print(locations)
	#location=str(state).upper()+"_"+str(county).upper()
	county_lookup=pd.read_csv('data_county_lookup.csv')
	county_lookup['clinton_margin']=county_lookup['CLINTON_%']-county_lookup['TRUMP_%']
	county_lookup['PER_CAPITA_INCOME']=county_lookup['PER_CAPITA_INCOME']/max_income

	predictions=[]
	#for place in location:
	state_name=locations[0][:2].lower()
	for place in locations:
		#print(place)
		PredictX=county_lookup[county_lookup['STATE_COUNTY']==place]
		PredictX=PredictX.ix[:, ['clinton_margin','PER_CAPITA_INCOME','UNINSURED_RATE','SOME_COLLEGE','AFAMERPER','WHITESPER','ASIANPER','HISPANICPER']]
		GLR_predict=GLR.predict(PredictX)*100.0
		predictions.append(round(GLR_predict[0]))
	script, div=plot(locations, predictions, state_name)

	return pcc, scc, pcc_p, scc_p, GLR_R2, GLR_predict[0]*100.0, PredictX.iloc[0,0]*100.0, PredictX.iloc[0,1]*max_income, PredictX.iloc[0,2], PredictX.iloc[0,3], N, script, div



if __name__ == '__main__':
  app.run(port=33507)
