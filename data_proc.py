# -*- coding: utf-8 -*-
import datetime
import numpy as np
import pandas as pd
import re


"""Files structure:
    - Sinvestors
        - data
            - IT橘子创业公司信息.txt
            - IT橘子创投公司数据.txt
            - IT橘子雷达公司估值.txt
            - 格上理财投资机构数据.txt
        - data_proc.py
        - main_model.py
        - README.md
"""

def unique_element(raw_column):
# split string to elements and get dummy variables, sep = \s
    ele_list = []
    ele = []
    for i in range(len(raw_column)):
        elements = re.split(r'\s', raw_column[i])
        ele_list.append(elements)
        ele.extend(elements)
        unique_ele = list(set(ele))
    return [ele_list, unique_ele]


def set_dummy(column, name, sep = r'\s', delete = True, delete_name = '-'):
# split string to elements and get dummy variables, sep = \s
    s = column.apply(lambda x: re.split(sep, x))
    if delete:
        return pd.get_dummies(s.apply(pd.Series).stack(), prefix='dummy_' + name).sum(level=0)\
            .drop('dummy_' + name + '_' + delete_name, axis = 1)
    else:
        return pd.get_dummies(s.apply(pd.Series).stack(), prefix='dummy_' + name).sum(level=0)    # http://stackoverflow.com/questions/29034928/pandas-convert-a-column-of-list-to-dummies
        # another but slower way:
        # column.apply(f_split).str.join(sep='*').str.get_dummies(sep='*')    # http://stackoverflow.com/questions/18889588/create-dummies-from-column-with-multiple-values-in-pandas


def get_nth_investment(n, col_name, num, data):
# get data of nth investment, n = 1 for latest round
    col = []
    for i in range(num):
        col_n = col_name + str(i + 1)
        col.append(col_n)
    nb_rounds = (data[col] != '-').sum(axis=1)
    s1 = nb_rounds.apply(lambda x: col[x - n])    # latest round
    s2 = s1
    for j in range(len(s1)):
        s2.iloc[j] = data[s1.iloc[j]].iloc[j]
    s2 = s2.astype(str)
    return s2


def correct_date(column):
# get correct date format
    s = column.apply(lambda x: x[0:10])
    return s


def invest_days(column_date_now, column_date_past):
# calculate time delta
    # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
    column_date_past[(column_date_past == '-') | (column_date_past == '0000-00-00')] = \
        column_date_now[(column_date_past == '-') | (column_date_past == '0000-00-00')]
    column_date_past = pd.to_datetime(correct_date(column_date_past))
    column_date_now = pd.to_datetime(correct_date(column_date_now))
    return column_date_now - column_date_past


def replace_money(x):
    if '亿元及以上人民币' in x:
        q = int(10000)
    elif '亿元及以上美元' in x:
        q = int(70000)
    elif '亿元及以上港元' in x:
        q = int(9000)
    elif '数十万人民币' in x:
        q = int(50)
    elif '数十万美元' in x:
        q = int(350)
    elif '数百万人民币' in x:
        q = int(500)
    elif '数百万美元' in x:
        q = int(3500)
    elif '数千万人民币' in x:
        q = int(5000)
    elif '数千万美元' in x:
        q = int(35000)
    elif '数千万新台币' in x:
        q = int(1000)
    elif '数千万港元' in x:
        q = int(4500)
    elif '其他' in x:
        q = int(0)
    elif '未透露' in x:
        q = int(0)
    elif '无记录' in x:
        q = int(0)
    elif '-' in x:
        q = int(0)
    elif '万人民币' in x:
        q = x.replace('万人民币', '')
        q = int(q)
    elif '亿元人民币' in x:
        q = x.replace('亿元人民币', '')
        q = int(float(q) * 10000)
        q = int(q)
    elif '亿人民币' in x:
        q = x.replace('亿人民币', '')
        q = int(float(q) * 10000)
        q = int(q)
    elif '万美元' in x:
        q = x.replace('万美元', '')
        q = int(float(q) * 7)
        q = int(q)
    elif '亿美元' in x:
        q = x.replace('亿美元', '')
        q = int(float(q) * 70000)
        q = int(q)
    elif '亿元美元' in x:
        q = x.replace('亿元美元', '')
        q = int(float(q) * 70000)
        q = int(q)
    elif '万新台币' in x:
        q = x.replace('万新台币', '')
        q = int(float(q) * 0.2)
        q = int(q)
    elif '亿新台币' in x:
        q = x.replace('亿新台币', '')
        q = int(float(q) * 2000)
        q = int(q)
    elif '亿港元' in x:
        q = x.replace('亿港元', '')
        q = int(float(q) * 9000)
        q = int(q)
    elif '亿元港元' in x:
        q = x.replace('亿元港元', '')
        q = int(float(q) * 9000)
        q = int(q)
    elif '万港元' in x:
        q = x.replace('万港元', '')
        q = int(float(q) * 0.9)
        q = int(q)
    elif '万英镑' in x:
        q = x.replace('万英镑', '')
        q = int(float(q) * 9)
        q = int(q)
    elif '亿英镑' in x:
        q = x.replace('亿英镑', '')
        q = int(float(q) * 90000)
        q = int(q)
    elif '万欧元' in x:
        q = x.replace('万欧元', '')
        q = int(float(q) * 7.7)
        q = int(q)
    elif '亿欧元' in x:
        q = x.replace('亿欧元', '')
        q = int(float(q) * 77000)
        q = int(q)
    elif '亿卢比' in x:
        q = x.replace('亿卢比', '')
        q = int(float(q) * 1068)
        q = int(q)
    elif '万卢比' in x:
        q = x.replace('万卢比', '')
        q = int(float(q) * 0.1068)
        q = int(q)
    elif '亿日元' in x:
        q = x.replace('亿日元', '')
        q = int(float(q) * 619)
        q = int(q)
    elif '亿元日元' in x:
        q = x.replace('亿元日元', '')
        q = int(float(q) * 619)
        q = int(q)
    elif '万日元' in x:
        q = x.replace('万日元', '')
        q = int(float(q) * 0.0619)
        q = int(q)
    elif x == '万':
        q = 0
    else:
        return x
    return q

# check if a is in b, and make a dummy column
# def dummy_check(a, b):


"""Companies data
IT橘子创业公司信息：
    id：主键，与雷达合并？
    项目名：
    项目名后轮次：转dummy
    一级分类：转dummy
    二级分类：转dummy  TODO: （分类有没有必要做交叉变量？）
    TODO: （项目方 - 资金方交叉变量）一级地区：转dummy、和投资机构匹配
    TODO: （项目方 - 资金方交叉变量）二级地区：转dummy
    tag：转dummy
    公司全称：
    TODO: 成立时间：（公司成立时间非项目成立时间），计算距项目时间  bug如：2009.70
    公司规模：获得数据(人)，转dummy
    TODO: 经营状态：转dummy  全部当作“运营中”，不处理
    获投时间15、获投轮次15、获投金额15、投资机构15：计算距上次投资时间，用本次获投轮次转dummy，用本次获投金额转金额，其余交叉时再算
    TODO:是否将金额不明确的删掉
    TODO:（项目方 - 资金方交叉变量）成员姓名12、成员职务12、人物简介12、创业经历12、工作经历12、教育经历12
    注册资金：币种问题、换算问题
    股东信息：获得数据(人) TODO：空值太多，没有放
    企业类型：转dummy
    注册时间：（公司成立时间非项目成立时间），计算距项目时间
    股东信息1、股东信息2：TODO：空值太多，舍去

IT橘子雷达公司估值：
    id：主键，与IT橘子项目还是公司合并？
    时间：时间换算
    公司规模：获得数据(人)，"不明确"
    估值：币种问题、换算问题
"""
# def get_company_data():
rawdata_itjuzi = pd.read_csv('./data/IT橘子创业公司信息.txt', sep='\t', encoding='gbk')    # 54858 rows x 150 columns
data_itjuzi = rawdata_itjuzi[rawdata_itjuzi['投资机构1'] != '-']    # 19836 rows x 150 columns
rawdata_leida = pd.read_csv('./data/IT橘子雷达公司估值.txt', sep='\t', encoding='gbk')    # 54975 rows x 4 columns

# generate variables
dummy_round = pd.get_dummies(data_itjuzi['项目名后轮次'], prefix='dummy_项目名后轮次')\
    .drop('dummy_项目名后轮次_获投状态：不明确', axis = 1)    # 19836 rows x 17 columns
dummy_class_first = pd.get_dummies(data_itjuzi['一级分类'], prefix='dummy_一级分类')    # 19836 rows x 18 columns
dummy_class_second = pd.get_dummies(data_itjuzi['二级分类'], prefix='dummy_二级分类')\
    .drop('dummy_二级分类_-', axis = 1)    # 19836 rows x 181 columns
dummy_tag = set_dummy(data_itjuzi['tag'], 'tag')    # 19836 rows x 1049 columns
dummy_numemp = pd.get_dummies(data_itjuzi['公司规模'], prefix='dummy_公司规模')\
    .drop(['dummy_公司规模_暂未收录', 'dummy_公司规模_不明确'], axis = 1)    # 19836 rows x 11 columns
dummy_invested = (data_itjuzi['获投时间2'] != '-').astype(int)    # whether have been invested before, 1 for yes
year_from_inv = invest_days(get_nth_investment(1, '获投时间', 15, data_itjuzi),
                            get_nth_investment(2, '获投时间', 15, data_itjuzi)) / np.timedelta64(365, 'D')    # years from last investment
get_nth_investment(1, '获投金额', 15, data_itjuzi).value_counts()
invested_amount = get_nth_investment(1, '获投金额', 15, data_itjuzi).apply(replace_money)
dummy_round =  pd.get_dummies(data_itjuzi['获投轮次2'], prefix='dummy_获投轮次2')\
    .drop('dummy_获投轮次2_不明确', axis = 1)    # 19836 rows x 17 columns
regi_money = data_itjuzi['注册资金'].apply(replace_money)
dummy_company_type = pd.get_dummies(data_itjuzi['企业类型'], prefix='dummy_企业类型')\
    .drop(['dummy_企业类型_-', 'dummy_企业类型_未公开'], axis=1)    # 19836 rows x 84 columns
year_from_inv = invest_days(get_nth_investment(1, '获投时间', 15, data_itjuzi),
                            (data_itjuzi['注册时间'] + '')) / np.timedelta64(365, 'D')    # years from company's establishment


"""Investors data
IT橘子创投公司数据：
    id：主键
    机构简称：与格上理财数据匹配
    管理资本规模：解决币种问题、“其中包含”问题、资本规模币种分割问题
    单个投资项目规模：币种问题、换算问题
    投资领域：空格分割
    投资轮次：空格分割
    （项目方 - 资金方 交叉变量）投资组合时间、投资组合名称、投资组合行业、投资组合轮次、投资组合金额：空格分割、重新做表、币种问题、换算问题
    （项目方 - 资金方 交叉变量）投资人姓名60、投资人职位60、投资人简介60、投资人投资项目60、投资人工作经历60、投资人教育经历60：把60人以这五类汇总
    已投资行业、已投资各行业数量、已投资轮次、已投资各轮次数量：总表dummy然后每个投资机构填入统计

格上理财投资机构数据:
    id：？
    机构简称：与IT橘子数据匹配
    机构类型：查空值、转dummy
    资本类型：查空值、转dummy
    成立日期：计算距项目时间（是否筛选？）
    （项目方 - 资金方交叉变量）机构总部：查空值、转dummy
    管理规模：币种问题、换算问题
    基金个数：查空值
    投资数量：查空值
    退出数量：查空值、（退出/投资 比？）
    投资项目名称、投资项目行业分类、投资项目投资阶段、投资项目投资资金、投资项目投资时间：行业转转dummy，各变量统计
    退出项目企业名称、退出项目行业分类、退出项目退出方式、退出项目账面回报、退出项目推出时间：行业转转dummy，各变量统计
"""

rawdata_invjuzi = pd.read_csv('./data/IT橘子创投公司数据.txt', sep='\t', encoding='gbk')    # 6607 rows x 375 columns
rawdata_geshang = pd.read_csv('./data/格上理财投资机构数据.txt', sep='\t', encoding='gbk')    # 10106 rows x 20 columns