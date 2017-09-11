# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
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
        self.data = pd.read_csv('./data/%s'%name)
        self.x_train = [np.asarray(self.data.iloc[:,:1384]), np.asarray(self.data.iloc[:,1384:2836]), np.asarray(self.data.iloc[:,2836:-1])]
        self.y_train = np.asarray(self.data.iloc[:,-1:])

if __name__ == '__main__':
    data = data_train('merged.csv')
    print('------------- 数据准备完毕 -------------')
    print('------------- 开始创建分支结构 -------------')
    main_model = model.branchmodel(COMPANY_SHAPE, INVESTOR_SHAPE, CROSS_DIM)
    print('------------- 开始进行训练 -------------')
    main_model.fitmodel_data(data, EPOCHS, BATCH_SIZE)
    main_model.savemodel('branchmodel-10')
    print('------------- 模型保存完毕 -------------')
