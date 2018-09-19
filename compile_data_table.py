#!/bin/python

states=['AL','AR','AZ','CA','CO','CT','DE','FL','LA','NY','MD','MA','TX']
states=['AL','AR','AZ','CA','CO','CT','FL','LA','NY','MD','MA','TX']
#DE, CA need to be fixed
county_name=[]
state_name=[]
trump_num=[];trump_per=[]
clinton_num=[];clinton_per=[]
johnson_num=[];johnson_per=[]
stein_num=[];stein_per=[]

#Tfirst_norm=['AL','AR','AZ']

for state in states:
	fr=open('%s.txt'%state,'r')
	data=fr.readlines()
	if state in ['AL','AZ','DE','TX','AR','FL']:#Trump,Clinton
		for i in range(len(data)):
			state_name.append('%s'%state)
			data_line=data[i].split('\t')
			county_name.append(data_line[0])
			trump_num.append(int(data_line[1].replace(',','')))
			trump_per.append(float(data_line[2][:-1])/100.0)
			clinton_num.append(int(data_line[3].replace(',','')))
			clinton_per.append(float(data_line[4][:-1])/100.0)
	elif state=='CO':#Clinton,Trump
		for i in range(len(data)):
			data_line=data[i].split('\t')
			if data_line[0]!='County':
				state_name.append('%s'%state)
				county_name.append(data_line[0])
				trump_num.append(int(data_line[4].replace(',','')))
				trump_per.append(float(data_line[3][:-1])/100.0)
				clinton_num.append(int(data_line[2].replace(',','')))
				clinton_per.append(float(data_line[1][:-1])/100.0)
	elif state in ['CT']:#Clinton,Trump
		for i in range(len(data)):
			data_line=data[i].split('\t')
			if data_line[0]!='County':
				state_name.append('%s'%state)
				county_name.append(data_line[0])
				trump_num.append(int(data_line[3][:-8]+data_line[3][-7:-4]+data_line[3][-3:]))
				trump_per.append(float(data_line[4][:-1])/100.0)
				clinton_num.append(int(data_line[1][:-8]+data_line[1][-7:-4]+data_line[1][-3:]))
				clinton_per.append(float(data_line[2][:-1])/100.0)
	elif state in ['NY']:#Clinton,Trump,Johnson,Stein, % then num
		for i in range(len(data)):
			data_line=data[i].split('\t')
			if data_line[0]!='County':
				state_name.append('%s'%state)
				county_name.append(data_line[0])
				trump_num.append(int(data_line[4][:-8]+data_line[4][-7:-4]+data_line[4][-3:]))
				trump_per.append(float(data_line[3][:-1])/100.0)
				clinton_num.append(int(data_line[2][:-8]+data_line[2][-7:-4]+data_line[2][-3:]))
				clinton_per.append(float(data_line[1][:-1])/100.0)
	elif state in ['CA']:#Chart with percentages and votes in different lines
		for i in range(len(data)):
			data_line=data[i].split('\t')
			if data_line[0][:7]=='Clinton':
				pass
			elif data_line[0]=='votes':
				trump_num.append(int(data_line[2].replace(',','')))
				clinton_num.append(int(data_line[1].replace(',','')))
			elif data_line[1]=='percent':
				state_name.append('%s'%state)
				county_name.append(data_line[0])
				trump_per.append(float(data_line[3][:-1])/100.0)
				clinton_per.append(float(data_line[2][:-1])/100.0)

	elif state in ['MD','MA','LA']:#Chart with percentages and votes in different lines
		for i in range(len(data)):
			if i==0: pass
			else:
				state_name.append('%s'%state)
				data_line=data[i].split('\t')
				county_name.append(data_line[0])
				trump_num.append(int(data_line[2].replace(',','')))
				trump_per.append(float(data_line[1].replace('%',''))/100.0)
				clinton_num.append(int(data_line[4].replace(',','')))
				clinton_per.append(float(data_line[3].replace('%',''))/100.0)
			#else:
				#state_name.append('%s'%state)
				#county_name.append(data_line[0])
				#trump_per.append(float(data_line[2][:-1])/100.0)
				#clinton_per.append(float(data_line[3][:-1])/100.0)
				#johnson_per.append(float(data_line[4][:-1])/100.0)
				#stein_per.append(float(data_line[5][:-1])/100.0)
		
		

print('STATE_COUNTY','TRUMP_N','TRUMP_%','CLINTON_N','CLINTON_%',sep=',')
for i in range(len(county_name)):
	print(state_name[i].upper()+'_'+county_name[i].upper(), trump_num[i], trump_per[i], clinton_num[i], clinton_per[i],sep=',')
