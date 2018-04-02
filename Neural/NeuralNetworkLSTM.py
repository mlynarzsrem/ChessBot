import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout,Flatten ,LSTM ,Embedding
from keras.models import load_model
import os.path
tf.logging.set_verbosity(tf.logging.ERROR)
class NeuralNetwork:
    def __init__(self):
        self.mName='Neural/lstm_model.h5'
        if(os.path.isfile(self.mName)==True):
            self.model =load_model(self.mName)
        else:
            self.model = Sequential()
            self.model.add(LSTM(units=500,input_shape=(8,8),return_sequences= True))
            self.model.add(LSTM(500))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(units=1, activation='sigmoid'))
            self.model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
        self.saveModel()
    def getPredition(self,X):
        X =X.reshape((1,8,8))
        return self.model.predict(X,batch_size=1)
    def train(self,X,Y,epochs=20,bs=1):
        try:
            X = X.reshape((1, 8, 8))
            self.model.fit(X,Y,batch_size=bs,epochs=epochs,verbose=2)
        except:
            print("Error neural")
        self.saveModel()
    def saveModel(self):
        self.model.save(self.mName)
        print("Model saved!")