# -*- coding: utf-8 -*-

from keras.layers import Input, Dense
from keras.models import Model
import numpy as np
from data_proc import get_invest_data, get_company_data
import matplotlib.pyplot as plt

# ------------------- Set hyperparameters -------------------

train_size = 3000 # maxnum 4297 in data
# test_size: 4297 - train_size

encoding_dim = 50  # size of our encoded representations, assuming the input is 784 floats
nb_epoch_autoencoder = 50
batch_size_autoencoder = 30

dense1_dim = 1000
nb_epoch_main = 30
batch_size_main = 1000


# ------------------- Load data -------------------

data_invest = get_invest_data()
print('■■■■■■■ 已读取 投资机构数据，维度：(' + str(data_invest.shape[0]) + ',' + str(data_invest.shape[1]) + ') ■■■■■■■')
data_company = get_company_data()
print('■■■■■■■ 已读取 创业公司数据，维度：(' + str(data_company.shape[0]) + ',' + str(data_company.shape[1]) + ') ■■■■■■■')
all_investor = data_invest[:, 0]


# normalization
data_company[:,-1] = data_company[:,-1]/data_company[:,-1].max()
data_company[:,6] = data_company[:,6]/data_company[:,6].max()

# get investor list in round 1
investor_1 = data_company[:,2:6].tolist() # length: 6527
unique_investor = []
investor_list = []
for i in range(len(investor_1)):
    sublist = []
    for j in range(len(investor_1[i])):
        if investor_1[i][j] != '无记录':
            unique_investor.append(investor_1[i][j])
            sublist.append(investor_1[i][j])
    investor_list.append(sublist) # length: 6527
unique_investor = list(set(unique_investor)) # length: 1300


# ------------------- Get intersection -------------------

check_investor_in_company = []
for i in range(len(all_investor)):
    check_investor_in_company.append(all_investor[i] in unique_investor)
data_invest_new = data_invest[check_investor_in_company, :] # shape: (1082, 43)
print('■■■■■■■ 取交集后 投资机构 数据维度：(' + str(data_invest_new.shape[0]) + ',' + str(data_invest_new.shape[1]) + ') ■■■■■■■')

check_company_in_investor = []
for i in range(len(data_company)):
    check_line = 0
    for j in range(len(investor_list[i])):
        if investor_list[i][j] not in data_invest_new[:,0]:
            check_line += 1
    if check_line:
        check_company_in_investor.append(False)
    else:
        check_company_in_investor.append(True)
data_company_new = data_company[check_company_in_investor, :] # shape: (4297, 1806)
print('■■■■■■■ 取交集后 创业公司 数据维度：(' + str(data_company_new.shape[0]) + ',' + str(data_company_new.shape[1]) + ') ■■■■■■■')


# ------------------- Final data -------------------

y_data = np.array(investor_list)[check_company_in_investor] # shape: (4297,)
x_data = data_company_new[:, 6:] # shape: (4297, 1800)
num_investor = data_invest_new.shape[0]
print('■■■■■■■ 最终数据中一共有 ' + str(num_investor) + ' 个投资机构. ■■■■■■■')
print('■■■■■■■ x_data 数据维度：(' + str(x_data.shape[0]) + ',' + str(x_data.shape[1]) + ') ■■■■■■■')
print('■■■■■■■ y_data 数据维度：(' + str(y_data.shape[0]) + ', ) ■■■■■■■ ')



# ------------------- Concatenate encoded training data with number label data -------------------

def add_investors(encoded_data, y_train, num_data, num_investor):
    encoded_data_new = encoded_data.repeat(num_investor, axis=0)  # shape: (60000, 16), encoded_imgs: (6000, 16)
    y_train_new = np.zeros((encoded_data.shape[0] * num_investor, 2)) # shape: (60000, 2)
    for i in range(y_train_new.shape[0]): # i=0-5999
        if num_data[i%num_investor, 0] in y_train[i//num_investor]: # 这里是针对数字的特例，程序简化了，但实际上在投资企业时是根据编号确定的
            y_train_new[i, 0] = 1.0 # Yes
            #print("ok")
        else:
            y_train_new[i, 1] = 1.0 # No
    num_data_new = np.tile(num_data[:, 1:], (encoded_data.shape[0], 1)) # shape: (60000, 625)
    train_new = np.concatenate([encoded_data_new, num_data_new], axis=1) # shape: (60000, 16+625)
    return([train_new, y_train_new])


# ------------------- Form testing data -------------------

def form_test(y_test, num_data, num_investor):
    y_test_new = np.zeros((y_test.shape[0] * num_investor, 2)) # shape: (60000, 2)
    for i in range(y_test_new.shape[0]): # i=0-5999
        if num_data[i%num_investor, 0] in y_train[i//num_investor]: # 这里是针对数字的特例，程序简化了，但实际上在投资企业时是根据编号确定的
            y_test_new[i, 0] = 1.0 # Yes
            #print("ok")
        else:
            y_test_new[i, 1] = 1.0 # No
    return (y_test_new)


# -------------------  Choose autoencoder -------------------
train_dimension = x_data.shape[1]
input_dataset = Input(shape=(train_dimension,)) # input placeholder
encoded = Dense(encoding_dim, activation='relu')(input_dataset)
decoded = Dense(train_dimension, activation='sigmoid')(encoded)
autoencoder = Model(input=input_dataset, output=decoded)
encoder = Model(input=input_dataset, output=encoded)

autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')


x_train = x_data[:train_size,:]
y_train = y_data[:train_size]
x_test = x_data[train_size:,:]
y_test = y_data[train_size:]
test_size = x_data.shape[0] - train_size
print('■■■■■■■ x_train 数据维度：(' + str(x_train.shape[0]) + ',' + str(x_train.shape[1]) + ') ■■■■■■■')
print('■■■■■■■ x_test 数据维度：(' + str(x_test.shape[0]) + ',' + str(x_test.shape[1]) + ') ■■■■■■■')

print('■■■■■■■ 开始训练自编码机...目标维度：('+ str(encoding_dim) + ',' + str(encoding_dim) + ') ■■■■■■■')

## train
autoencoder.fit(x_train, x_train,
                nb_epoch=nb_epoch_autoencoder,
                batch_size=batch_size_autoencoder,
                shuffle=True,
                validation_data=(x_test, x_test))

encoded_data = encoder.predict(x_train)


# ------------------- Add investors to train data -------------------

print('■■■■■■■ 开始合并投资机构数据... ■■■■■■■')
train_new = add_investors(encoded_data, y_train, data_invest_new, num_investor)
print('■■■■■■■ 合并完成 ■■■■■■■')
# XXX = add_investors(x_data[:5, :], y_data[:5, :], data_company_new, num_investor)
x_train_new = train_new[0]
y_train_new = train_new[1]
print('■■■■■■■ 合并后训练集维度：(' + str(x_train_new.shape[0]) + ',' + str(x_train_new.shape[1]) + ') ■■■■■■■')


# ------------------- main model -------------------
main_dim = data_invest_new.shape[1]-1 + encoding_dim
input_data = Input(shape=(main_dim,))
dense1 = Dense(dense1_dim, activation='relu')(input_data)
output_data = Dense(2, activation='softmax')(dense1)
main_model = Model(input=input_data, output=output_data)
main_model.compile(optimizer='adadelta', loss='binary_crossentropy')

print('■■■■■■■ 开始训练神经网络模型... ■■■■■■■')
main_model.fit(x_train_new, y_train_new,
                nb_epoch=nb_epoch_main,
                batch_size=batch_size_main,
                shuffle=True)
print('■■■■■■■ 训练完成 ■■■■■■■')
encoded_imgs_test = encoder.predict(x_test)

test_new = add_investors(encoded_imgs_test, y_test, data_invest_new, num_investor)
x_test_new = test_new[0]

result_test = main_model.predict(x_test_new)
print('■■■■■■■ 预测结果已输出 ■■■■■■■')

result_index = np.tile(np.array(range(num_investor))+1, (test_size, 1)).reshape(num_investor*test_size,1)

result_y = form_test(y_test, data_invest_new, num_investor)
result = np.concatenate([result_test, result_y, np.zeros((result_y.shape[0],1))], axis=1)

for i in range(int(len(result)/num_investor)):
    result[i*num_investor:(i+1)*num_investor,4] = i+1
    current_tile = result[i*num_investor:(i+1)*num_investor,:]
    sorted_tile = current_tile[np.argsort(-current_tile[:,0]), :]
    result[i*num_investor:(i+1)*num_investor,:] = sorted_tile

result_graph = np.concatenate([result[:, [2,4]],result_index],axis=1)
plot_points = result_graph[result_graph[:,0]==1, 1:]

print('■■■■■■■ 开始作图... ■■■■■■■')
fig = plt.figure()
graph = fig.add_subplot(1,1,1)
plt.ylim([0,num_investor])
plt.xlim([0,test_size+1])
plt.axhline(4)
graph.scatter(plot_points[:, 0], plot_points[:, 1])
plt.show()
print('■■■■■■■ 作图完成，清真否？蛤蛤蛤 ■■■■■■■')
Acc = np.mean(plot_points[:, 1])
print('■■■■■■■ 正确率：' + str(Acc) + ' ■■■■■■■')

# 贡献均衡
# 爬数据
# keras.generator
# 多线程，独立处理数据和学习模型
# 写一个Acc
# 存数据