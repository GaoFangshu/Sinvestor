# -*- coding: utf-8 -*-

import pandas as pd
import multiprocessing
import os

def getdata(id, queue, info_queue):
    # 子进程函数，用于打开文件读取正样本抽取负样本
    info_queue.put('Worker %d: Begin work!'%id)
    try:
        data = pd.read_csv('./data/saved_data/saved_data_%d.csv'%id)
    except:
        return
    data_1 = data[data['2842']==1]
    data_2 = data[data['2842'] == 0].sample(len(data_1)*9)
    data = pd.concat([data_1, data_2])
    queue.put(data)
    info_queue.put('Worker %d: Get it!'%id)


if __name__ == '__main__':
    # 多进程准备
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    manager = multiprocessing.Manager()

    # 数据传输与信息传输
    data_queue = manager.Queue()
    info_queue = manager.Queue()

    # 获取文件编号
    file_list = []
    for parent,dirnames,filenames in os.walk('./data/saved_data'):
        for filename in filenames:
            file_list.append(filename)
    max_count = 0
    for file in file_list:
        if int(file[file.find('data_')+5:-4]) >= max_count:
            max_count = int(file[file.find('data_')+5:-4])

    # 分多次开始多进程，设定每次进程树
    count_list = []
    while max_count > 50:
        count_list.append(50)
        max_count -= 50
    count_list.append(max_count)

    # 准备多进程变量，包括data，传入id与已处理文件数
    data = pd.DataFrame()
    id_now = 0
    count = 0

    # 多次多进程循环
    for cl in count_list:

        # 此次循环是否全部处理完毕
        count_now = 0

        # 开启多进程
        for i in range(cl):
            worker = multiprocessing.Process(target=getdata, args=(id_now+1, data_queue, info_queue))
            id_now += 1
            worker.start()

        # 捕获信息与数据
        while 1:
            # 捕获数据
            if data_queue.empty() == 0:
                data_temp = data_queue.get(True)
                data = pd.concat([data, data_temp])
                count += 1
                count_now += 1
                print('%d files have been handled!'%count)
            # 捕获信息
            if info_queue.empty() == 0:
                info = info_queue.get(True)
                print(info)
            # 判断此次多进程是否处理完毕
            if count_now == cl:
                break

    data.to_csv('./data/merged.csv', index=0)
    print('------------ Data has been saved ! ------------')
    

            
