# -*- coding: utf-8 -*-
import data_proc

# ------------------- Set hyperparameters -------------------

TRAIN_SIZE = 3000  # maxnum 4297 in data
# test_size: 4297 - train_size

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

    data_investors = data_proc.DataInvestor()
    data_investors.import_data_invjuzi()
    data_investors.import_data_geshang()
    data_investors.gen_variables()
    data_investors.gen_data()
