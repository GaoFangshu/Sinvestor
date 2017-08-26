# -*- coding: utf-8 -*-

from keras.layers import Input, Dense, concatenate
from keras.models import Model
from keras.utils import plot_model

class autoencodermodel():

    def __init__(self, input_dim, encoding_dim):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        
        self.input_data = Input(shape=(input_dim,))
        self.encoded = Dense(encoding_dim, activation='relu')(input_data)
        self.decoded = Dense(input_dim, activation='sigmoid')(encoded)
        self.autoencoder = Model(input=self.input_data, output=self.decoded)
        self.encoder = Model(input=self.input_data, output=self.encoded)

        self.autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        
        print('■■■■■■■ 输入数据维度为：%d ■■■■■■■' %input_dim)
        print('■■■■■■■ 开始训练自编码机...目标维度：%d ■■■■■■■' %encoding_dim)


    def fitmodel(self, data, steps, epochs, max_q_size=100):
        self.autoencoder.fit_generator(data, steps_per_epoch=steps, epochs=epochs, max_q_size=100)
        


class branchmodel():

    def __init__(self, input_company_dim, input_investor_dim, input_cross_dim):
        input_company = Input(shape=(input_company_dim,), name='input_company')
        input_investor = Input(shape=(input_investor_dim,), name='input_investor')
        input_cross = Input(shape=(input_cross_dim,), name='input_cross')

        dense_company = Dense(input_company_dim//3, activation='relu')(input_company)
        dense_investor = Dense(input_investor_dim//3, activation='relu')(input_investor)

        merged_layer = concatenate([dense_company, dense_investor, input_cross], axis=-1)
        merged_dense = Dense(input_company_dim + input_investor_dim + input_cross_dim, activation='relu')(merged_layer)

        output_dense = Dense(1, activation='sigmoid', name='output_dense')(merged_dense)

        self.model = Model(input=[input_company, input_investor, input_cross], output=output_dense)
        self.model.compile(optimizer='adadelta', loss='binary_crossentropy')

        self.model.summary()
        plot_model(self.model, to_file='./model/branchmodel.png')

    def fitmodel(self, data, steps, epochs, max_q_size=100):
        self.model.fit_generator(data, steps_per_epoch=steps, epochs=epochs, max_q_size=100)
        

        
