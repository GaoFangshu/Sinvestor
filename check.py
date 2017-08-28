# -*- coding: utf-8 -*-
from random import randint
import numpy as np
import data_proc
import pandas as pd
import multiprocessing

def paste_string(data, name, num_start, num_end):
    string = ''
    for i in range(num_start, num_end + 1):
        work = str(data[name + str(i)])
        if work != '-':
            string = string + work + ' '
    item = string.split(sep=' ')
    # item = list(set(item))
    item.remove('')
    return item

def check_relation(list_company, list_investor):
    r = 0
    for i in list_company:
        for j in list_investor:
            if (i in j) | (j in i):
                r += 1
    return r

def check_percent(string_company, string_investor):
    list_investor = str(string_investor).split(sep=' ')
    percent = list_investor.count(string_company) / len(list_investor)
    return percent

def check_competitor(string_company, string_investor, data):
    list_investor = str(string_investor).split(sep=' ')
    count = 0
    check = 0
    for i in list_investor:
        if not data['二级分类'][data['项目名'] == i].empty:
            if sum(data['二级分类'][data['项目名'] == i] == string_company) > 0:
                count += 1
    if count > 0:
        check = 1
    return [check, count]

class Observation:
    """One observation for model, based on DataCompany, DataInvestor"""
    def __init__(self, data_companies, data_investors, data_itjuzi, data_invjuzi, train_size, batch_size_main):
        """data_companies = DataCompany().data,
        data_investors = DataInvestor().data,
        data_itjuzi = DataCompany().data_itjuzi,
        data_invjuzi = DataInvestor().data_invjuzi,
        train_size = TRAIN_SIZE,
        batch_size_main = BATCH_SIZE_MAIN"""
        self.data_companies = data_companies
        self.data_investors = data_investors
        self.data_itjuzi = data_itjuzi
        self.data_invjuzi = data_invjuzi
        self.train_size = train_size
        self.batch_size_main = batch_size_main

        self.investor_now = data_proc.get_nth_investment(1, '投资机构', 15, self.data_itjuzi)
        self.investor_name_list = self.data_invjuzi['投资机构名称'].loc[self.data_investors.index]

    def gen_observation(self, save_flag=0, queue=0):
        # TODO: Multithread?
        def check(loc_company, loc_investor):
            """For random location (row), calculate variables of interaction."""
            # print('Check start ')
            self.relation_work = check_relation(paste_string(self.data_itjuzi.loc[loc_company], '工作经历', 1, 12),
                                                paste_string(self.data_invjuzi.loc[loc_investor], '投资人工作经历', 1,
                                                             60))
            # print('relation_work OK ' + str(self.relation_work))
            self.relation_edu = check_relation(paste_string(self.data_itjuzi.loc[loc_company], '教育经历', 1, 12),
                                               paste_string(self.data_invjuzi.loc[loc_investor], '投资人教育经历', 1, 60))
            # print('relation_edu OK ' + str(self.relation_edu))
            self.percent_class_first = check_percent(self.data_itjuzi['一级分类'].loc[loc_company],
                                                     self.data_invjuzi['投资组合行业'].loc[loc_investor])
            # print('percent_class_first OK ' + str(self.percent_class_first))
            self.percent_round = check_percent(self.data_itjuzi['项目名后轮次'].loc[loc_company],
                                               self.data_invjuzi['已投资轮次'].loc[loc_investor])
            # print('percent_round OK ' + str(self.percent_round))
            self.competitor = check_competitor(self.data_itjuzi['二级分类'].loc[loc_company],
                                               self.data_invjuzi['投资组合名称'].loc[loc_investor],
                                               self.data_itjuzi)
            # print('competitor OK ' + str(self.competitor))
            # print('Check finished')

        def get_sample(i_random_company, i_random_invest):    # based on index
            """Concatenate company observation, investor observation, interaction variables and answer y (0 or 1).
            Maybe the observations should be autoencoded."""
            # TODO: Autoencoded?
            if str(self.investor_name_list.loc[i_random_invest]) in str(self.investor_now.loc[i_random_company]):
                check(i_random_company, i_random_invest)
                sample = [self.data_companies.loc[i_random_company],
                          self.data_investors.loc[i_random_invest],
                          np.array([self.relation_work, self.relation_edu, self.percent_class_first,
                                   self.percent_round,self.competitor[0], self.competitor[1]]),
                         np.array([1])]
                # print('Sample prepared (1)')
                return sample
            else:
                check(i_random_company, i_random_invest)
                sample = [self.data_companies.loc[i_random_company],
                          self.data_investors.loc[i_random_invest],
                          np.array([self.relation_work, self.relation_edu, self.percent_class_first,
                                   self.percent_round,self.competitor[0], self.competitor[1]]),
                         np.array([0])]
                # print('Sample prepared (0)')
                return sample
            
        if save_flag == 1:
            while 1:
                random_company = [randint(0, self.train_size - 1) for i in range(self.batch_size_main)]
                index_random_company = self.data_companies.index[random_company]
                random_invest = [randint(0, len(self.data_investors) - 1) for i in range(self.batch_size_main)]
                index_random_invest = self.data_investors.index[random_invest]
                # print(random_invest)
                sample = [get_sample(index_random_company[i], index_random_invest[i]) for i in range(self.batch_size_main)]
                queue.put(pd.DataFrame([np.concatenate([i[0], i[1], i[2], i[3]]) for i in sample]))

        else:
            while 1:
                random_company = [randint(0, self.train_size - 1) for i in range(self.batch_size_main)]
                index_random_company = self.data_companies.index[random_company]
                random_invest = [randint(0, len(self.data_investors) - 1) for i in range(self.batch_size_main)]
                index_random_invest = self.data_investors.index[random_invest]
                # print(random_invest)
                sample = [get_sample(index_random_company[i], index_random_invest[i]) for i in range(self.batch_size_main)]
                yield ({'input_company':np.asarray([i[0] for i in sample]), 'input_investor':np.asarray([i[1] for i in sample]),
                        'input_cross':np.asarray([i[2] for i in sample])}, {'output_dense':np.asarray([i[3] for i in sample])})


def writeinworker(queue, path='./data/saved_data/'):
    while 1:
        if not queue.empty():
            data = queue.get(True)
            data.to_csv('%ssaved_data.csv'%path, index=0)
        else:
            continue
    


WORKER_NUM = 10



if __name__ == '__main__':
    data_companies = data_proc.DataCompany()
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

    observation = Observation(data_companies.data,
                              data_investors.model_data,
                              data_companies.data_itjuzi,
                              data_investors.data_invjuzi,
                              train_size=3000,
                              batch_size_main=30)
    print('■■■■■■■ 训练数据准备生成 ■■■■■■■')

    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()

    queue_data = manager.Queue()
    queue_writein = manager.Queue()

    print('■■■■■■■ 多进程准备完毕 ■■■■■■■')

    for worker in range(WORKER_NUM):
        pool.apply_async(observation.gen_observation, args=(1, queue_data))
    pool.close()

    print('■■■■■■■ 工作进程准备完毕 ■■■■■■■')

    writein = multiprocessing.Process(target=writeinworker, args=(queue_writein,))
    writein.start()

    print('■■■■■■■ 写入进程准备完毕 ■■■■■■■')
    print('■■■■■■■ 开始捕获生成数据 ■■■■■■■')

    savedata = pd.DataFrame()
    count = 0
    while 1:
        if not queue_data.empty():
            data_frame = queue_data.get(True)
            savedata = pd.concat([savedata, data_frame])
            count += 1
            print('-- %d rows get it'%(count * 30))
            if count % 100 == 0:
                queue_writein.put(savedata)
                print('---- %d rows writein'%(count * 30))
        else:
            continue
            
        

# --------------------- End ----------------------
