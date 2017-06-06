data_itjuzi['创业经历1'][1] + ' ' + data_itjuzi['创业经历2'][1] # 创业经历的企业被谁投过，是为1，不是为0
data_itjuzi['创业经历'+'1']

def paste_string(data, name, num_start, num_end):
    string = ''
    for i in range(num_start, num_end + 1):
        if data[name + str(i)] != '-':
            string = string + data[name + str(i)] + ' '
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

check_relation(paste_string(data_itjuzi.iloc[1], '工作经历', 1, 12), paste_string(data_invjuzi.iloc[1], '投资人工作经历', 1, 60))
check_relation(paste_string(data_itjuzi.iloc[1], '教育经历', 1, 12), paste_string(data_invjuzi.iloc[1], '投资人教育经历', 1, 60))

def check_percent(string_company, string_investor):
    list_investor = string_investor.split(sep=' ')
    percent = list_investor.count(string_company) / len(list_investor)
    return percent

check_percent(data_itjuzi['一级分类'].iloc[4], data_invjuzi['投资组合行业'].iloc[1])



data_invjuzi['投资组合行业']
data_itjuzi['一级分类'].value_counts()
data_itjuzi['二级分类']

paste_string(data_itjuzi.iloc[1], '创业经历', 1, 12)
paste_string(data_itjuzi.iloc[15], '工作经历', 1, 12)
paste_string(data_itjuzi.iloc[1], '教育经历', 1, 12)
paste_string(data_invjuzi.iloc[25], '投资人工作经历', 1, 60)
paste_string(data_invjuzi.iloc[1], '投资人教育经历', 1, 60)
paste_string(data_invjuzi.iloc[1], '投资组合行业', 1, 60)





data_itjuzi['工作经历1'] data_invjuzi['投资人工作经历1'] # 工作经历直接dummy?  bubububu, 要跟投资机构的工作经历比对
data_itjuzi['教育经历1'] data_invjuzi['投资人教育经历1'] # 比对

data_invjuzi['投资组合行业']  # 行业占以前的比重      # 需要一个比对字符计数的函数
data_invjuzi['投资组合金额']　# 当前币种，占曾经被投资的比重，
                               # 目标金额和历史平均的差别
投资组合轮次
data_invjuzi['投资组合轮次'] #　当前投资轮次占历史的百分之几

data_invjuzi['投资人职位1'] # 暂时没有给职位赋权重
data_invjuzi['投资人投资项目1']

