import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

regions = {
	'Sul': ['SC', 'RS', 'PR'],
	'Sudeste': ['SP', 'RJ', 'ES', 'MG'],
	'Centro-Oeste': ['GO', 'MS', 'MT', 'DF'],
	'Norte': ['AC', 'AM', 'AP', 'PA', 'RR', 'RO', 'TO'],
	'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
}

def read_file():
	df = pd.read_csv('coords.txt', sep=";", header=None)
	df.columns = ['Localization', 'State', 'Abbreviation', 'Latitude', 'Longitude']
	return df

def get_number_of_locs_by_state(df):
	temp = df.set_index('State').groupby(level=0)['Abbreviation'].agg('count')
	df2 = pd.DataFrame({'State': temp.index, 'Count': temp.values})
	df2 = df2.set_index('State')
	return df2

def distance(lat1, lon1, lat2, lon2):
	R = 6371.0
	dLat = (lat2 - lat1) * np.pi / 180.0
	dLon = (lon2 - lon1) * np.pi / 180.0
	a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(lat1 * np.pi / 180.0) * np.cos(lat2 * np.pi / 180.0) * np.sin(dLon / 2) * np.sin(dLon / 2)
	c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
	d = R * c
	return d

def get_data_by_state(df, abbr):
	res = df[df['Abbreviation'] == abbr]
	return res

def get_data_by_region(df, region):
	states = regions[region]
	res = df[df['Abbreviation'].isin(states)]
	return res
	

def get_map(df):
	coords = df[['Latitude', 'Longitude']]

	fig = plt.figure()

	'''
	llcrnrlat - lower-left corner longitude
	urcrnrlat - lower-left corner latitude
	llcrnrlon - upper-right corner longitude
	urcrnrlon - upper-right corner latitude
	'''
	m = Basemap(projection='gall',
		llcrnrlat=coords.Latitude.min()-5,
		urcrnrlat=coords.Latitude.max()+5,
		llcrnrlon=coords.Longitude.min()-5,
		urcrnrlon=coords.Longitude.max()+5,
		resolution='i',
		area_thresh=100000)

	m.drawcoastlines()
	m.drawcountries()
	m.drawstates()
	m.fillcontinents(color='gray')
	m.drawmapboundary(fill_color='steelblue')

	x, y = m(coords['Longitude'].tolist(), coords['Latitude'].tolist())
	m.plot(x, y, 'o', color='Indigo', markersize=4)
	#plt.show()

	return plt