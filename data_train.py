# -*- coding: utf-8 -*-

from keras.models import load_model
import pandas as pd
import numpy as np
import model

OPEN_EPOCHS = 10
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

# # -------------------- 分支结构的生成读取以及训练 --------------------
# if __name__ == '__main__':
#     data = data_train('merged.csv')
#     print('------------- 数据准备完毕 -------------')
#     print('------------- 开始创建分支结构 -------------')
#     main_model = model.branchmodel(COMPANY_SHAPE, INVESTOR_SHAPE, CROSS_DIM, load_model_flag=OPEN_EPOCHS)
#     print('------------- 开始进行训练 -------------')
#     main_model.fitmodel_data(data, EPOCHS, BATCH_SIZE)
#     main_model.savemodel('branchmodel-%d'%(OPEN_EPOCHS+EPOCHS))
#     print('------------- 模型保存完毕 -------------')

# -------------------- 全连接结构的生成读取以及训练 --------------------
if __name__ == '__main__':
    data = data_train('merged.csv')
    print('------------- 数据准备完毕 -------------')
    print('------------- 开始创建全连接结构 -------------')
    main_model = model.sequentialmodel(COMPANY_SHAPE, INVESTOR_SHAPE, CROSS_DIM, load_model_flag=OPEN_EPOCHS)
    print('------------- 开始进行训练 -------------')
    main_model.fitmodel_data(data, EPOCHS, BATCH_SIZE)
    main_model.savemodel('sequentialmodel-%d'%(OPEN_EPOCHS+EPOCHS))
    print('------------- 模型保存完毕 -------------')    
