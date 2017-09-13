# Sinvestors
A neural-networks to seek investors.

## 数据
### 格上理财和it橘子匹配问题
* it橘子的部分机构在格上理财里是基金，可以直接用基金对应机构作为匹配，但这方面之前遗漏了（橘子 id 334 之前）
* it橘子里有些机构则是格上理财里已经退出的创投项目，应该删去？
* it橘子里有些英文机构在格上理财里是用的中文翻译名，光靠搜索找不到
* 有的投资机构在格上理财的网页 id 是拼音，比如 `gongsi-ZhongNanZiBen.html`

## 各文件执行功能
### data_proc.py
* 创业公司数据读取并与雷达数据合并，而后数字化
* 投资机构数据读取并与格上数据合并，而后数字化
* 预测时读取需预测公司与原有数据合并后的结果并进行数字化

### check.py
* 按批次进行投资公司与创业公司的抽样生成观测值
* 对观测值生成交叉变量
* 多进程大规模生成观测值（低正样本）并保存

### getdata.py
* 对 check.py 中生成保存的数据进行并行处理
* 保留正样本并抽取负样本，保证正负样本比例为1:9
* 生成新的训练数据

### main.py
* 并行预处理数据（ check.py ）
* 直接将数据使用 fit_generator 的方法进行训练（正样本比例过低效果不佳）

### data_train.py
* 生成建立模型model（或者读取模型）
* 使用 getdata.py 生成好的数据进行模型的训练与保存

### predict.py
* 读取填写的公司信息并合并生成新的数据
* 生成此公司与所有机构的交叉变量（慢，可能需要并行处理）
* 读取模型并对投资概率进行预测，并输出预测结果

### model.py
* 定义了三种模型的生成、读取以及训练（迭代器或者直接 fit ）：自编码机+全连接 分支结构 全连接
* 需要进一步测试 xgb 等模型效果

### main_model.py
* 1.0 demo
