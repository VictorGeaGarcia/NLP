import operator
import os

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
import matplotlib.pyplot as plt
import pandas as pd

from nlp_code import Nlp_Model


def main():
    """
    Execute nlp_code module to get all_sentences, vectorize them and prepare list for a dataset
    :return: list containing every sentence vectorized and its corresponding 1 or 0 value and another list with
             vocabulary used for training
    """
    nlp_object = Nlp_Model()
    nlp_object.get_words_and_sentences()
    nlp_object.vectorize_fit()
    nlp_object.vectorize_transform()

    sorted_voc = sorted(nlp_object.vectorizer.vocabulary_.items(), key=operator.itemgetter(1))
    sorted_voc_list = [x[0] for x in sorted_voc]

    dataset = []

    for elem, features in enumerate(nlp_object.vector_array):
        if elem < nlp_object.len_code:
            dataset.append((list(features), 1))
        else:
            dataset.append((list(features), 0))

    return dataset, sorted_voc_list

def create_df(dataset, sorted_voc_list):
    """
    Create dataframe with columns: vocabulary list, its values are the corresponding vectorized matrix, and
    columns 'classif' with values 1 or 0.
    :param dataset:
    :param sorted_voc_list:
    :return:
    """
    X  = pd.DataFrame([x[0] for x in dataset], columns=sorted_voc_list)
    Y = pd.DataFrame([x[1] for x in dataset], columns=['classif'])
    df = pd.concat([X,Y], axis=1)
    return df

def neural_net(df):
    """
    Using dataframe with vectorized sentences, run a NN model on it and save it.
    """
    # Shuffle data
    df = df.sample(frac=1)
    X = df.loc[:,df.columns != 'classif']
    Y = df.loc[:,df.columns == 'classif']
    
    epochs = 1000

    model = Sequential()
    
    n_cols = X.shape[1]

    model.add(Dense(100, activation='relu', input_shape=(n_cols,)))
    model.add(Dropout(0.5))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    
    opt = tf.keras.optimizers.Adam(lr=1e-5, decay=1e-2)
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    history = model.fit(X, Y, batch_size= 20,validation_split=0.2, epochs=epochs)

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # TODO: handle saving model correctly
    current_path = os.getcwd()
    model.save('{0}/nlp_code_python_{1}.h5'.format(current_path,epochs))


dataset, sorted_voc_list = main()
df = create_df(dataset, sorted_voc_list)
neural_net(df)