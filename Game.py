from GameEngine.Board import *
from Extras.GradedMove import *
from Neural.NeuralNetworkLSTM import *
import numpy as np
import datetime
import math
from Extras.State import State


class Game:
    def __init__(self,tm=True):
        self.board = Board()
        self.cCPUState, self.cPlState = self.board.getState()
        self.trainigData = []
        self.neuralNetwork = NeuralNetwork()
        self.trainMode = tm

    def updateTrainigDataRanks(self,value):
        n = len(self.trainigData)
        for i in range(len(self.trainigData)):
            self.trainigData[i].updateRank(float(value)/math.sqrt(n))
            n-=1

    def addNewTrainigData(self,newGradedMove):
        if(self.trainMode ==True):
            self.updateTrainigDataRanks(newGradedMove.getRank())
            self.trainigData.append(newGradedMove)
            if(len(self.trainigData)==5):
                toTrain = self.trainigData.pop(0)
                state,mProb =toTrain.getTrainingData()
                self.neuralNetwork.train(state,[mProb])
    #Train NN with rest of training examples
    def gameOver(self,CPUwon):
        if(self.trainMode ==True):
            if(CPUwon==True):
                self.updateTrainigDataRanks(100)
            else:
                self.updateTrainigDataRanks(-100)
            for toTrain in self.trainigData:
                state,mProb =toTrain.getTrainingData()
                self.neuralNetwork.train(state,np.array([mProb]))

    #Analyze all moves and choose the best
    def analyzeMoves(self,moveList):
        probs = [] #List with rates of each moves
        states = [] #List of all valid moves
        for m in moveList:
            state = self.convertMoveData(m)
            move = m
            states.append(State(move,state))
        for s in states:
            state =s.getState()
            probs.append(self.neuralNetwork.getPredition(state))
        #Find best move
        x =np.argmax(probs)
        print(probs)
        return states[x],probs[x]

    def updateGameLog(self,WHOwon):
        if(self.trainMode ==False):
            if(WHOwon==1):
                winner ='COMPUTER'
            if (WHOwon == -1):
                winner='PLAYER'
            if (WHOwon == 0):
                winner='DRAW'
            now = datetime.datetime.now()
            text ='\nWinner '+winner+' Date: '+str(now.strftime("%Y-%m-%d %H:%M"))
            text+=' Player state: '+str(self.cPlState)+' Computer state: '+str(self.cCPUState)+' Liczba ruchów: '+str(self.board.moveCount)+'\n'
            text+='-----------------------------------------------------------------------------\n'
            with open("/home/mlynarzsrem/mysite/logs/GameLog.txt", "a") as myfile:
                myfile.write(text)
            text =winner+' ; '+str(now.strftime("%Y-%m-%d %H:%M"))
            text+=' ; '+str(self.cPlState)+' ; '+str(self.cCPUState)+'; '+str(self.board.moveCount)+';\n'
            with open("/home/mlynarzsrem/mysite/logs/GameLog.csv", "a") as myfile2:
                myfile2.write(text)
    #Create 1D array to input it into the neural network
    def convertMoveData(self,move):
        state =  self.board.getStateAfterMove(move=move,CPU=True)
        arr = np.asarray(state)
        return arr
    #Retruns diffrences between prievious and current game state
    def updateGameState(self):
        cpuState, playerState = self.board.getState()
        #Points gained by CPU == lost by player
        gain = -1*(cpuState - self.cCPUState)**2
        #Points gained by player == lost by CPU
        cost = (self.cPlState - playerState)**2
        self.cCPUState=cpuState
        self.cPlState=playerState
        return gain,cost

    #Returns
    # endgame: boolean - True if game is ended
    # state : integer - '-1' if player won, '1' if CPU won 0 if was a draw
    def computerMove(self):
        gain,cost = self.updateGameState()
        self.updateTrainigDataRanks(cost)
        #Check if is check
        moveList = self.board.getValidCheckStateMoves(CPU=True)
        if(self.board.isKingChecked(CPU=True)==True):
            self.updateTrainigDataRanks(value=-10)
            if(len(moveList)==0):
                self.gameOver(CPUwon=False)
                return True,-1
        if (len(moveList) == 0):
            self.updateTrainigDataRanks(-30)
            return True, 0
        # Get best move and execute it
        state, prob = self.analyzeMoves(moveList)
        self.board.doMove(state.getMove(),CPU=True)
        #Updaet game state
        gain, cost = self.updateGameState()
        #Create grade move
        self.addNewTrainigData(GradedMove(state.getState(),prob,gain))
        if (self.board.isKingChecked(CPU=False) == True):
            self.updateTrainigDataRanks(value=10)
            if(self.board.isLooser(CPU=False)):
                self.gameOver(CPUwon=True)
                return True ,1
        return False ,0
x = Game()
x.computerMove()
