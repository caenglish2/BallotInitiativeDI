# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 15:43:03 2018

@author: caenglish
"""
#Does keyword search on ballot question text
import pandas as pd

#For CA
data=pd.read_csv('CA_ballot.txt',sep=',')

data['Obligation']=data['Ballotquestion']
#len(data)
print('Starting scan')
fw=open('ballot_issues.csv','w')
fw.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%('STATE_COUNTY','PERCENT','tax','property_tax','sales_tax','business_tax','utility_tax','hotel_tax','bonds','ordinance','infrastructure','roads','parks','social_services','mental_health','substance_abuse','affordable_housing','emergency_services','fire','police','paramedic','spending_limit','cannabis','education','library','school','land_use'))
#len(data)
for i in range(len(data['PERCENT'])):
	if float(data['PERCENT'].ix[i][:-1])<1.0:
		data['PERCENT'].ix[i]=str(float(data['PERCENT'].ix[i][:-1])*100.0)
	else:
		data['PERCENT'].ix[i]=data['PERCENT'].ix[i][:-1]

print(data['PERCENT'].head(10))
for row in range(0,len(data)):
    fw.write('%s,'%('CA'+'_'+data['CNTYNAME'].iloc[row]))
    fw.write('%s,'%data['PERCENT'].iloc[row][:-1])
    question=data['Ballotquestion'].iloc[row]
    question=question.lower()
    obligations=[];issues=[]
    #print(question)
    #Guess the obligation from the ballot question text

    if 'tax' in question or 'Tax' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')

    if 'parcel' in question or 'residential lot' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'sales tax' in question or 'transactions' in question or 'sales and use' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'business tax' in question or 'businesses' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'utility users' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'hotel' in question and 'charges' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
            
    if 'bonds' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'ordinance' in question:
        fw.write('%s'%'1,')
    else:     
        fw.write('%s'%'0,')


    #Issues relevant
    if 'road' in question or 'sidewalk' in question or 'park' in question or 'landscape' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'road' in question or 'street repairs' in question or 'repair streets' in question or 'streets' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'park' in question or 'parks' in question or 'landscape' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
            
    if 'mental health' in question or 'substance abuse' in question or 'affordable housing' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'mental health' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'substance abuse' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'affordable housing' in question:
        fw.write('%s'%'1,')
    else:   
        fw.write('%s'%'0,')
            
    if "public safety" in question or "fire" in question or "sheriff" in question or 'law enforcement' in question or 'police' in question or 'paramedic' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')     
        
    if "fire" in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if "sheriff" in question or 'law enforcement' in question or 'police' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'paramedic' in question or 'emergency medical services' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
            
    if 'spending limit' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'cannabis' in question or 'marijuana' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'library' in question or 'school' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'library' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'school' in question:
        fw.write('%s'%'1,')
    else:
        fw.write('%s'%'0,')
        
    if 'land use' in question:
        fw.write('%s'%'1')
    else:
        fw.write('%s'%'0')
    fw.write('\n')
            
fw.close()
