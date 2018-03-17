
def inRange(posX, posY):
    cond1 = (posX>=0 and posX<8)
    cond2 = (posY >= 0 and posY < 8)
    if(cond1 and cond2):
        return True
    else:
        return False

def isEnemy(value, CPU):
    if(CPU==True):
        if(value<0):
            return True
        else:
            return False
    else:
        if(value>0):
            return True
        else:
            return False

def isFriend(value, CPU):
    if(CPU==True):
        if(value>0):
            return True
        else:
            return False
    else:
        if(value<0):
            return True
        else:
            return False

def borders(board,X,Y, value):
    for x in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        X2 = X + (1 * x[0]);
        Y2 = Y + (1 * x[1])
        if( inRange(X2,Y2) and board[X2,Y2]==value):
            return True
    return False