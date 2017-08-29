# -*- coding: utf-8 -*-

from keras.layers import Input, Dense, concatenate
from keras.models import load_model
from keras.models import Model
from keras.utils import plot_model
from keras import metrics

class autoencodermodel():

    def __init__(self, input_dim, encoding_dim):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        
        self.input_data = Input(shape=(input_dim,))
        self.encoded = Dense(encoding_dim, activation='relu')(input_data)
        self.decoded = Dense(input_dim, activation='sigmoid')(encoded)
        self.autoencoder = Model(input=self.input_data, output=self.decoded)
        self.encoder = Model(input=self.input_data, output=self.encoded)

        self.autoencoder.compile(optimizer='adadelta',
                                 loss='binary_crossentropy',
                                 metrics=['accuracy', metrics.precision, metrics.recall, metrics.fmeasure])
        
        print('■■■■■■■ 输入数据维度为：%d ■■■■■■■' %input_dim)
        print('■■■■■■■ 开始训练自编码机...目标维度：%d ■■■■■■■' %encoding_dim)


    def fitmodel(self, data, steps, epochs, max_q_size=100):
        self.autoencoder.fit_generator(data, steps_per_epoch=steps, epochs=epochs, max_q_size=100)
        


class branchmodel():

    def __init__(self, input_company_dim, input_investor_dim, input_cross_dim, load_model_flag=0):
        if load_model_flag:
            self.model = load_model('./model/savedmodel/%s.h5'%load_model_flag)
            self.model.summary()
        else:
            input_company = Input(shape=(input_company_dim,), name='input_company')
            input_investor = Input(shape=(input_investor_dim,), name='input_investor')
            input_cross = Input(shape=(input_cross_dim,), name='input_cross')

            dense_company = Dense(input_company_dim//3, activation='relu')(input_company)
            dense_investor = Dense(input_investor_dim//3, activation='relu')(input_investor)

            merged_layer = concatenate([dense_company, dense_investor, input_cross], axis=-1)
            merged_dense = Dense(input_company_dim + input_investor_dim + input_cross_dim, activation='relu')(merged_layer)

            output_dense = Dense(1, activation='sigmoid', name='output_dense')(merged_dense)

            self.model = Model(input=[input_company, input_investor, input_cross], output=output_dense)
            self.model.compile(optimizer='adadelta',
                               loss='binary_crossentropy',
                               metrics=['accuracy', metrics.precision, metrics.recall, metrics.fmeasure])

            self.model.summary()
            plot_model(self.model, to_file='./model/picture/branchmodel.png')

    def savemodel(self, name, path='./model/savedmodel/'):
        self.model.save('%s%s.h5'%(path, name))

    def fitmodel(self, data, steps, epochs, max_q_size=100):
        self.model.fit_generator(data, steps_per_epoch=steps, epochs=epochs, max_q_size=100)
        

class sequentialmodel():

    def __init__(self, input_company_dim, input_investor_dim, input_cross_dim):
        input_company = Input(shape=(input_company_dim,), name='input_company')
        input_investor = Input(shape=(input_investor_dim,), name='input_investor')
        input_cross = Input(shape=(input_cross_dim,), name='input_cross')

        merged_layer = concatenate([input_company, input_investor, input_cross], axis=-1)

        dense_layer_1 = Dense((input_company_dim + input_investor_dim + input_cross_dim)//3, activation='relu')(merged_layer)
        dense_layer_2 = Dense((input_company_dim + input_investor_dim + input_cross_dim)//9, activation='relu')(dense_layer_1)
        dense_layer_3 = Dense((input_company_dim + input_investor_dim + input_cross_dim)//27, activation='relu')(dense_layer_2)

        output_dense = Dense(1, activation='sigmoid', name='output_dense')(dense_layer_3)

        self.model = Model(input=[input_company, input_investor, input_cross], output=output_dense)
        self.model.compile(optimizer='adadelta',
                           loss='binary_crossentropy',
                           metrics=['accuracy', metrics.precision, metrics.recall, metrics.fmeasure])

        self.model.summary()
        plot_model(self.model, to_file='./model/picture/sequentialmodel.png')

    def savemodel(self, name, path='./model/savedmodel/'):
        self.model.save('%s%s.h5'%(path, name))

    def fitmodel(self, data, steps, epochs, max_q_size=100):
        self.model.fit_generator(data, steps_per_epoch=steps, epochs=epochs, max_q_size=100)        
