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

    def validateNextMoves(self,state,movelist,nextMoves):
        dirty = False
        for m in movelist:
            if (m not in nextMoves):
                dirty = True
                p = random.randint(0, 100) / float(100)
                nextMoves[m] = p
        if (dirty == True):
            self.dbase.updateMoves(state, pickle.dumps(nextMoves))
        return nextMoves
    def addNewState(self,state,movelist):
        mCount = len(movelist)
        keys = movelist
        values = []
        for i in range(mCount):
            p = random.randint(0, 100) / float(100)
            values.append(p)
        nextMoves = dict(zip(keys, values))
        self.dbase.insertMoves(state, pickle.dumps(nextMoves))
        return nextMoves
    def chooseMove(self,movelist,allNextMoves,trainMode):
        nextMoves = {m: allNextMoves[m] for m in movelist}
        if (trainMode == True):
            nextMovesList = list(nextMoves.keys())
            probs = np.array(list(nextMoves.values()))*100
            probs = probs/float(sum(probs))
            draw = choice(nextMovesList, 1, p=probs)
            return draw[0]
        else:
            return max(nextMoves.items(), key=operator.itemgetter(1))[0]
    def getNextMove(self,state,movelist,trainMode =True):
        state = state.flatten().tostring()
        moves = self.dbase.getMovesInState(state)
        if(len(moves)>0):
            nextMoves=pickle.loads(moves[0][0])
            nextMoves = self.validateNextMoves(state,movelist,nextMoves)
        else:
            nextMoves = self.addNewState(state,movelist)
        return self.chooseMove(movelist,nextMoves,trainMode)
    def getReward(self,state,move,reward):
        state = state.flatten().tostring()
        moves = self.dbase.getMovesInState(state)[0][0]
        nextMoves =pickle.loads(moves)
        nextMoves[move]=min(max(0,nextMoves[move] +reward),1)
        self.dbase.updateMoves(state,pickle.dumps(nextMoves))
