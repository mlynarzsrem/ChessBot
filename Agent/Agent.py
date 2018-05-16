from Dbase.DBase import DBase
import numpy as np
import json
import pickle
import random
import operator
from numpy.random import choice
class QAgent():
    def __init__(self):
        self.dbase  = DBase("qlearn2")
        self.alpha =0.9
        self.gamma =0.1

    #Add discovered state to the database
    def addNewState(self,state,movelist):
        #Number of possible moves in this state
        mCount = len(movelist)
        #Randomly initialize probabilites
        values = list(np.random.rand(mCount))
        #Create dictionary
        nextMoves = dict(zip(movelist, values))
        #Insert state to the database
        self.dbase.insertMoves(state, pickle.dumps(nextMoves))
        return nextMoves
    #Choose move in training or testing mode
    def chooseMove(self,nextMoves,trainMode):
        if (trainMode == True):
            nextMovesList = list(nextMoves.keys())
            x = random.randint(0,len(nextMovesList)-1)
            return nextMovesList[x]
        else:
            return max(nextMoves.items(), key=operator.itemgetter(1))[0]
    def getNextMove(self,state,movelist,trainMode =True,CPU=True):
        #Prepare the state before searching
        state = state.flatten().tostring()+bytes(CPU)
        #Search state in the database
        moves = self.dbase.getMovesInState(state)
        if(len(moves)>0):
            nextMoves=pickle.loads(moves[0][0])
        else:
            nextMoves = self.addNewState(state,movelist)
        return self.chooseMove(movelist,nextMoves,trainMode)
    #Get value of best move in state
    def getNextStateReward(self,state,curReward,CPU=True):
        if(state is not None):
            # Prepare the state before searching
            state = state.flatten().tostring()+bytes(CPU)
            ##Search state in the database
            moves = self.dbase.getMovesInState(state)
            if(len(moves)!=0):
                nextMoves=pickle.loads(moves[0][0])
                values =curReward - list(nextMoves.values())
                return max(values)
        return 0
    def getReward(self,state,move,reward,nextState = None,CPU=True):
        # Prepare the state before searching
        state = state.flatten().tostring()+bytes(CPU)
        #Get possible moves in this state
        moves = self.dbase.getMovesInState(state)[0][0]
        nextMoves =pickle.loads(moves)
        #Calculate reward
        nsReward = self.getNextStateReward(nextState,nextMoves[move],not CPU)
        finalReward = self.alpha*(reward + self.gamma*nsReward)
        #Update move rate
        nextMoves[move]=min(max(0,nextMoves[move] +finalReward),1)
        self.dbase.updateMoves(state,pickle.dumps(nextMoves))
