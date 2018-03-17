from Board import *
from GradedMove import *
from NeuralNetwork import *
import numpy as np
import datetime

class Game:
    def __init__(self):
        self.board = Board()
        self.cCPUState, self.cPlState = self.board.getState()
        self.trainigData = []
        self.neuralNetwork = NeuralNetwork()

    def updateTrainigDataRanks(self,value):
        n = len(self.trainigData)
        for i in range(len(self.trainigData)):
            self.trainigData[i].updateRank(float(value)/n)
            n-=1

    def addNewTrainigData(self,newGradedMove):
        self.updateTrainigDataRanks(newGradedMove.getRank())
        self.trainigData.append(newGradedMove)
        if(len(self.trainigData)==5):
            toTrain = self.trainigData.pop(0)
            move,mProb =toTrain.getTrainingData()
            move = move.reshape(1,move.shape[0])
            self.neuralNetwork.train(move,[mProb])
    #Train NN with rest of training examples
    def gameOver(self,CPUwon):
        if(CPUwon==True):
            self.updateTrainigDataRanks(100)
        else:
            self.updateTrainigDataRanks(-100)
        for toTrain in self.trainigData:
            move,mProb =toTrain.getTrainingData()
            print(mProb)
            move = move.reshape(1,move.shape[0])
            self.neuralNetwork.train(move,np.array([mProb]))

    #Analyze all moves and choose the best
    def analyzeMoves(self,moveList):
        probs = [] #List with rates of each moves
        moves = [] #List of all valid moves
        for m in moveList:
            moves.append(self.convertMoveData(m))
        for m in moves:
            m = m.reshape(1,m.shape[0])
            probs.append(self.neuralNetwork.getPredition(m))
        #Find best move
        x = np.argmax(probs)
        return moves[x],probs[x]

    def updateGameLog(self,WHOwon):
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
        with open("logs/GameLog.txt", "a") as myfile:
            myfile.write(text)
        text =winner+' ; '+str(now.strftime("%Y-%m-%d %H:%M"))
        text+=' ; '+str(self.cPlState)+' ; '+str(self.cCPUState)+'; '+str(self.board.moveCount)+';\n'
        with open("logs/GameLog.csv", "a") as myfile2:
            myfile2.write(text)
    #Create 1D array to input it into the neural network
    def convertMoveData(self,move):
        finalList = []
        intBoard = self.board.getIntBoard()
        for row in intBoard:
            for x in row:
                finalList.append(x)
        for x in move:
            finalList.append(x)
        return np.asarray(finalList)

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
        move, prob = self.analyzeMoves(moveList)
        self.board.doMove(move[-4:],CPU=True)
        #Updaet game state
        gain, cost = self.updateGameState()
        #Create grade move
        self.addNewTrainigData(GradedMove(move,prob,gain))
        if (self.board.isKingChecked(CPU=False) == True):
            self.updateTrainigDataRanks(value=10)
            if(self.board.isLooser(CPU=False)):
                self.gameOver(CPUwon=True)
                return True ,1
        return False ,0
