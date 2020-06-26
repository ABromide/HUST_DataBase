import pandas as pd

def change_format(location,item):
	data1 = pd.read_csv(location + '/2020-05-20_in_' + item + '.csv')
	data2 = pd.read_csv(location + '/2020-05-20_out_' + item + '.csv')
	data = pd.concat([data1,data2])

	for i in range(21,32):
		d1 = pd.read_csv(location + '/2020-05-' + str(i) + '_in_' + item + '.csv')
		d2 = pd.read_csv(location + '/2020-05-' + str(i) + '_out_' + item + '.csv')
		data = pd.concat([data,d1])
		data = pd.concat([data,d2])

	for i in range(1,4):
		d1 = pd.read_csv(location + '/2020-06-0' + str(i) +'_in_' + item + '.csv')
		d2 = pd.read_csv(location + '/2020-06-0' + str(i) +'_out_' + item + '.csv')
		data = pd.concat([data,d1])
		data = pd.concat([data,d2])

	data = data.drop(['Unnamed: 0'],axis=1)
	data.to_csv(location+'.csv',index=0)

change_format('DirectInfo','direct')
change_format('TransitInfo','transit')