from Pieces import *
import numpy as np
import copy


class Board:
    def __init__(self):
        self.board=np.empty(shape=(8,8),dtype=object)
        self.initBoard()
        self.destroyed = {}
        self.destroyed['CPU'] = []
        self.destroyed['PL'] = []
        self.whMove=False
        self.moveCount =0

    def initBoard(self):
        #Add computer's pieces
        for i in range(8): #add Pawns
            self.board[1,i]=Pawn(True,1,i)
        self.board[0, 0]=Rook(True,0,0);self.board[0, 7] =Rook(True,0,7)
        self.board[0, 1]=Knight(True,0,1);self.board[0, 6] =Knight(True,0,6)
        self.board[0, 2] = Bishop(True,0,2);self.board[0, 5] = Bishop(True,0,5)
        self.board[0, 3] = Queen(True,0,3); self.board[0, 4] = King(True,0,4)
        #Add player pieces
        for i in range(8): #add Pawns
            self.board[6,i]=Pawn(False,6,i)
        self.board[7, 0]=Rook(False,7,0);self.board[7, 7] =Rook(False,7,7)
        self.board[7, 1]=Knight(False,7,1);self.board[7, 6] =Knight(False,7,6)
        self.board[7, 2] = Bishop(False,7,2);self.board[7, 5] = Bishop(False,7,5)
        self.board[7, 4] = Queen(False,7,4); self.board[7, 3] = King(False,7,3)

    def getState(self):
        cpuState = sum([abs(x.getId())for x in self.destroyed['CPU']])
        playerState = sum([abs(x.getId()) for x in self.destroyed['PL']])
        return cpuState,playerState

    def whoseMove(self):
        return self.whMove

    def getIntBoard(self):
        intBoard = np.zeros(shape=(8,8),dtype='int32')
        for i in range(8):
            for j in range(8):
                if(self.board[i,j] is not None):
                    intBoard[i,j] = self.board[i,j].getId()
        return intBoard

    #Returns positon of the king
    def getKingPosition(self,CPU):
        if(CPU==True):
            king=6
        else:
            king=-6
        for x in range(8):
            for y in range(8):
                if(self.board[x,y] is not None and self.board[x,y].getId()==king):
                    return x,y

    def isKingChecked(self,CPU):
        dangerousCords =[(x[2],x[3]) for x in self.getAllMoves(not CPU,False)]
        if(len(dangerousCords)==0):
            return False
        if(self.getKingPosition(CPU) in dangerousCords):
            return True
        else:
            return False

    #Returns true if after this move player's King is checked
    def testMove(self,move,CPU):
        bTest = Board()
        bTest.board=self.board.copy()
        bTest.doMove(move,CPU)
        return bTest.isKingChecked(CPU)

    #Check if checked player has posibility to do move
    def isLooser(self,CPU):
        if(self.isKingChecked(CPU)==False):
            return False
        moves = self.getAllMoves(CPU,True)
        for m in moves:
            if(self.testMove(m,CPU)==False):
                return False
        return True

    #Extrac from all moves that ones which make your king safe
    def getValidCheckStateMoves(self,CPU):
        moveList = []
        moves = self.getAllMoves(CPU, True)
        for m in moves:
            if(self.testMove(m,CPU)==False):
                moveList.append(m)
        return moveList

    def getAllMoves(self,CPU,reCallable=False):
        moveList = []
        for i in range(8):
            for j in range(8):
                if(CPU==True):
                    if (self.board[i, j] is not None and self.board[i,j].getId()>0):
                            moveList += self.board[i, j].getMoves(self,reCallable)
                else:
                    if (self.board[i, j] is not None and self.board[i,j].getId()<0):
                            moveList += self.board[i, j].getMoves(self,reCallable)
        return moveList

    #param - move tuple(x0,y0,x1,y1)
    def doMove(self,move,CPU):
        x0=move[0];y0=move[1];x1=move[2];y1=move[3]
        if(self.board[x1,y1] is not None):
            dPiece = copy.copy(self.board[x1,y1])
            if(CPU==True):
                self.destroyed['CPU'].append(dPiece)
            else:
                self.destroyed['PL'].append(dPiece)
        if((x1==0 or x1 == 7) and abs(self.board[x0,y0].getId())==PawnValue ):
            self.board[x1,y1] = Queen(CPU,x1,y1)
        else:
            self.board[x1, y1] = copy.copy(self.board[x0,y0])
            self.board[x1, y1].setPosition(x1,y1)
        self.board[x0, y0] = None
        np.delete( self.board,[x0,x1])
        self.whMove= not self.whMove
        self.moveCount +=1

