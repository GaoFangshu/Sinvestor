# -*- coding: utf-8 -*-

import pandas as pd
import model

EPOCHS = 10
BATCH_SIZE = 64

COMPANY_SHAPE = 1384
INVESTOR_SHAPE = 1452
CROSS_DIM = 6

class data_train():
	"""Data class for model directly"""
	def __init__(self, name):
		self.name = name
		self.data = pd.read_csv('./data/saved_data/%s'%name)
		self.x_train = [self.data.iloc[:,:1384], self.data.iloc[:,1384:2836], self.data.iloc[:,2836:-1]]
		self.y_train = self.data.iloc[:,2836:-1]

if __name__ == '__main__':
	data = data_train('saved_data.csv')
	main_model = model.branchmodel(COMPANY_SHAPE, INVESTOR_SHAPE, CROSS_DIM)
	main_model.fitmodel_data(data, EPOCHS, BATCH_SIZE)
	main_model.savemodel('branchmodel-10')