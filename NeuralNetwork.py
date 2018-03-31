import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout,Flatten
from keras.models import load_model
import os.path
tf.logging.set_verbosity(tf.logging.ERROR)
class NeuralNetwork:
    def __init__(self,hiddenLayersNumber=2,hiddenUnits=500):
        self.mName='my_model.h5'
        if(os.path.isfile(self.mName)==True):
            self.model =load_model(self.mName)
        else:
            self.model = Sequential()
            self.model.add(Dense(units=500, activation='sigmoid', input_shape=(8,8)))
            self.model.add(Flatten())
            self.model.add(Dropout(0.15))
            #hidden layers
            for i in range(hiddenLayersNumber):
                self.model.add(Dense(units=hiddenUnits, activation='sigmoid'))
            #Output
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