from sklearn.neural_network import MLPClassifier
import numpy as np
class NeuralNetwork:
    def __init__(self):
        self.model = MLPClassifier(solver='lbfgs',hidden_layer_sizes=(500, 500), random_state=1,alpha=1e-5,activation='tanh')
        zeros = np.zeros((8,8))
        zeros = zeros.flatten()
        zeros = zeros.reshape((1,zeros.shape[0]))
        score  =np.array([0.5])
        score =score.reshape((1,1))
        print(score.shape)

        self.model.fit(zeros,score)
    def changeDataFormat(self,X):
        X = X.flatten()
        X = X.reshape((1, X.shape[0]))
        return X
    def getPredition(self,X):
        X =self.changeDataFormat(X)
        return self.model.predict(X)
    def train(self,X,Y,epochs=20,bs=1):
        X = self.changeDataFormat(X)
        for i in range(epochs):
            self.model.fit(X,Y)
        self.saveModel()
    def saveModel(self):
        #self.model.save(self.mName)
        print("Model saved!")