# -*- coding: utf-8 -*-
from random import randint
import numpy as np
import data_proc

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
        self.investor_name_list = self.data_investors['投资机构名称']

    def gen_observation(self):
        # TODO: Multithread?
        def check(loc_company, loc_investor):
            """For random location (row), calculate variables of interaction."""
            # print('Check start ')
            self.relation_work = check_relation(paste_string(self.data_itjuzi.iloc[loc_company], '工作经历', 1, 12),
                                                paste_string(self.data_invjuzi.iloc[loc_investor], '投资人工作经历', 1,
                                                             60))
            # print('relation_work OK ' + str(self.relation_work))
            self.relation_edu = check_relation(paste_string(self.data_itjuzi.iloc[loc_company], '教育经历', 1, 12),
                                               paste_string(self.data_invjuzi.iloc[loc_investor], '投资人教育经历', 1, 60))
            # print('relation_edu OK ' + str(self.relation_edu))
            self.percent_class_first = check_percent(self.data_itjuzi['一级分类'].iloc[loc_company],
                                                     self.data_invjuzi['投资组合行业'].iloc[loc_investor])
            # print('percent_class_first OK ' + str(self.percent_class_first))
            self.percent_round = check_percent(self.data_itjuzi['项目名后轮次'].iloc[loc_company],
                                               self.data_invjuzi['已投资轮次'].iloc[loc_investor])
            # print('percent_round OK ' + str(self.percent_round))
            self.competitor = check_competitor(self.data_itjuzi['二级分类'].iloc[loc_company],
                                               self.data_invjuzi['投资组合名称'].iloc[loc_investor],
                                               self.data_itjuzi)
            # print('competitor OK ' + str(self.competitor))
            # print('Check finished')

        def get_sample(i_random_company, i_random_invest):
            """Concatenate company observation, investor observation, interaction variables and answer y (0 or 1).
            Maybe the observations should be autoencoded."""
            # TODO: Autoencoded?
            if self.investor_name_list.iloc[i_random_invest] in self.investor_now.iloc[i_random_company]:
                check(i_random_company, i_random_invest)
                sample = [np.concatenate([self.data_companies.iloc[i_random_company],
                                         self.data_investors.iloc[i_random_invest],
                                         np.array([self.relation_work, self.relation_edu, self.percent_class_first,
                                                   self.percent_round,self.competitor[0], self.competitor[1]])]),
                         np.array([1])]
                # print('Sample prepared (1)')
                return sample
            else:
                check(i_random_company, i_random_invest)
                sample = [np.concatenate([self.data_companies.iloc[i_random_company],
                                         self.data_investors.iloc[i_random_invest],
                                         np.array([self.relation_work, self.relation_edu, self.percent_class_first,
                                                   self.percent_round,self.competitor[0], self.competitor[1]])]),
                         np.array([0])]
                # print('Sample prepared (0)')
                return sample
        while 1:
            random_company = [randint(0, self.train_size - 1) for i in range(self.batch_size_main)]
            random_invest = [randint(0, len(self.data_invjuzi) - 1) for i in range(self.batch_size_main)]
            # print(random_invest)
            yield (np.asarray([get_sample(random_company[i], random_invest[i])[0] for i in range(self.batch_size_main)]),
                 np.asarray([get_sample(random_company[i], random_invest[i])[1] for i in range(self.batch_size_main)]))

if __name__ == '__main__':
    data_companies = data_proc.DataCompany()
    data_companies.import_data_itjuzi()
    data_companies.import_data_radar()
    data_companies.gen_variables()
    data_companies.gen_data()

    data_investors = data_proc.DataInvestor()
    data_investors.import_data_invjuzi()
    data_investors.import_data_geshang()
    data_investors.gen_variables()
    data_investors.gen_data()

    observation = Observation(data_companies.data,
                              data_investors.data,
                              data_companies.data_itjuzi,
                              data_investors.data_invjuzi,
                              train_size=3000,
                              batch_size_main=1000)
    observation.gen_observation()

# --------------------- End ----------------------