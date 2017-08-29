# -*- coding: utf-8 -*-
import data_proc
import check
import model
import pandas as pd

# ------------------- Set hyperparameters -------------------

TRAIN_SIZE = 16000  # maxnum 19836 in data
# test_size: 4297 - train_size
BATCH_SIZE = 32
CROSS_DIM = 6
STEPS_PER_EPCHO = 5000
EPCHOS = 2

ENCODING_DIM = 50  # size of our encoded representations, assuming the input is 784 floats
NB_EPOCH_AUTOENCODER = 50
BATCH_SIZE_AUTOENCODER = 30

DENSE1_DIM = 1000
NB_EPOCH_MAIN = 30
BATCH_SIZE_MAIN = 1000


if __name__ == '__main__':

    # Import data
    data_companies = data_proc.DataCompany()
    data_companies.import_data_itjuzi()
    data_companies.import_data_radar()
    data_companies.gen_variables()
    data_companies.gen_data()
    print('■■■■■■■ 已读取 初创公司数据，维度：(%d, %d) ■■■■■■■'%(data_companies.data.shape[0], data_companies.data.shape[1]))

    data_investors = data_proc.DataInvestor()
    data_investors.import_data_invjuzi()
    data_investors.import_data_geshang()
    data_investors.gen_variables()

    # Get deleted data
    data_investors.delete_small(data=data_investors.data_invjuzi['投资组合金额'])
    merged_data = pd.merge(left=data_investors.data_invjuzi_deleted_small.to_frame(), right=data_investors.data_invjuzi['投资组合时间'].to_frame(), how='left', left_index=True, right_index=True)
    data_investors.delete_no_recent(data=merged_data, column=1)
    data_investors.gen_model_data()
    print('■■■■■■■ 已读取 投资机构数据，维度：(%d, %d) ■■■■■■■'%(data_investors.model_data.shape[0], data_investors.model_data.shape[1]))

    # Sampling
    observation = check.Observation(data_companies.data,
                              data_investors.model_data,
                              data_companies.data_itjuzi,
                              data_investors.data_invjuzi,
                              train_size=TRAIN_SIZE,
                              batch_size_main=BATCH_SIZE)
    print('■■■■■■■ 训练数据已经生成 ■■■■■■■')

    company_shape = observation.data_companies.shape[1]
    investor_shape = observation.data_investors.shape[1]

##    main_model = model.branchmodel(company_shape, investor_shape, CROSS_DIM)
    main_model = model.branchmodel(company_shape, investor_shape, CROSS_DIM, load_model_flag='branchmodel-2')
    main_model.fitmodel(observation.gen_observation(), STEPS_PER_EPCHO, EPCHOS)
    main_model.savemodel('branchmodel-4')


##    observation.gen_observation()
