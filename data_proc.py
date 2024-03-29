# -*- coding: utf-8 -*-

"""
Files structure:

- Sinvestors
    - main.py
    - data
        - IT橘子创业公司信息.txt
        - IT橘子创投公司数据.txt
        - IT橘子雷达公司估值.txt
        - 格上理财投资机构数据.txt
        - itjuzi_geshang_finished.txt
    - data_proc.py
    - main_model.py
    - README.md
"""

import numpy as np
import pandas as pd
import re
import datetime


# Functions used in DataCompany

def set_dummy(column, name, sep=r'\s', delete=True, delete_name='-'):
    """Split string to elements and get dummy variables, sep = \s."""
    s = column.apply(lambda x: re.split(sep, x))
    if delete:
        return pd.get_dummies(s.apply(pd.Series).stack(), prefix='dummy_' + name).sum(level=0) \
            .drop('dummy_' + name + '_' + delete_name, axis=1)
    else:
        return pd.get_dummies(s.apply(pd.Series).stack(), prefix='dummy_' + name).sum(
            level=0)  # http://stackoverflow.com/questions/29034928/pandas-convert-a-column-of-list-to-dummies
        # another but slower way:
        # column.apply(f_split).str.join(sep='*').str.get_dummies(sep='*')    # http://stackoverflow.com/questions/18889588/create-dummies-from-column-with-multiple-values-in-pandas


def correct_date(column):
    """Get correct date format."""
    s = column.apply(lambda x: x[0:10])
    return s


def invest_days(column_date_now, column_date_past):
    """Calculate time delta."""
    # https://stackoverflow.com/questions/36921951/truth-value-of-a-series-is-ambiguous-use-a-empty-a-bool-a-item-a-any-o
    column_date_past[(column_date_past == '-') | (column_date_past == '0000-00-00')] = \
        column_date_now[(column_date_past == '-') | (column_date_past == '0000-00-00')]
    column_date_past = pd.to_datetime(correct_date(column_date_past))
    column_date_now = pd.to_datetime(correct_date(column_date_now))
    return column_date_now - column_date_past


def get_nth_investment(n, col_name, num, data):
    """Get data of nth investment, n = 1 for latest round."""
    col = []
    for i in range(num):
        col_n = col_name + str(i + 1)
        col.append(col_n)
    nb_rounds = (data[col] != '-').sum(axis=1)
    s1 = nb_rounds.apply(lambda x: col[x - n])  # latest round
    s2 = s1
    for j in range(len(s1)):
        s2.iloc[j] = data[s1.iloc[j]].iloc[j]
    s2 = s2.astype(str)
    return s2


def replace_money(x):
    """Replace currency and amount of money."""
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
    elif '数百万英镑' in x:
        q = int(4500)
    elif '数千万人民币' in x:
        q = int(5000)
    elif '数千万美元' in x:
        q = int(35000)
    elif '数千万新台币' in x:
        q = int(1000)
    elif '数千万港元' in x:
        q = int(4500)
    elif '数千万欧元' in x:
        q = int(38500)
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
    elif '亿人民币' in x:
        q = x.replace('亿人民币', '')
        q = int(float(q) * 10000)
    elif '万美元' in x:
        q = x.replace('万美元', '')
        q = int(float(q) * 7)
    elif '亿美元' in x:
        q = x.replace('亿美元', '')
        q = int(float(q) * 70000)
    elif '亿元美元' in x:
        q = x.replace('亿元美元', '')
        q = int(float(q) * 70000)
    elif '万新台币' in x:
        q = x.replace('万新台币', '')
        q = int(float(q) * 0.2)
    elif '亿新台币' in x:
        q = x.replace('亿新台币', '')
        q = int(float(q) * 2000)
    elif '亿港元' in x:
        q = x.replace('亿港元', '')
        q = int(float(q) * 9000)
    elif '亿元港元' in x:
        q = x.replace('亿元港元', '')
        q = int(float(q) * 9000)
    elif '万港元' in x:
        q = x.replace('万港元', '')
        q = int(float(q) * 0.9)
    elif '万英镑' in x:
        q = x.replace('万英镑', '')
        q = int(float(q) * 9)
    elif '亿英镑' in x:
        q = x.replace('亿英镑', '')
        q = int(float(q) * 90000)
    elif '万欧元' in x:
        q = x.replace('万欧元', '')
        q = int(float(q) * 7.7)
    elif '亿欧元' in x:
        q = x.replace('亿欧元', '')
        q = int(float(q) * 77000)
    elif '亿卢比' in x:
        q = x.replace('亿卢比', '')
        q = int(float(q) * 1068)
    elif '万卢比' in x:
        q = x.replace('万卢比', '')
        q = int(float(q) * 0.1068)
    elif '亿日元' in x:
        q = x.replace('亿日元', '')
        q = int(float(q) * 619)
    elif '亿元日元' in x:
        q = x.replace('亿元日元', '')
        q = int(float(q) * 619)
    elif '万日元' in x:
        q = x.replace('万日元', '')
        q = int(float(q) * 0.0619)
    elif '亿新加坡元' in x:
        q = x.replace('亿新加坡元', '')
        q = int(float(q) * 49577)
    elif '亿加元' in x:
        q = x.replace('亿加元', '')
        q = int(float(q) * 50922)
    elif x == '万':
        q = 0
    else:
        return 0
    return q


def get_deltaday(string_date):
    """Calculate delta time (day)."""
    if '年' in string_date:
        year = int(re.search(r'(\d+)年', string_date).group(1))
    else:
        year = 0
    if '个月' in string_date:
        month = int(re.search(r'(\d+)个月', string_date).group(1))
    else:
        month = 0
    delta = year * 365 + month * 30.4
    return delta


# Functions used in DataInvestor

def get_invamount(string_amount, num):
    var_total_amount = 0
    var_CNY_amount = 0
    var_USD_amount = 0
    if '其中包含' in string_amount:
        total_amount = re.search(r'(.*)其中包含(.*)', string_amount).group(1)
        contains = re.findall(r'\d+\.*\d*\D+', re.search(r'(.*)其中包含(.*)', string_amount).group(2))
        if not contains:
            contains = [total_amount]
            if '亿人民币' in contains[0]:
                var_CNY_amount = int(float(contains[0].replace('亿人民币', '')) * 10000)
                var_total_amount = var_CNY_amount
            elif '亿美元' in contains[0]:
                var_USD_amount = int(float(contains[0].replace('亿美元', '')) * 70000)
                var_total_amount = var_USD_amount
        else:
            for i in contains:
                if '亿人民币' in i:
                    var_CNY_amount = int(float(i.replace('亿人民币', '')) * 10000)
                    var_total_amount = var_total_amount + var_CNY_amount
                elif '亿美元' in i:
                    var_USD_amount = int(float(i.replace('亿美元', '')) * 70000)
                    var_total_amount = var_total_amount + var_USD_amount
    return [var_total_amount, var_CNY_amount, var_USD_amount][num]


def get_minmax_amount(string_amount, num):
    var_min_amount = 0
    var_max_amount = 0
    if '—' in string_amount:
        if '人民币' in string_amount:
            var_min_amount = int(re.search(r'\d+', re.search(r'(.*)—(.*)', string_amount).group(1)).group())
            var_max_amount = int(re.search(r'\d+', re.search(r'(.*)—(.*)', string_amount).group(2)).group())
        elif '美元' in string_amount:
            var_min_amount = int(re.search(r'\d+', re.search(r'(.*)—(.*)', string_amount).group(1)).group()) * 7
            var_max_amount = int(re.search(r'\d+', re.search(r'(.*)—(.*)', string_amount).group(2)).group()) * 7
    return [var_min_amount, var_max_amount][num]


def get_percent_var(item, item_name, item_amount, item_set):
    def get_percent(item, check, item_name, item_amount):
        if check in item[item_name]:
            percent = int(item[item_amount][item[item_name].index(check)]) / sum([int(x) for x in item[item_amount]])
        else:
            percent = 0
        return percent

    n = True
    for i in item_set:
        if n:
            percent_merged = item.apply(get_percent, args=(i, item_name, item_amount), axis=1)
            n = False
        else:
            percent_merged = pd.concat(
                [percent_merged, item.apply(get_percent, args=(i, item_name, item_amount), axis=1)]
                , axis=1)
    percent_merged.columns = ['percent_' + x for x in item_set]
    return percent_merged


def count_percent(name, data):
    count = pd.get_dummies(data[name]
                           .str.split(r'\s', expand=True)
                           .stack(),
                           prefix='percent_' + name).groupby(level='id').sum()
    # https: // stackoverflow.com / questions / 39459321 / have - pandas - column - containing - lists - how - to - pivot - unique - list - elements - to - column
    percent = count.div(count.sum(axis=1), axis=0) \
        .drop(['percent_' + name + '_-', 'percent_' + name + '_----'], axis=1)
    return percent


class DataCompany:
    """Data of companies invested.

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
        公司规模：获得数据(人)，"不明确"太多，舍去
        估值：币种问题、换算问题"""

    def __init__(self, predict=0):
        """Initialize companies data to be used in model."""
        self.data = pd.DataFrame()
        self.predict = predict

    def import_data_itjuzi(self, dir='./data/IT橘子创业公司信息.txt'):
        """Import Itjuzi rawdata, dir is directory of data file."""
        if self.predict==1:
            dir='./output/setting/IT橘子创业公司信息.txt'
        self.data_itjuzi = pd.read_csv(dir, sep='\t', encoding='gbk')  # 54858 rows x 150 columns
        self.data_itjuzi = self.data_itjuzi[self.data_itjuzi['投资机构1'] != '-']  # 19836 rows x 150 columns
        self.data_itjuzi = self.data_itjuzi.set_index('id')  # 19836 rows x 149 columns 此时id不连续

    def import_data_radar(self, dir='./data/IT橘子雷达公司估值.txt'):
        """Import Itjuzi radar rawdata, dir is directory of data file."""
        if self.predict==1:
            dir='./output/setting/IT橘子雷达公司估值.txt'
        self.data_radar = pd.read_csv(dir, sep='\t', encoding='gbk')  # 54975 rows x 4 columns
        self.data_radar = self.data_radar.set_index('id')  # 54975 rows x 3 columns 变量命名与data_itjuzi一致，此时id不连续

    def gen_variables(self):
        """Generate variables in data."""

        # generate variables in IT橘子创业公司信息.txt
        # generate current round dummy
        self.dummy_round = pd.get_dummies(self.data_itjuzi['项目名后轮次'], prefix='dummy_项目名后轮次') \
            .drop('dummy_项目名后轮次_获投状态：不明确', axis=1)  # 19836 rows x 17 columns 对轮次的定义有待精确化，如按融资重新定义
        # generate industry dummy
        self.dummy_class_first = pd.get_dummies(self.data_itjuzi['一级分类'],
                                                prefix='dummy_一级分类')  # 19836 rows x 18 columns
        self.dummy_class_second = pd.get_dummies(self.data_itjuzi['二级分类'], prefix='dummy_二级分类') \
            .drop('dummy_二级分类_-', axis=1)  # 19836 rows x 181 columns
        self.dummy_tag = set_dummy(self.data_itjuzi['tag'], 'tag')  # 19836 rows x 1049 columns 感觉这个函数速度有点慢，但是暂时不知道怎么改
        # generate scale dummy
        self.dummy_numemp = pd.get_dummies(self.data_itjuzi['公司规模'], prefix='dummy_公司规模') \
            .drop(['dummy_公司规模_暂未收录', 'dummy_公司规模_不明确'], axis=1)  # 19836 rows x 11 columns
        # generate whether-invested-before dummy
        self.dummy_invested = (self.data_itjuzi['获投时间2'] != '-').astype(
            int)  # whether have been invested before, 1 for yes
        # generate years from last investment
        self.year_from_inv = invest_days(get_nth_investment(1, '获投时间', 15, self.data_itjuzi),
                                         get_nth_investment(2, '获投时间', 15, self.data_itjuzi)) / np.timedelta64(365, 'D')
        # generate price for the current round
        self.invested_amount = get_nth_investment(1, '获投金额', 15, self.data_itjuzi).apply(replace_money)
        # generate last round dummy
        self.dummy_round = pd.get_dummies(self.data_itjuzi['获投轮次2'], prefix='dummy_获投轮次2') \
            .drop('dummy_获投轮次2_不明确', axis=1)  # 19836 rows x 17 columns
        # generate register money
        self.regi_money = self.data_itjuzi['注册资金'].apply(replace_money)
        self.dummy_company_type = pd.get_dummies(self.data_itjuzi['企业类型'], prefix='dummy_企业类型') \
            .drop(['dummy_企业类型_-', 'dummy_企业类型_未公开'], axis=1)  # 19836 rows x 84 columns
        self.year_from_establish = invest_days(get_nth_investment(1, '获投时间', 15, self.data_itjuzi),
                                               (self.data_itjuzi['注册时间'] + '')) / np.timedelta64(365,
                                                                                                 'D')  # years from company's establishment

        # generate variables in IT橘子雷达公司估值.txt
        self.radar_deltaday = self.data_radar['时间'].apply(get_deltaday)
        self.valuation = self.data_radar['估值'].apply(replace_money)  # 0: 53278/54975

    def gen_data(self, normalize=True):
        """Merge variables and merge companies data"""

        if normalize:
            self.year_from_inv = (self.year_from_inv - np.min(self.year_from_inv)) / \
                                (np.max(self.year_from_inv) - np.min(self.year_from_inv)) - 0.5
            self.invested_amount = (self.invested_amount - np.min(self.invested_amount)) / \
                                 (np.max(self.invested_amount) - np.min(self.invested_amount)) - 0.5
            self.regi_money = (self.regi_money - np.min(self.regi_money)) / \
                                 (np.max(self.regi_money) - np.min(self.regi_money)) - 0.5
            self.year_from_establish = (self.year_from_establish - np.min(self.year_from_establish)) / \
                                 (np.max(self.year_from_establish) - np.min(self.year_from_establish)) - 0.5
            self.radar_deltaday = (self.radar_deltaday - np.min(self.radar_deltaday)) / \
                                       (np.max(self.radar_deltaday) - np.min(self.radar_deltaday)) - 0.5
            self.valuation = (self.valuation - np.min(self.valuation)) / \
                                  (np.max(self.valuation) - np.min(self.valuation)) - 0.5

        self.variables_itjuzi = pd.concat(
            [self.dummy_round, self.dummy_class_first, self.dummy_class_second, self.dummy_tag, self.dummy_numemp,
             self.dummy_invested, self.year_from_inv, self.invested_amount, self.dummy_round, self.regi_money,
             self.dummy_company_type, self.year_from_establish],
            axis=1)  # 19836 rows x 1382 columns
        self.variables_radar = pd.concat([self.radar_deltaday, self.valuation], axis=1)  # 54975 rows x 2 columns
        self.data = pd.concat([self.variables_itjuzi, self.variables_radar], axis=1,
                              join_axes=[self.variables_itjuzi.index])  # 19836 rows x 1384 columns


class DataInvestor:
    """Data of investors.

    IT橘子创投公司数据：
        id：主键
        机构简称：与格上理财数据匹配
        管理资本规模：解决币种问题、“其中包含”问题、资本规模币种分割问题
        单个项目投资规模：币种问题、换算问题
        投资领域：空格分割
        投资轮次：空格分割
        （项目方 - 资金方 交叉变量）投资组合时间（没用到）、投资组合名称、投资组合行业、投资组合轮次、投资组合金额：空格分割、重新做表、币种问题、换算问题
        （项目方 - 资金方 交叉变量）投资人姓名60、投资人职位60、投资人简介60、投资人投资项目60、投资人工作经历60、投资人教育经历60：把60人以这五类汇总
        已投资行业、已投资各行业数量、已投资轮次、已投资各轮次数量：总表dummy然后每个投资机构填入统计

    格上理财投资机构数据:
        id：？
        机构简称：与IT橘子数据匹配
        机构类型：查空值、转dummy
        资本类型：查空值、转dummy
        成立日期：计算距项目时间（是否筛选？） TODO:交叉变量
        （项目方 - 资金方交叉变量）机构总部：查空值、转dummy，  TODO:合并it橘子一二级地区，删格上理财多余字
        管理规模：币种问题、换算问题
        基金个数：查空值
        投资数量：查空值
        退出数量：查空值、（退出/投资 比？）
        投资项目名称、投资项目行业分类、投资项目投资阶段、投资项目投资资金、投资项目投资时间：行业转dummy，各变量统计
            TODO:投资项目投资资金(暂时没有币种分类)、投资项目投资时间
        退出项目企业名称、退出项目行业分类、退出项目退出方式、退出项目账面回报、退出项目推出时间：行业转dummy，各变量统计
            TODO:退出项目账面回报('----'和'-'记为0)、退出项目推出时间"""

    def __init__(self):
        """Initialize investors data to be used in model."""
        self.data = pd.DataFrame()

    def import_data_invjuzi(self, dir='./data/IT橘子创投公司数据.txt'):
        """Import Itjuzi investors rawdata, dir is directory of data file."""
        self.data_invjuzi = pd.read_csv(dir, sep='\t', encoding='gbk')  # 6607 rows x 375 columns
        self.data_invjuzi = self.data_invjuzi.set_index('id')
        self.data_invjuzi['已投资轮次'][self.data_invjuzi['已投资轮次'] == 'arr_x'] = '-'
        self.data_invjuzi['已投资各轮次数量'][self.data_invjuzi['已投资轮次'] == 'arr_x'] = '-'

    def import_data_geshang(self, dir='./data/格上理财投资机构数据.txt'):
        """Import Geshang rawdata, dir is directory of data file."""
        self.data_geshang = pd.read_csv(dir, sep='\t', encoding='gbk')  # 10106 rows x 20 columns
        self.data_geshang = self.data_geshang.set_index('id')
        self.data_geshang['机构类型'][self.data_geshang['机构类型'] == '天使投资人'] = '天使投资'
        self.data_geshang['机构类型'][self.data_geshang['机构类型'] == 'FOF'] = 'FOFs'
        self.data_geshang['管理规模'][self.data_geshang['管理规模'] != self.data_geshang['管理规模']] = '----'  # delete NaN

    def gen_variables(self, normalize = True):
        """Generate variables in data."""

        # generate variables in IT橘子创投公司数据.txt
        self.total_amount = self.data_invjuzi['管理资本规模'].apply(get_invamount, args=(0,))
        self.CNY_amount = self.data_invjuzi['管理资本规模'].apply(get_invamount, args=(1,))
        self.USD_amount = self.data_invjuzi['管理资本规模'].apply(get_invamount, args=(2,))
        self.min_amount = self.data_invjuzi['单个项目投资规模'].apply(get_minmax_amount, args=(0,))
        self.max_amount = self.data_invjuzi['单个项目投资规模'].apply(get_minmax_amount, args=(1,))
        self.dummy_invarea = set_dummy(self.data_invjuzi['投资领域'], '投资领域')  # 6607 rows x 33 columns
        self.dummy_invround = set_dummy(self.data_invjuzi['投资轮次'], '投资轮次')  # 6607 rows x 9 columns
        item_industry = pd.concat([self.data_invjuzi['已投资行业'].apply(lambda x: re.split(r'\s', x)),
                                   self.data_invjuzi['已投资各行业数量'].apply(lambda x: re.split(r'\s', x))], axis=1)
        self.percent_industry = get_percent_var(item_industry, '已投资行业', '已投资各行业数量',
                                                ['企业服务', '体育运动', '医疗健康', '工具软件', '广告营销', '房产服务', '教育',
                                                 '文化娱乐', '旅游', '本地生活', '汽车交通', '游戏', '物流', '电子商务', '硬件',
                                                 '社交网络', '移动互联网', '金融'])
        item_round = pd.concat([self.data_invjuzi['已投资轮次'].apply(lambda x: re.split(r'\s', x)),
                                self.data_invjuzi['已投资各轮次数量'].apply(lambda x: re.split(r'\s', x))], axis=1)
        self.percent_round = get_percent_var(item_round, '已投资轮次', '已投资各轮次数量',
                                             ['A+轮', 'A轮', 'B+轮', 'B轮', 'C轮', 'D轮', 'E轮', 'F轮-上市前', 'IPO上市',
                                              'IPO上市后', 'Pre-A轮', 'Pre-B轮', '不明确', '天使轮', '战略投资',
                                              '新三板', '种子轮'])

        # generate variables in 格上理财投资机构数据.txt
        self.dummy_inv_type = pd.get_dummies(self.data_geshang['机构类型'], prefix='dummy_机构类型') \
            .drop('dummy_机构类型_----', axis=1)
        self.dummy_inv_type['dummy_机构类型_VC'] = self.dummy_inv_type['dummy_机构类型_VC'] + \
                                               self.dummy_inv_type['dummy_机构类型_VCPE'] + \
                                               self.dummy_inv_type['dummy_机构类型_VC/PE'] + \
                                               self.dummy_inv_type['dummy_机构类型_VC/战略投资者']
        self.dummy_inv_type['dummy_机构类型_PE'] = self.dummy_inv_type['dummy_机构类型_PE'] + \
                                               self.dummy_inv_type['dummy_机构类型_VCPE'] + \
                                               self.dummy_inv_type['dummy_机构类型_VC/PE']
        self.dummy_inv_type['dummy_机构类型_战略投资者'] = self.dummy_inv_type['dummy_机构类型_战略投资者'] + \
                                                  self.dummy_inv_type['dummy_机构类型_VC/战略投资者']
        self.dummy_inv_type.drop(['dummy_机构类型_VCPE', 'dummy_机构类型_VC/PE', 'dummy_机构类型_VC/战略投资者'],
                                 axis=1)  # 10106 rows x 8 columns

        self.dummy_cap_type = pd.get_dummies(self.data_geshang['资本类型'], prefix='dummy_资本类型') \
            .drop('dummy_资本类型_----', axis=1)  # 10106 rows x 3 columns

        self.manage_money = self.data_geshang['管理规模'].apply(replace_money)

        self.data_geshang['基金个数'][self.data_geshang['基金个数'] == '----'] = 0
        self.num_fund = self.data_geshang['基金个数'].apply(lambda x: int(x))

        self.data_geshang['投资数量'][self.data_geshang['投资数量'] == '----'] = 0
        self.num_inv = self.data_geshang['投资数量'].apply(lambda x: int(x))
        self.data_geshang['退出数量'][self.data_geshang['退出数量'] == '----'] = 0
        self.num_quit = self.data_geshang['退出数量'].apply(lambda x: int(x))
        self.num_quit_inv = self.num_quit / self.num_inv
        self.num_quit_inv[self.num_quit_inv == np.inf] = 1
        self.num_quit_inv[self.num_quit_inv != self.num_quit_inv] = 1  # or 0?

        self.percent_inv_industry = count_percent('投资项目行业分类', self.data_geshang)  # 10106 rows x 906 columns
        self.percent_inv_period = count_percent('投资项目投资阶段', self.data_geshang)  # 10106 rows x 6 columns
        self.percent_quit_industry = count_percent('退出项目行业分类', self.data_geshang)  # 10106 rows x 428 columns
        self.percent_quit_period = count_percent('退出项目退出方式', self.data_geshang)  # 10106 rows x 8 columns

        amount_invest = self.data_geshang['投资项目投资资金'].str.split(r'\s*', expand=True).stack().apply(replace_money)
        self.var_amount_invest = amount_invest.astype(float).replace(0, np.NaN).groupby(level=0).mean().replace(np.NaN,
                                                                                                                0)

        return_quit = self.data_geshang['退出项目账面回报'].str.split(r'\s*', expand=True).stack()
        return_quit[(return_quit == '-') | (return_quit == '----')] = 0
        self.var_return_quit = return_quit.astype(float).groupby(level=0).mean()


        if normalize:
            self.total_amount = (self.total_amount - np.min(self.total_amount)) / \
                                (np.max(self.total_amount) - np.min(self.total_amount)) - 0.5
            self.CNY_amount = (self.CNY_amount - np.min(self.CNY_amount)) / \
                                (np.max(self.CNY_amount) - np.min(self.CNY_amount)) - 0.5
            self.USD_amount = (self.USD_amount - np.min(self.USD_amount)) / \
                                (np.max(self.USD_amount) - np.min(self.USD_amount)) - 0.5
            self.min_amount = (self.min_amount - np.min(self.min_amount)) / \
                                (np.max(self.min_amount) - np.min(self.min_amount)) - 0.5 # TODO: 应该有一个判断项目是否符合的 indicator
            self.max_amount = (self.max_amount - np.min(self.max_amount)) / \
                                (np.max(self.max_amount) - np.min(self.max_amount)) - 0.5

            self.manage_money = (self.manage_money - np.min(self.manage_money)) / \
                              (np.max(self.manage_money) - np.min(self.manage_money)) - 0.5 # TODO: 应该有一个判断是否为空的 indicator
            self.num_fund = (self.num_fund - np.min(self.num_fund)) / \
                              (np.max(self.num_fund) - np.min(self.num_fund)) - 0.5
            self.num_inv = (self.num_inv - np.min(self.num_inv)) / \
                              (np.max(self.num_inv) - np.min(self.num_inv)) - 0.5
            self.num_quit = (self.num_quit - np.min(self.num_quit)) / \
                              (np.max(self.num_quit) - np.min(self.num_quit)) - 0.5
            self.num_quit_inv = (self.num_quit_inv - np.min(self.num_quit_inv)) / \
                              (np.max(self.num_quit_inv) - np.min(self.num_quit_inv)) - 0.5
            self.var_amount_invest = (self.var_amount_invest - np.min(self.var_amount_invest)) / \
                              (np.max(self.var_amount_invest) - np.min(self.var_amount_invest)) - 0.5
            self.var_return_quit = (self.var_return_quit - np.min(self.var_return_quit)) / \
                              (np.max(self.var_return_quit) - np.min(self.var_return_quit)) - 0.5


        self.variables_invjuzi = pd.concat([self.data_invjuzi['投资机构名称'], self.total_amount, self.CNY_amount,
                                            self.USD_amount, self.min_amount, self.max_amount, self.dummy_invarea,
                                            self.dummy_invround, self.percent_industry, self.percent_round],
                                           axis=1)  # 6607 rows x 83 columns
        self.variables_geshang = pd.concat([self.data_geshang['机构简称'], self.dummy_inv_type, self.dummy_cap_type,
                                            self.manage_money, self.num_fund, self.num_inv, self.num_quit,
                                            self.num_quit_inv,
                                            self.percent_inv_industry, self.percent_inv_period,
                                            self.percent_quit_industry,
                                            self.percent_quit_period, self.var_amount_invest, self.var_return_quit],
                                           axis=1)  # 10106 rows x 1369 columns

    def gen_data(self, normalize = True):
        """Merge variables and merge investors data"""

        self.data = self.variables_invjuzi.merge(self.variables_geshang, left_on='投资机构名称', right_on='机构简称', how='left')

    def delete_foreign(self):
        """Delete foreign investors"""
        pass

    def delete_small(self, data, sep=r'\s'):
        """Delete investors whose amount less than 1000,0000 $ or 6800,0000 ￥"""
        # data = self.data_invjuzi['投资组合金额']
        money_list = data.apply(lambda x: re.split(sep, str(x))).apply(lambda x: [replace_money(i) for i in x])
        self.data_invjuzi_deleted_small = data[money_list.apply(lambda x: not all(i < 6800 for i in x))]

    def delete_no_recent(self, data, column, sep=r'\s'):
        """Delete investors who didn't invest in last 3 years"""
        def delta_last_date(date_list):
            try:
                return pd.to_datetime('2017-05-10') - pd.to_datetime(date_list[0]) < datetime.timedelta(365 * 3)
            except:
                print(date_list)
                return False

        self.data_invjuzi_deleted_old = data[data.iloc[:, column].apply(lambda x: re.split(sep, str(x))).apply(lambda x: delta_last_date(x))]

    def gen_model_data(self):
        """Generate investors data for training"""
        data_merger = pd.read_csv('./data/itjuzi_geshang_finished.txt', sep=',', encoding='utf-8', )
        deleted_merged = pd.merge(left=self.variables_invjuzi.loc[self.data_invjuzi_deleted_old.index, :],
                                  right=data_merger[['投资机构名称', 'id']].rename(columns={'id': 'geshang_id'}),
                                  how='left')
        self.data_merged = pd.merge(left=deleted_merged, right=self.variables_geshang, how='left',
                               left_on='geshang_id', right_index=True)
        self.model_data = pd.concat([self.data_merged.drop(['geshang_id', '投资机构名称', '机构简称'], axis=1),
                                ~np.isnan(self.data_merged['geshang_id'].astype(float)) * 1], axis=1)\
                          .set_index(self.data_invjuzi_deleted_old.index)
        self.model_data = self.model_data.fillna(0)

if __name__ == '__main__':
    data_companies = DataCompany()
    data_companies.import_data_itjuzi()
    data_companies.import_data_radar()
    data_companies.gen_variables()
    data_companies.gen_data()

    print(data_companies.data.head())

    data_investors = DataInvestor()
    data_investors.import_data_invjuzi()
    data_investors.import_data_geshang()
    data_investors.gen_variables()

    # Get deleted data
    data_investors.delete_small(data=data_investors.data_invjuzi['投资组合金额'])
    merged_data = pd.merge(left=data_investors.data_invjuzi_deleted_small.to_frame(), right=data_investors.data_invjuzi['投资组合时间'].to_frame(), how='left', left_index=True, right_index=True)
    data_investors.delete_no_recent(data=merged_data, column=1)
    # deleted_data = pd.merge(left=data_investors.data_invjuzi['投资机构名称'].to_frame(), right=data_investors.data_invjuzi_deleted_old, how='right', left_index=True, right_index=True)
    # deleted_data['投资机构名称'].to_frame().to_csv('/media/gaofangshu/Windows/Users/Fangshu Gao/Desktop/demo/Sinvestor/deleted_data.csv')
    #
    # data_investors.data_geshang['id'] = data_investors.data_geshang.index
    # deletd_with_geshang = pd.merge(left=deleted_data['投资机构名称'].to_frame(), right=data_investors.data_geshang[['id', '机构简称']], how='left', left_on='投资机构名称', right_on='机构简称')
    # deletd_with_geshang.to_csv('/media/gaofangshu/Windows/Users/Fangshu Gao/Desktop/demo/Sinvestor/itjuzi_geshang_data.csv')

    data_investors.gen_model_data()

    print(data_investors.model_data.head())

# --------- End ---------
