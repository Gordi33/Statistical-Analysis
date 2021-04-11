#!python

# Initial settings

import numpy as np
import pandas as pd
import scipy.stats
import math
import sys
import time
import researchpy as rp
import pyodbc
import os
import csv
from matplotlib import pyplot
import matplotlib.pyplot as plt
from IPython.display import HTML
import sklearn as skl
import seaborn as sns
from collections import Counter
import string
import re
import pickle
from IPython.display import clear_output
from datetime import date,datetime, timedelta as td
from scipy.stats import *
import warnings
from statsmodels.graphics.gofplots import qqplot
from scipy import stats


class Analyser:

	# -------            -----------------------------------------------------------
	def __init__(self):
		pass

	# -------            -----------------------------------------------------------
	def __del__(self):
		print("Destructor called.")

	# -------            -----------------------------------------------------------
	def chi_squared_test(self, p_columnDEP, p_columnINDEP, p_maxNumAttributes = 6):
		tableREL, results, exp = rp.crosstab(p_columnDEP, p_columnINDEP, prop='col', test= 'chi-square', expected_freqs= True)
		tableABS = rp.crosstab(p_columnDEP, p_columnINDEP)

		ct = pd.crosstab(p_columnDEP, p_columnINDEP, normalize ='columns').reset_index()
		ct = ct.transpose()

		stacked = ct.stack().reset_index().rename(columns={0:'value'})
		stacked = eval('stacked[stacked.' + p_columnINDEP.name + '!= p_columnDEP.name]')
		stacked = stacked.rename(columns={"level_1": p_columnDEP.name})

		_myPlot = eval('sns.barplot(x=stacked.' + p_columnINDEP.name + ', y=stacked.value, hue=stacked.' + p_columnDEP.name + ')')

		a  = str(len(tableABS.columns) - 1) + ' attributes'
		a0 = '--------------------------------------------------------------------------------------'
		a1 = '----------------------------------------------------------------- OBSERVED FREQUENCIES'
		a2 = '------------------------------------------------------ OBSERVED FREQUENCIES (relative)'
		a3 = '----------------------------------------------------------------- EXPECTED FREQUENCIES'
		a4 = '------------------------------------------------------------------------- TEST RESULTS'
		a5 = '--------------------------------------------------------------------------------- PLOT'

		if len(tableABS.columns) - 1 > p_maxNumAttributes:
			b1 = '--- not plotted --- number of attributes with ' + str(len(tableABS.columns) - 1) + ' is too big ---------------------------'
			return [a, a0, a1, a0, b1, a2, b1, a3, b1, a4, results, a5, _myPlot]  
		else:
			return [a, a0, a1, a0, tableABS, a0, a2, a0, tableREL, a0, a3, a0, round(exp,0), a0, a4, a0, results, a0, a5, a0, _myPlot]  

	# -------            -----------------------------------------------------------
	def mann_whitney_U_test(self, p_columnDEP, p_columnINDEP):
		if len(p_columnDEP.unique()) != 2:
			return 'The dependent attribute needs to have two characteristics !!!'
		else:
			a0 = '--------------------------------------------------------------------------------------'
			a1 = '----------------------------------------------------------------- OBSERVED FREQUENCIES'
			temp = pd.DataFrame()
			temp[p_columnDEP.name] = p_columnDEP
			temp[p_columnINDEP.name] = p_columnINDEP
			temp['Total'] = 1
			a2 = temp.groupby(p_columnDEP.name).count().reset_index()[[p_columnDEP.name,'Total']]
			temp['Rank_Avg'] = rankdata(temp[p_columnINDEP.name])
			temp_0 = temp[temp[p_columnDEP.name] == temp[p_columnDEP.name].unique()[0]]
			temp_1 = temp[temp[p_columnDEP.name] == temp[p_columnDEP.name].unique()[1]]
			a3 = '-------------------------------------------------------------------- AVERGAE RANKSUMS'
			a4 = p_columnDEP.name + ' = ' + str(temp[p_columnDEP.name].unique()[0]) + '    E(sum(rank)) = ' + str(round(temp_0['Rank_Avg'].mean(),2))
			a5 = p_columnDEP.name + ' = ' + str(temp[p_columnDEP.name].unique()[1]) + '    E(sum(rank)) = ' + str(round(temp_1['Rank_Avg'].mean(),2))
			a6 = '                     E(sum(rank)) = ' + str(round(temp['Rank_Avg'].mean(),2))
			a7 = '------------------------------------------------------------------------- TEST RESULTS'
			u_statistic, p_value = stats.mannwhitneyu(temp_0[p_columnINDEP.name], temp_1[p_columnINDEP.name], True)
			a8 = 'U-Statistik:     ' + str(u_statistic)
			a9 = 'p-Value:         ' + str(round(100 * p_value, 4)) + ' %'
			a10 = '-------------------------------------------------------------------------------- PLOT'
			a11 = sns.boxplot( x=temp[p_columnDEP.name], y=temp[p_columnINDEP.name] )
			
			#a13 = temp_0[p_columnINDEP.name].hist()
			#a12 = temp_1[p_columnINDEP.name].hist()
			return [a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11]

	# -------            -----------------------------------------------------------
	def correlation_matrix(self, p_df, p_method='spearman'):
		plt.figure(figsize = (10, 10))
		sns.heatmap(p_df.corr(method = p_method), annot = True)

	# -------            -----------------------------------------------------------	
	def plot_distributions(self, p_df, p_header = None):
		if p_header is None:
			column_headers = tuple(p_df.select_dtypes(['number']).columns.values)
		else:
			column_headers = tuple(p_header)
		
		i = 1
		fig, ax = plt.subplots(2, 4, figsize = (20, 20))
		
		for column_header in column_headers:
			plt.subplot(2, 4, i)
			sns.distplot(p_df[column_header])
			i = i + 1

	# -------            -----------------------------------------------------------
	def plot_boxplots(self, p_df, p_header = None):
		if p_header is None:
			column_headers = tuple(p_df.select_dtypes(['number']).columns.values)
		else:
			column_headers = tuple(p_header)
		
		i = 1
		fig, ax = plt.subplots(2, 4, figsize = (20, 10))
		
		for column_header in column_headers:
			plt.subplot(2, 4, i)
			sns.boxplot(p_df[column_header], orient = "h")
			i = i + 1

	# -------            -----------------------------------------------------------
	def chi_square_test_for_each_category_level(self, p_columnDEP, p_columnINDEP):
		g = pd.get_dummies(p_columnINDEP)
		h = pd.DataFrame(p_columnDEP)
		k = h.join(g)
		k = k.reset_index().drop(['index'], axis=1)
		
		temp = pd.DataFrame(columns = ['AttrCharacteristic','AttrCharacteristicRenamed','ChiSq','p_value','CramerV'])
		
		for i in range(1,len(k.columns)):
			_from = k.columns[i]
			_to = re.sub('[^A-Za-z0-9_]+', '_', k.columns[i])
			k = k.rename(columns = { _from: _to })
			a, results = rp.crosstab(k[p_columnDEP.name], k[k.columns[i]], test= 'chi-square')
			temp = temp.append({'AttrCharacteristic':			_from,
								'AttrCharacteristicRenamed':	_to,
								'ChiSq':						results.iloc[0,1],
								'p_value':						results.iloc[1,1],
								'CramerV':						results.iloc[2,1]}
								, ignore_index=True)
		return temp.sort_values(by='CramerV', ascending=False, na_position='first')		

	# -------            -----------------------------------------------------------
	def variable_info(self, p_column):
		sns.countplot(x = p_column.name, data = pd.DataFrame(p_column), palette = 'hls')
		plt.show()
		count_no_fraud = sum(p_column == 0)
		count_fraud    = sum(p_column == 1)
		
		temp = pd.DataFrame(columns = [p_column.name, 'Absolute', 'Percentage'])
		
		pct_of_no_fraud = count_no_fraud / (count_no_fraud + count_fraud)	# print('{0:25} : {1:20}'.format('percentage of no fraud is', pct_of_no_fraud*100))
		pct_of_fraud = count_fraud / (count_no_fraud + count_fraud)			# print('{0:25} : {1:20}'.format('percentage of fraud is', pct_of_fraud*100))

		temp = temp.append({p_column.name:	'0',
							'Absolute':		count_no_fraud,
							'Percentage':	pct_of_no_fraud}, ignore_index=True)
		temp = temp.append({p_column.name:	'1',
							'Absolute':		count_fraud,
							'Percentage':	pct_of_fraud}, ignore_index=True)
		return temp

	# -------            -----------------------------------------------------------
	def apply_chi_squared_statistic_on_timeline(self, p_df, p_columnDEP, p_columnINDEP, p_dates):
		temp = p_df.copy(deep=True)
		temp2 = None
		temp_i = None
		
		function_start = time.time()
		print('Starting:' + '\t' + 'date: ' + '\t' + time.ctime())
		
		# create empty dataset
		temp2 = pd.DataFrame(columns = ['Starting_Date', 'ChiSq', 'p_value', 'CramerV'])
		
		for i in p_dates:
			starting = time.time()
			temp_i = temp[temp['starting_Date'] == i]
			ct, results = rp.crosstab(temp_i[p_columnDEP], temp_i[p_columnINDEP], test= 'chi-square')
			temp2 = temp2.append({	'Starting_Date':	i,
									'ChiSq':			results.iloc[0,1],
									'p_value':			results.iloc[1,1],
									'CramerV':			results.iloc[2,1]}, ignore_index=True)
		
		print('\n' + 'Duration: ' + '\t' + '{:5.3f}s'.format(time.time() - function_start) + '\n')
		return temp2

	# -------            -----------------------------------------------------------
	def apply_mann_whitney_U_statistic_on_timeline(self, p_df, p_columnDEP, p_columnINDEP, p_dates):
		temp = p_df.copy(deep=True)
		temp2 = None
		temp_i = None
		function_start = time.time()
		print('Starting:' + '\t' + 'date: ' + '\t' + time.ctime())

		# create empty dataset
		temp2 = pd.DataFrame(columns = ['Starting_Date', '_0', '_1', 'Avg_Rank_0', 'Avg_Rank_1', 'Avg_Rank', 'AvgR0_vsAvgR', 'AvgR1_vsAvgR'])

		for i in p_dates:
			starting = time.time()
			temp_i = temp[temp['starting_Date'] == i]
			_ranks = self.mann_whitney_U_test(temp_i[p_columnDEP], temp_i[p_columnINDEP], 'Rank_Avg') 
			temp2 = temp2.append({	'Starting_Date': i,
									'_0':				_ranks[0],
									'_1':				_ranks[1],
									'Avg_Rank_0':		_ranks[2],
									'Avg_Rank_1':		_ranks[3],
									'Avg_Rank':			_ranks[4],
									'AvgR0_vsAvgR':		_ranks[2] / _ranks[4],
									'AvgR1_vsAvgR':		_ranks[3] / _ranks[4]}, ignore_index=True)      

		print('\n' + 'Duration: ' + '\t' + '{:5.3f}s'.format(time.time() - function_start) + '\n')
		return temp2

	def normality_test(self, df, alpha = 0.05):
		pyplot.hist(df)
		qqplot(df, line='s')
		pyplot.show()
		Stats, p = stats.normaltest(df)
		print("Alpha      = {:g}".format(alpha))
		print("p          = {:g}".format(p))
		print("Statistik  =", Stats)
		if p > alpha:
		
			print('Sample looks Gaussian (fail to reject H0)')
		else:
			print('Sample does not look Gaussian (reject H0)')

