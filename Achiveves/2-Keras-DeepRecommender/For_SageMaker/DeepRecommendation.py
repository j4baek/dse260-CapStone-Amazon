#!/usr/bin/env python3

# Tensorflow
import tensorflow as tf
import warnings
warnings.filterwarnings("ignore")
import re

# import nltk
# import tqdm as tqdm
# import sqlite3
import pandas as pd
import numpy as np
from pandas import DataFrame 
import string

#from nltk.corpus import stopwords
#stop = stopwords.words("english")
# from nltk.stem.porter import PorterStemmer
# english_stemmer=nltk.stem.SnowballStemmer('english')
# from nltk.tokenize import word_tokenize

from sklearn.metrics import accuracy_score, confusion_matrix,roc_curve, auc,classification_report, mean_squared_error, mean_absolute_error
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection  import train_test_split
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn import neighbors
from scipy.spatial.distance import cosine
from sklearn.feature_selection import SelectKBest
# from IPython.display import SVG

import pickle
import time
import gzip
import os
os.getcwd()

#Keras
# from tensorflow.python.keras import Sequential
# from tensorflow.python.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
# from tensorflow.python.training.rmsprop import RMSPropOptimizer

from tensorflow.python.keras import Sequential, Model
from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.layers import Dense, Activation, Dropout, Input, Masking, TimeDistributed, LSTM, Conv1D, Embedding
from tensorflow.python.keras.layers import GRU, Bidirectional, BatchNormalization, Reshape
from tensorflow.python.keras.optimizers import Adam

from tensorflow.python.keras.layers.core import Reshape, Dropout, Dense
from tensorflow.python.keras.layers.merge import Multiply, Dot, Concatenate
from tensorflow.python.keras.layers.embeddings import Embedding
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.utils.vis_utils import model_to_dot

#Pandas
import pandas as pd


def train(review_data):
    ################################################################
    # declare input embeddings to the model
    #User input
    user_id_input = Input(shape=[1], name='user')
    #Item Input
    item_id_input = Input(shape=[1], name='item')
    price_id_input = Input(shape=[1], name='price')
    title_id_input = Input(shape=[1], name='title')

    # define the size of embeddings as a parameter
    # ****H: size_of_embedding - 5, 10 , 15, 20, 50
    size_of_embedding = 15
    user_embedding_size = size_of_embedding 
    item_embedding_size = size_of_embedding
    price_embedding_size = size_of_embedding
    title_embedding_size = size_of_embedding

    # apply an embedding layer to all inputs
    user_embedding = Embedding(output_dim=user_embedding_size, input_dim=users.shape[0],
                                   input_length=1, name='user_embedding')(user_id_input)

    item_embedding = Embedding(output_dim=item_embedding_size, input_dim=items_reviewed.shape[0],
                                   input_length=1, name='item_embedding')(item_id_input)

    price_embedding = Embedding(output_dim=price_embedding_size, input_dim=price.shape[0],
                               input_length=1, name='price_embedding')(price_id_input)

    title_embedding = Embedding(output_dim=title_embedding_size, input_dim=titles.shape[0],
                               input_length=1, name='title_embedding')(title_id_input)

    # reshape from shape (batch_size, input_length,embedding_size) to (batch_size, embedding_size). 
    user_vecs = Reshape([user_embedding_size])(user_embedding)
    item_vecs = Reshape([item_embedding_size])(item_embedding)
    price_vecs = Reshape([price_embedding_size])(price_embedding)
    title_vecs = Reshape([title_embedding_size])(title_embedding)    
    
    ################################################################
    # Concatenate the item embeddings :
    item_vecs_complete  = Concatenate()([item_vecs, price_vecs,title_vecs])

    # Concatenate user and item embeddings and use them as features for the neural network:
    input_vecs = Concatenate()([user_vecs, item_vecs_complete]) # can be changed by Multiply
    #input_vecs = Concatenate()([user_vecs, item_vecs]) # can be changed by Multiply

    # Multiply user and item embeddings and use them as features for the neural network:
    #input_vecs = Multiply()([user_vecs, item_vecs]) # can be changed by concat 

    # Dropout is a technique where randomly selected neurons are ignored during training to prevent overfitting 
    input_vecs = Dropout(0.1)(input_vecs)  

    # Check one dense 128 or two dense layers (128,128) or (128,64) or three denses layers (128,64,32))

    # First layer
    # Dense(128) is a fully-connected layer with 128 hidden units.
    # Use rectified linear units (ReLU) f(x)=max(0,x) as an activation function.
    x = Dense(128, activation='relu')(input_vecs)
    x = Dropout(0.1)(x) # Add droupout or not # To improve the performance

    # Next Layers
    #x = Dense(128, activation='relu')(x) # Add dense again or not 
    x = Dense(64, activation='relu')(x) # Add dense again or not 
    x = Dropout(0.1)(x) # Add droupout or not # To improve the performance
    x = Dense(32, activation='relu')(x) # Add dense again or not #
    x = Dropout(0.1)(x) # Add droupout or not # To improve the performance

    # The output
    y = Dense(1)(x)

    
    ################################################################
    model = Model(inputs=[user_id_input,
                          item_id_input,
                          price_id_input,
                          title_id_input
                         ], 
              outputs=y)

    
    ################################################################
    # ****H: loss
    # ****H: optimizer
    model.compile(loss='mse',
                  optimizer="adam" )
    
    
    ################################################################
    
    save_path = "./"
    mytime = time.strftime("%Y_%m_%d_%H_%M")
    # modname = 'dense_2_15_embeddings_2_epochs' + mytime 
    modname = 'dense_2_15_embeddings_2_epochs'
    thename = save_path + '/' + modname + '.h5'
    mcheck = ModelCheckpoint(thename  , monitor='val_loss', save_best_only=True)
    
    ################################################################
    
    # ****H: batch_size
    # ****H: epochs
    # ****H: 
    # ****H: 
    
    history = model.fit([ratings_train["user_id"],
                        ratings_train["item_id"],
                        ratings_train["price_id"],
                        ratings_train["title_id"]
                        ]
                        , ratings_train["score"]
                        , batch_size=64
                        , epochs=2
                        , validation_split=0.2
                        , callbacks=[mcheck]
                        , shuffle=True)
    
    print("MSE: ", history.history)
    
    return model




