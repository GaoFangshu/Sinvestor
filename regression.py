from sklearn import linear_model

def regression(x, y):
    # x 是各个投资机构的投资数目，经过标准化后
    # y 是神经网络模型得到的预测概率
    lir = linear_model.LinearRegression()
    lir.fit(x, y)
    error = y - x.dot(lir.coef_)
    # 嵌入读写结果的部分，比如 predict.getname
    # 或者在 predict 里面写
    return error