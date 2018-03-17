import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import os.path
tf.logging.set_verbosity(tf.logging.ERROR)
class NeuralNetwork:
    def __init__(self,hiddenLayersNumber=6,hiddenUnits=60):
        self.mName='my_model.h5'
        if(os.path.isfile(self.mName)==True):
            self.model =load_model(self.mName)
        else:
            self.model = Sequential()
            self.model.add(Dense(units=68, activation='relu', input_dim=68))
            #hidden layers
            for i in range(hiddenLayersNumber):
                self.model.add(Dense(units=hiddenUnits, activation='relu'))
            #Output
            self.model.add(Dense(units=1, activation='sigmoid'))
            self.model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['mean_squared_error'])
    def getPredition(self,X):
        return self.model.predict(X,batch_size=1)
    def train(self,X,Y,epochs=15,bs=1):
        try:
            self.model.fit(X,Y,batch_size=bs,epochs=epochs)
        except:
            pass
        self.saveModel()
    def saveModel(self):
        self.model.save(self.mName)
        print("Model saved!")