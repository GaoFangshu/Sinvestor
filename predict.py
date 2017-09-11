# -*- coding: utf-8 -*-

import pandas as pd
import data_proc
import check
from keras.models import load_model

MODEL_NAME = ''

class preparedata():
    """准备提取需要预测的公司信息并合成新数据集"""
    def __init__(self):
        super(preparedata, self).__init__()

        def getdata(path):
            f = open(path, 'r', encoding='utf-8')
            content = f.read()
            f.close()
            info_list = content.split('\n')
            info_list = [info.split(':') for info in info_list]
            info_list = [info[1] for info in info_list]
            data = '\t'.join(info_list)
            return data

        print('----------- 开始读取公司信息 -----------')
        data_company = getdata('./output/创业公司信息.txt')
        data_valution = getdata('./output/公司估值.txt')
        data_companies = open('./data/IT橘子创业公司信息.txt', 'r')
        data_valutions = open('./data/IT橘子雷达公司估值.txt', 'r')
        print('----------- 已经读取公司信息 -----------')

        data_companies = data_companies.read() + data_company + '\n'
        data_valutions = data_valutions.read() + data_valution + '\n'

        f_companies = open('./output/setting/IT橘子创业公司信息.txt', 'w')
        f_valutions = open('./output/setting/IT橘子雷达公司估值.txt', 'w')

        print('----------- 开始保存公司信息 -----------')
        f_companies.write(data_companies)
        f_valutions.write(data_valutions)
        print('----------- 保存公司信息完毕 -----------')

def getname(data, companies, output):
	name_list = []
	for i in data.index:
		name_list.append(companies.loc[int(data.loc[i])]['投资机构名称'])
	data = pd.DataFrame({'name':name_list, 'output':output})
	data = data.sort_index(axis = 0,ascending = False,by = 'output') 
	data.reset_index()
	return data


if __name__ == '__main__':
    preparedata()

    data_companies = data_proc.DataCompany(predict=1)
    data_companies.import_data_itjuzi()
    data_companies.import_data_radar()
    data_companies.gen_variables()
    data_companies.gen_data()    # Output: data_companies.data
    print('■■■■■■■ 已读取 初创公司数据，维度：(%d, %d) ■■■■■■■'%(data_companies.data.shape[0], data_companies.data.shape[1]))

    data_investors = data_proc.DataInvestor()
    data_investors.import_data_invjuzi()
    data_investors.import_data_geshang()
    data_investors.gen_variables()

    data_investors.delete_small(data=data_investors.data_invjuzi['投资组合金额'])
    merged_data = pd.merge(left=data_investors.data_invjuzi_deleted_small.to_frame(),
                           right=data_investors.data_invjuzi['投资组合时间'].to_frame(), how='left', left_index=True,
                           right_index=True)
    data_investors.delete_no_recent(data=merged_data, column=1)
    data_investors.gen_model_data()    # Output: data_investors.model_data
    print('■■■■■■■ 已读取 投资机构数据，维度：(%d, %d) ■■■■■■■'%(data_investors.model_data.shape[0], data_investors.model_data.shape[1]))

    observation = check.Observation(data_companies.data,
                              data_investors.model_data,
                              data_companies.data_itjuzi,
                              data_investors.data_invjuzi,
                              train_size=TRAIN_SIZE,
                              batch_size_main=BATCH_SIZE)
    print('■■■■■■■ 预测数据已经准备 ■■■■■■■')

    data = observation.predict_data()
    model = load_model('%s.h5'%MODEL_NAME)
    print('■■■■■■■ 模型读取完成，计算预测数据，请等待 ■■■■■■■')

    output = model.predict(data[:-1])
    print('■■■■■■■ 预测数据计算完成 ■■■■■■■')

    output = output.tolist()

    name = data.iloc[:,-1:]
    
    data = getname(data, data_investors.data_invjuzi, output)
    data.to_csv('./output/output.csv')
    print('■■■■■■■ 数据输出完毕 ■■■■■■■')








