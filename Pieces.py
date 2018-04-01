from extras import *

PawnValue = 1
KnightValue = 2
BishopValue = 3
RookValue = 4
QueenValue = 5
KingValue = 6

class Piece:
    #param Piece value (integer), CPU if it's computer's piece then CPU==True else CPU# ==False
    def __init__(self,CPU,posX,posY):
        self.posX=posX #Position X - row
        self.posY=posY #PositionY - column
        self.value=0
        self.CPU=CPU
        self.isMoved = False
    #Returns piece value if it's computer's piece else return piece value multiplied by -1
    def getId(self):
        if(self.CPU==True):
            return self.value
        else:
            return self.value*-1
    #sets new piece position on board
    def setPosition(self,posX,posY):
        self.posX=posX
        self.posY=posY
        self.isMoved = True
    #Return current postion (tuple (posX,posY))
    def getPosition(self):
        return self.posX,self.posY
    def getMoves(self,board,gmCallA=False):
        pass

class Pawn(Piece): #Value =1
    def __init__(self,CPU,posX,posY):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=PawnValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        X = self.posX; Y = self.posY; movesList = []
        if(self.CPU==True):
            s=1;fRow=1 # s - Move direction, fRow-  starting row
        else:
            s=-1;fRow=6
        #get Moves
        if (inRange(X + s*1, Y) and board[X + s*1, Y] == 0 ):
            movesList.append((X, Y, X + s*1, Y))
        if(inRange(X+s*2,Y) and board[X+s*2,Y]==0and X==fRow): #First move of this Pawn
            movesList.append((X,Y,X+s*2,Y))
        #Get posible strikes
        for t in [(X+s*1,Y+1),(X + s*1, Y-1)]:
            if (inRange(t[0],t[1]) and isEnemy(board[t[0],t[1]],self.CPU)):
                movesList.append((X, Y,t[0], t[1]) )
        return movesList

class Knight(Piece):
    def __init__(self,CPU,posX,posY,reCallable=False):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=KnightValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        X = self.posX;Y = self.posY;movesList = []
        #Get all possible tatgetss
        targets = [(X+2,Y-1),(X+2,Y+1),(X-2,Y-1),(X-2,Y+1),(X+1,Y-2),(X+1,Y+2),(X-1,Y-2),(X-1,Y+2)]
        for t in targets:
            if (inRange(t[0], t[1]) and(board[t[0], t[1]] == 0 or isEnemy(board[t[0], t[1]],self.CPU))):
                movesList.append((X, Y,t[0], t[1]))
        return movesList

class Bishop(Piece):
    def __init__(self,CPU,posX,posY):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=BishopValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        X = self.posX;Y = self.posY;movesList = []
        for x in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            for i in range(1,8):
                X2 = X + (i * x[0]);Y2 = Y + (i * x[1])
                # Check if field is occupied by your piece and if is in still on board
                if(inRange(X2,Y2)==False or isFriend(board[X2,Y2],self.CPU)==True):
                    break
                movesList.append((X, Y,X2,Y2))
                # Finish discovering moves in this direction if you found enemyPiece
                if(isEnemy(board[X2,Y2],self.CPU)==True):
                    break
        return movesList

class Rook(Piece):
    def __init__(self,CPU,posX,posY):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=RookValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        X = self.posX;Y = self.posY;movesList = []
        for x in [(-1,0),(1,0),(0,-1),(0,1)]:
            for i in range(1,8):
                X2 = X + (i * x[0]);Y2 = Y + (i * x[1])
                # Check if field is occupied by your piece and if is in still on board
                if(inRange(X2,Y2)==False or isFriend(board[X2,Y2],self.CPU)==True):
                    break
                movesList.append((X, Y,X2,Y2))
                # Finish discovering moves in this direction if you found enemyPiece
                if(isEnemy(board[X2,Y2],self.CPU)==True):
                    break
        return movesList

class Queen(Piece):
    def __init__(self,CPU,posX,posY,danerousCord=None):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=QueenValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        X = self.posX;Y = self.posY;movesList = []
        for x in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            for i in range(1,8):
                X2 = X+(i*x[0]) ; Y2 = Y+(i*x[1])
                #Check if field is occupied by your piece and if is in still on board
                if(inRange(X2,Y2)==False or isFriend(board[X2,Y2],self.CPU)==True):
                    break
                movesList.append((X, Y,X2,Y2))
                #Finish discovering moves in this direction if you found enemyPiece
                if(isEnemy(board[X2,Y2],self.CPU)==True):
                    break
        return movesList

class King(Piece):
    def __init__(self,CPU,posX,posY):
        super(self.__class__, self).__init__(CPU,posX,posY)
        self.value=KingValue
    def getMoves(self,gameBoard,gmCallA=False):
        board = gameBoard.getIntBoard()
        dangerousCords = None
        if(gmCallA==True):
            #Get positions which can make my king checked
            dangerousCords = [(x[2],x[3]) for x in gameBoard.getAllMoves(not self.CPU)]
            if(len(dangerousCords)==0):
                dangerousCords=None;
        X = self.posX;Y = self.posY;movesList = []
        for x in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            X2 = X + (1 * x[0]);Y2 = Y + (1 * x[1])
            if (inRange(X2, Y2) == True and  isFriend(board[X2, Y2],self.CPU) == False):
                #Check if target field is dangerous
                if(dangerousCords is None or ((X2,Y2) not in dangerousCords)):
                    #check if it borders with enemy king
                    if(borders(board,X2,Y2,self.getId()*-1)==False):
                        movesList.append((X, Y, X2, Y2))
        castling = self.checkCastlingPosiblity(gameBoard,dangerousCords)
        if(castling is not None):
            movesList = movesList+ castling
        return movesList
    def checkCastlingPosiblity(self,gameBoard,dangerousCords):
        if(self.isMoved==True):
            return None
        board = gameBoard.getIntBoard()
        moves = []
        if(self.getId()>0):
            startX =0
        else:
            startX = 7
        if(self.posX != startX or self.posY !=4 or isIn((startX,6) ,dangerousCords)):
            return None
        if(abs(board[startX,7])==RookValue and gameBoard.board[startX,7].isMoved ==False):
            ispos =True
            for i in range(5,7):
                if(board[startX,i]!=0 or isIn((startX,i) ,dangerousCords)):
                    ispos = False
                    break
            if(ispos ==True and isIn((startX,6) ,dangerousCords)==False):
                moves.append((startX, self.posY, startX, 6))
        if (abs(board[startX, 0]) == RookValue and gameBoard.board[startX,0].isMoved ==False):
            ispos = True
            for i in range(2,4):
                if(board[startX,i]!=0 or isIn((startX,i) ,dangerousCords)):
                    ispos = False
                    break
            if(ispos ==True and isIn((startX,2) ,dangerousCords) ==False):
                moves.append((startX,self.posY,startX,2))
        return moves