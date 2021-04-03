#!python

# Initial settings

import numpy as np
import pandas as pd
import sys
import time
import random
import os
import csv
import matplotlib.pyplot as plt
import scipy.special


class WhitakterHenderson: 
	def __init__(self):
		#print("Constructor called.")
		self.__g = 1
		self.__m = 2
		self.__weights = None
		self.__weights_set_flag = False
		self.__weights_set_unif_flag = True
		self.__data_unsmoothened = None
		self.__data_smoothened = None

	def __del__(self): 
		pass#print("Destructor called.")

	def K(self, n, m): 
		mat_K = np.zeros((n-m, n))
		for i in range(1, n-m + 1):
			for j in range(1, n+1):
				if i==j:
					for s in range(1, m+1+1):
						mat_K[i-1][j+s-1-1] = (-1)**(s-1) * scipy.special.binom(m,s-1)
		return mat_K

	def W(self, n): 
		mat_W = np.zeros((n,n))
		w_sum = self.__weights.sum()
		
		for i in range(1,n+1):
			for j in range(1,n+1):
				if i==j:
					mat_W[i-1][j-1] = (self.__weights[i-1] / w_sum)
		return mat_W

	def binomialkoeffizient(self, n, k): 
		if k>n:  return 0
		if n==k: return 1
		if n>k:  return self.fakultaet(n)/(self.fakultaet(k) * self.fakultaet(n-k))

	def fakultaet(self, p_n): 
		if p_n==0:
			return 1
		else:
			return p_n * fakultaet(p_n-1)

	def set_weights(self, p_weights = None):
		try:
			if p_weights == None:
				#self.__weights = np.empty(len(self.__data_unsmoothened))
				#self.__weights.fill(1)
				self.__weights = np.array(np.full(len(self.__data_unsmoothened), 1))
				self.__weights_set_flag = True
				self.__weights_set_unif_flag = True
		except:
				self.__weights =  np.array(p_weights)
				self.__weights_set_flag = True
				self.__weights_set_unif_flag = False
	
	def get_weights(self):
		return self.__weights

	def get_weights_uniform_flag(self):
		return self.__weights_set_unif_flag

	def set_data_unsmoothened(self, p_data):
		self.__data_unsmoothened = p_data

	def fit(self):
		m = self.__m
		g = self.__g
		try:
			n = len(self.__data_unsmoothened)
		except:
			print("Data has Not been set !")

		if self.__weights_set_flag == False:
			self.set_weights()
		sub_part_1 = np.linalg.inv(self.W(n) + g * np.dot(np.transpose(self.K(n,m)),self.K(n,m)))
		sub_part_2 = np.dot(sub_part_1, self.W(n))
		self.__data_smoothened = np.dot(sub_part_2, self.__data_unsmoothened)

	def get_data_smoothened(self):
		return self.__data_smoothened

	def get_data_unsmoothened(self):
		return self.__data_unsmoothened

	def set_g(self, p_g):
		self.__g = p_g

	def set_m(self, p_m):
		self.__m = p_m
	
	def get_g(self):
		return self.__g
	
	def get_m(self):
		return self.__m

	def plot_data(self):
		plt.plot(self.__data_unsmoothened)
		plt.plot(self.__data_smoothened)
		#plt.plot(x, y, 'o')
		#plt.axhline(y, c = "orange")
		#plt.title("")
		plt.legend(['Raw data', 'Smoothed g=' + str(self.get_g()) +
												', m=' + str(self.get_m()) +
												", weights " + ( 'unif' if self.get_weights_uniform_flag() else 'modi')])
		plt.show()
