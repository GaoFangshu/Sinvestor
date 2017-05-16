# -*- coding: utf-8 -*-

import numpy as np
import re
import pandas as pd
from datetime import datetime

def unique_element(raw_column):
    ele_list = []
    ele = []
    for i in range(len(raw_column)-1):
        ind_string = np.array_str(raw_column[i+1])
        elements = re.split(r'\[\s\'|\'\]|,|\[\'', ind_string) # 可能不太完全
        ele_list.append(elements[1:len(elements)-1])
        ele.extend(elements[1:len(elements)-1])
        unique_ele = list(set(ele))
    return [ele_list, unique_ele]

def set_dummy(ele_list, unique_ele):
    dummy_array = np.zeros((len(ele_list), len(unique_ele)))
    for i in range(len(ele_list)): # for each investor
        for j in range(len(ele_list[i])): # for each industry of the investor
            dummy_array[i][unique_ele.index(ele_list[i][j])] = 1
    return dummy_array

def set_dummy_1c(ele_list, unique_ele):
    dummy_array = np.zeros((len(ele_list), len(unique_ele)))
    for i in range(len(ele_list)): # for each investor
        dummy_array[i][unique_ele.index(ele_list[i])] = 1
    return dummy_array

def set_dummy_series(data, title):
    title_unique_ele = data[title].unique().tolist()
    title_ele_list = data[title].values.tolist()
    dummy = set_dummy_1c(title_ele_list, title_unique_ele)
    print(dummy.shape)
    return dummy

def set_dummy_dataframe(data, title_list):
    title_data = pd.Series()
    for i in title_list:
        title_data = title_data.append(data[i])
    title_unique_ele = title_data.unique().tolist()
    title_ele_list = data[title_list].values.tolist()
    dummy = set_dummy(title_ele_list, title_unique_ele)  # (6595, 18)
    print(dummy.shape)
    return dummy

def replace_money(rawdata, title):
    # for k in range(len(rawdata)):
    #     if '无记录' in rawdata.loc[k, title]:
    #         rawdata.drop(k, inplace=True)
    rawdata.index = range(len(rawdata))
    for k in range(len(rawdata)):
        if '亿元及以上人民币' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(10000)
        elif '亿元及以上美元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(70000)
        elif '亿元及以上港元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(9000)
        elif '数十万人民币' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(50)
        elif '数十万美元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(350)
        elif '数百万人民币' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(500)
        elif '数百万美元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(3500)
        elif '数千万人民币' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(5000)
        elif '数千万美元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(35000)
        elif '数千万新台币' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(1000)
        elif '数千万港元' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(4500)
        elif '其他' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(0)
        elif '未透露' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(0)
        elif '无记录' in rawdata.loc[k, title]:
            rawdata.loc[k, title] = int(0)
        elif '万人民币' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('万人民币', '')
            rawdata.loc[k, title] = int(q)
        elif '亿人民币' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('亿人民币', '')
            q = int(float(q) * 10000)
            rawdata.loc[k, title] = int(q)
        elif '万美元' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('万美元', '')
            q = int(float(q) * 7)
            rawdata.loc[k, title] = int(q)
        elif '亿美元' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('亿美元', '')
            q = int(float(q) * 70000)
            rawdata.loc[k, title] = int(q)
        elif '万新台币' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('万新台币', '')
            q = int(float(q) * 0.2)
            rawdata.loc[k, title] = int(q)
        elif '亿港元' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('亿港元', '')
            q = int(float(q) * 9000)
            rawdata.loc[k, title] = int(q)
        elif '万英镑' in rawdata.loc[k, title]:
            q = rawdata.loc[k, title].replace('万英镑', '')
            q = int(float(q) * 90000)
            rawdata.loc[k, title] = int(q)

def del_whitespace(data, title):
    for k in range(len(data)):
        data.loc[k, title].replace(' ', '')

def invest_days(data, title_date_now, title_date_past):
    days = []
    for i in range(len(data)):
        if data[title_date_past][i] == '无记录':
            days.extend([0.0])
        else:
            timedelta = datetime.strptime(data[title_date_now][i], '%Y.%m.%d') - datetime.strptime(
                data[title_date_past][i], '%Y.%m.%d')
            days.extend([timedelta.total_seconds() / 3600 / 24 / 365])
    return days


# ------------------- Investors data -------------------

def get_invest_data():
    # IT橘子创投公司数据：
    #     id：主键
    #     机构简称：与格上理财数据匹配
    #     管理资本规模：解决币种问题、“其中包含”问题、资本规模币种分割问题
    #     单个投资项目规模：币种问题、换算问题
    #     投资领域：空格分割
    #     投资轮次：空格分割
    #     （项目方 - 资金方 交叉变量）投资组合时间、投资组合名称、投资组合行业、投资组合轮次、投资组合金额：空格分割、重新做表、币种问题、换算问题
    #     （项目方 - 资金方 交叉变量）投资人姓名60、投资人职位60、投资人简介60、投资人投资项目60、投资人工作经历60、投资人教育经历60：把60人以这五类汇总
    #     已投资行业、已投资各行业数量、已投资轮次、已投资各轮次数量：总表dummy然后每个投资机构填入统计
    #
    # 格上理财投资机构数据:
    #     id：？
    #     机构简称：与IT橘子数据匹配
    #     机构类型：查空值、转dummy
    #     资本类型：查空值、转dummy
    #     成立日期：计算距项目时间（是否筛选？）
    #     （项目方 - 资金方交叉变量）机构总部：查空值、转dummy
    #     管理规模：币种问题、换算问题
    #     基金个数：查空值
    #     投资数量：查空值
    #     退出数量：查空值、（退出/投资 比？）
    #     投资项目名称、投资项目行业分类、投资项目投资阶段、投资项目投资资金、投资项目投资时间：行业转转dummy，各变量统计
    #     退出项目企业名称、退出项目行业分类、退出项目退出方式、退出项目账面回报、退出项目推出时间：行业转转dummy，各变量统计

    invest_list = pd.read_csv('./data/IT橘子创投公司数据.txt', sep='\t', encoding= 'gbk')

    count = 0


    raw_data_invest = np.asarray(invest_list).reshape(count,int(len(invest_list)/count))
    raw_data_invest.shape
    title_invest = raw_data_invest[0]
    data_invest = raw_data_invest[:,[a1 or a2 or a3 or a4 for a1,a2,a3,a4 in zip(title_invest == '\ufeffid_vc',
                                                 title_invest == 'name_firm',
                                                 title_invest == 'industry_vc',
                                                 title_invest == 'round_vc')]] # choose columns
    invindustry = raw_data_invest[:,title_invest == 'industry_vc'] # choose columns
    invround = raw_data_invest[:,title_invest == 'round_vc']

    invindustry_elements = unique_element(invindustry)
    dummy_invindustry = set_dummy(invindustry_elements[0], invindustry_elements[1])

    invround_elements = unique_element(invround)
    dummy_invround = set_dummy(invround_elements[0], invround_elements[1])

    data_invest_new = np.concatenate([data_invest[1:, [0, 1]], dummy_invindustry, dummy_invround], axis = 1)[:,1:]
    data_invest_new.shape # 6590(2592 unique)
    return data_invest_new

# ------------------- Companies data -------------------
def get_company_data():
    # IT橘子创业公司信息：
    #     id：主键，与雷达合并？
    #     项目名：
    #     项目名后轮次：转dummy
    #     一级分类：转dummy
    #     二级分类：转dummy （分类有没有必要做交叉变量？）
    #     （项目方 - 资金方交叉变量）一级地区：转dummy、和投资机构匹配
    #     （项目方 - 资金方交叉变量）二级地区：转dummy
    #     tag：转dummy
    #     公司全称：
    #     成立时间：（公司成立时间非项目成立时间），计算距项目时间
    #     公司规模：获得数据(人)
    #     经营状态：转dummy
    #     获投时间15、获投轮次15、获投金额15、投资机构15：按照原来的来
    #     （项目方 - 资金方交叉变量）成员姓名12、成员职务12、人物简介12、创业经历12、工作经历12、教育经历12
    #     注册资金：币种问题、换算问题
    #     股东信息：获得数据(人)
    #     企业类型：转dummy
    #     注册时间：（公司成立时间非项目成立时间），计算距项目时间
    #     股东信息1、股东信息2：
    #
    # IT橘子雷达公司估值：
    #     id：主键，与IT橘子项目还是公司合并？
    #     时间：时间换算
    #     公司规模：获得数据(人)，"不明确"
    #     估值：币种问题、换算问题


    rawdata = pd.read_excel('raw_data.xls', encoding='gbk', parse_cols='A,C:F,H,L,S:AD,AH:BJ')
    # delete whitespace
    # del_whitespace(rawdata, '投资人1,1')

    rawdata = rawdata.drop_duplicates(['项目key值'])
    rawdata.index = range(len(rawdata))

    # raise amount
    replace_money(rawdata, '融资额度2')
    replace_money(rawdata, '融资额度3')
    replace_money(rawdata, '融资额度4')
    money_total = (rawdata['融资额度2'] + rawdata['融资额度3'] + rawdata['融资额度4']).values # .reshape(rawdata.shape[0], 1)
    money_total = money_total / money_total.max()

    # round of raise
    dummy_round = set_dummy_dataframe(rawdata, ['融资轮次1','融资轮次2','融资轮次3','融资轮次4']) # (6595, 18)

    # industry dummies
    dummy_industry1 = set_dummy_series(rawdata, '行业标签') # (6595, 17)
    dummy_industry2 = set_dummy_series(rawdata, '细分标签') # (6595, 156)
    dummy_industry3 = set_dummy_dataframe(rawdata, ['橘子标签1', '橘子标签2', '橘子标签3', '橘子标签4', '橘子标签5',
                                                    '橘子标签6', '橘子标签7', '橘子标签8', '橘子标签9', '橘子标签10']) # (6595, 824)
    dummy_type = set_dummy_series(rawdata,'公司类型') # (6595, 82)

    # investor dummies
    dummy_investors = set_dummy_dataframe(rawdata, ['投资人2,1', '投资人2,2', '投资人2,3', '投资人2,4',
                                                    '投资人3,1', '投资人3,2', '投资人3,3', '投资人3,4',
                                                    '投资人4,1', '投资人4,2', '投资人4,3', '投资人4,4']) # (6595, 701)/(6595, 1456)

    # days from last investment
    days = np.array(invest_days(rawdata, '融资时间1', '融资时间2'))
    days = days / days.max()


    companies_data = np.concatenate([rawdata[['项目key值','项目名称','投资人1,1', '投资人1,2', '投资人1,3', '投资人1,4']].values,
                                     money_total.reshape(len(rawdata), 1), dummy_round,
                                     dummy_industry1, dummy_industry2, dummy_industry3, dummy_type, dummy_investors,
                                     days.reshape(len(rawdata), 1)], axis=1)

    return companies_data