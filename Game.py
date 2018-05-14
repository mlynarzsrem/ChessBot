from GameEngine.Board import *
from Extras.GradedMove import *
from Agent.Agent import QAgent
import numpy as np
import datetime
import math
from Extras.State import State


class Game:
    def __init__(self,tm=True):
        self.board = Board()
        self.cCPUState, self.cPlState = self.board.getState()
        self.trainigData = []
        self.trainigDataNCPU = []
        self.qAgent = QAgent()
        self.trainMode = tm

    def updateTrainigDataRanks(self,value,CPU =True):
        if(CPU==True):
            trainigData =self.trainigData
        else:
            trainigData = self.trainigDataNCPU
        n = len(trainigData)
        for i in range(len(trainigData)):
            trainigData[i].updateRank(float(value)/math.sqrt(n))
            n-=1

    def addNewTrainigData(self,newGradedMove,CPU =True):
        if(CPU==True):
            trainigData =self.trainigData
        else:
            trainigData = self.trainigDataNCPU
        if(self.trainMode ==True):
            self.updateTrainigDataRanks(newGradedMove.getRank())
            trainigData.append(newGradedMove)
            if(len(self.trainigData)==5):
                toTrain = trainigData.pop(0)
                state,move,reward =toTrain.getTrainingData()
                self.qAgent.getReward(state,move,reward)
    #Train NN with rest of training examples
    def gameOver(self,CPUwon):
        if(self.trainMode ==True):
            if(CPUwon==True):
                self.updateTrainigDataRanks(100)
                self.updateTrainigDataRanks(-100,False)
            else:
                self.updateTrainigDataRanks(-100)
                self.updateTrainigDataRanks(100, False)
            for toTrain in self.trainigData:
                state,move,reward =toTrain.getTrainingData()
                self.qAgent.getReward(state,move,reward)
            for toTrain in self.trainigDataNCPU:
                state,move,reward =toTrain.getTrainingData()
                self.qAgent.getReward(state,move,reward)

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
            self.updateTrainigDataRanks(value=10,CPU=False)
            if(len(moveList)==0):
                self.gameOver(CPUwon=False)
                return True,-1
        if (len(moveList) == 0):
            self.updateTrainigDataRanks(-30)
            self.updateTrainigDataRanks(-30,False)
            return True, 0
        # Get best move and execute it
        state = self.board.getIntBoard()
        move = self.qAgent.getNextMove(state,moveList,self.trainMode)
        self.board.doMove(move,CPU=True)
        #Updaet game state
        gain, cost = self.updateGameState()
        #Create grade move
        self.addNewTrainigData(GradedMove(state,move,gain))
        if (self.board.isKingChecked(CPU=False) == True):
            self.updateTrainigDataRanks(value=10)
            self.updateTrainigDataRanks(value=-10, CPU=False)
            if(self.board.isLooser(CPU=False)):
                self.gameOver(CPUwon=True)
                return True ,1
        return False ,0
    def playerMove(self):
        cost, gain = self.updateGameState()
        self.updateTrainigDataRanks(cost,False)
        moveList = self.board.getValidCheckStateMoves(CPU=False)
        state = self.board.getIntBoard()
        move = self.qAgent.getNextMove(state, moveList, self.trainMode)
        self.board.doMove(move, CPU=False)
        cost, gain = self.updateGameState()
        self.addNewTrainigData(GradedMove(state, move, gain),False)
    def traingGame(self,nMoves=50):
        for i in range(nMoves):
            state,x =self.computerMove()
            if(state==True):
                break
            else:
                self.playerMove()
"""
for i in range(10):
    x = Game()
    x.traingGame()
    """

