# -*- coding: utf-8 -*-
from random import randint

def paste_string(self, data, name, num_start, num_end):
    string = ''
    for i in range(num_start, num_end + 1):
        if data[name + str(i)] != '-':
            string = string + data[name + str(i)] + ' '
    item = string.split(sep=' ')
    # item = list(set(item))
    item.remove('')
    return item

def check_relation(self, list_company, list_investor):
    r = 0
    for i in list_company:
        for j in list_investor:
            if (i in j) | (j in i):
                r += 1
    return r

def check_percent(self, string_company, string_investor):
    list_investor = string_investor.split(sep=' ')
    percent = list_investor.count(string_company) / len(list_investor)
    return percent

def check_competitor(self, string_company, string_investor, data):
    list_investor = str(string_investor).split(sep=' ')
    count = 0
    check = 0
    for i in list_investor:
        if not data['二级分类'][self.data_itjuzi['项目名'] == i].empty:
            if (data['二级分类'][self.data_itjuzi['项目名'] == i] == string_company).bool():
                count += 1
    if count > 0:
        check = 1
    return [check, count]

class observation:
    """One observation for model, based on DataCompany, DataInvestor"""
    def __init__(self, data_companies, data_investors, data_itjuzi, data_invjuzi, train_size, batch_size_main):
        self.data_companies = data_companies
        self.data_investors = data_investors
        self.data_itjuzi = data_itjuzi
        self.data_invjuzi = data_invjuzi
        self.train_size = train_size
        self.batch_size_main = batch_size_main

    def check(self):
        self.relation_work = check_relation(paste_string(self.data_itjuzi.iloc[1], '工作经历', 1, 12),
                       paste_string(self.data_invjuzi.iloc[1], '投资人工作经历', 1, 60))
        self.relation_edu = check_relation(paste_string(self.data_itjuzi.iloc[1], '教育经历', 1, 12),
                       paste_string(self.data_invjuzi.iloc[1], '投资人教育经历', 1, 60))
        self.percent_class_first = check_percent(self.data_itjuzi['一级分类'].iloc[4],
                                                 self.data_invjuzi['投资组合行业'].iloc[1])
        self.percent_round = check_percent(self.data_itjuzi['项目名后轮次'].iloc[4],
                                           self.data_invjuzi['已投资轮次'].iloc[1])
        self.competitor = check_competitor(self.data_itjuzi['二级分类'].iloc[4],
                                           self.data_invjuzi['投资组合名称'].iloc[1],
                                           self.data_itjuzi)

    def gen_observation(self):
        while 1:
            # TODO: 变化很大 Sad
            random_company = [randint(0, self.train_size - 1) for i in range(self.batch_size_main)]
            random_invest = [randint(0, num_investor - 1) for i in range(batch_size_main)]
            yield (np.asarray([get_sample(random_company[i], random_invest[i])[0] for i in range(batch_size_main)]),
                   np.asarray([get_sample(random_company[i], random_invest[i])[1] for i in range(batch_size_main)]))
