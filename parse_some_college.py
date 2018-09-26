#!/bin/python

#Data from https://datausa.io/map/?level=county&key=uninsured

statename_to_abbr = {
    # Other
    'District of Columbia': 'DC',

    # States
    'Alabama': 'AL',
    'Montana': 'MT',
    'Alaska': 'AK',
    'Nebraska': 'NE',
    'Arizona': 'AZ',
    'Nevada': 'NV',
    'Arkansas': 'AR',
    'New Hampshire': 'NH',
    'California': 'CA',
    'New Jersey': 'NJ',
    'Colorado': 'CO',
    'New Mexico': 'NM',
    'Connecticut': 'CT',
    'New York': 'NY',
    'Delaware': 'DE',
    'North Carolina': 'NC',
    'Florida': 'FL',
    'North Dakota': 'ND',
    'Georgia': 'GA',
    'Ohio': 'OH',
    'Hawaii': 'HI',
    'Hawaiʻi': 'HI',
    'Oklahoma': 'OK',
    'Idaho': 'ID',
    'Oregon': 'OR',
    'Illinois': 'IL',
    'Pennsylvania': 'PA',
    'Indiana': 'IN',
    'Rhode Island': 'RI',
    'Iowa': 'IA',
    'South Carolina': 'SC',
    'Kansas': 'KS',
    'South Dakota': 'SD',
    'Kentucky': 'KY',
    'Tennessee': 'TN',
    'Louisiana': 'LA',
    'Texas': 'TX',
    'Maine': 'ME',
    'Utah': 'UT',
    'Maryland': 'MD',
    'Vermont': 'VT',
    'Massachusetts': 'MA',
    'Virginia': 'VA',
    'Michigan': 'MI',
    'Washington': 'WA',
    'Minnesota': 'MN',
    'West Virginia': 'WV',
    'Mississippi': 'MS',
    'Wisconsin': 'WI',
    'Missouri': 'MO',
    'Wyoming': 'WY',
    'American Samoa' : 'TR',
    'Guam' : 'TR',
    'Northern Mariana Islands' : 'TR',
    'Puerto Rico' : 'TR',
    'U.S. Minor Outlying Islands' : 'TR',
    'Virgin Islands (U.S.)': 'TR'
}

fr=open('raw_data_some_college2.txt','r')
fr_county=open('list_of_counties_us.txt','r')
data=fr.readlines()

counties=fr_county.readlines()
county_lookup={}
state_lookup={}
for i in counties:
	x=i.split('\t')
	county_lookup[x[0]]=x[1].replace('County','').replace(' ','').upper()
	state_lookup[x[0]]=statename_to_abbr[x[2]]

print('UnInsYEAR','STATE_COUNTY','PERCENT_UNINSURED')
for i in data:
	x=i.split('\t')
	if x[0]!='year' and x[1]!='None':
		id_county=x[2][-5:]
		#print(state_lookup[id_county]+'_'+county_lookup[id_county])
		print(x[0],state_lookup[id_county]+'_'+county_lookup[id_county],x[3].replace('\n',''),sep=',')
