from Dbase.dbase import DBase
import numpy as np
import json
import pickle
import random
import operator
class QAgent():
    def __init__(self):
        self.dbase  = DBase("qlearn2")

    def getNextMove(self,state,movelist,trainMode =True):
        state = state.flatten().tostring()
        moves = self.dbase.getMovesInState(state)
        if(len(moves)>0):
            nextMoves=pickle.loads(moves[0][0])
            print(nextMoves)
        else:
            mCount = len(movelist)
            keys = movelist
            values = []
            for i in range(mCount):
                p = random.randint(0,100)/float(100)
                values.append(p)
            nextMoves = dict(zip(keys,values))
            self.dbase.insertMoves(state,pickle.dumps(nextMoves))
        if(trainMode==True):
            x = random.randint(0,len(nextMoves.keys()) -1 )
            return list(nextMoves.keys())[x]
        else:
            return max(nextMoves.items(), key=operator.itemgetter(1))[0]
    def getReward(self,state,move,reward):
        state = state.flatten().tostring()
        moves = self.dbase.getMovesInState(state)[0][0]
        nextMoves =pickle.loads(moves)
        nextMoves[move]=min(max(0,nextMoves[move] +reward),1)
        self.dbase.updateMoves(state,pickle.dumps(nextMoves))


a =QAgent()

A = np.zeros((8,8))
moves =[(1,2,3,3),(2,3,4,4),(4,4,3,5)]
print(a.getNextMove(A,moves,False))
a.getReward(A,(1,2,3,3),-0.2)