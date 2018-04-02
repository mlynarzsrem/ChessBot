#Check if all values in string are digits
def isDigitList(values):
    for x in values:
        if(str(x).isdigit()==False):
            return False
    return True
#Check if all of integers in string are in board's range
def inRangeList(values):
    for x in values:
        if(int(x)>7 or int(x)<0):
            return False
    return True

#Check if input is valid
def isValidInput(input,size):
    if (len(input) != size or isDigitList(input) == False or inRangeList(input) == False):
        return False
    else:
        return True
#Convert string of ints to tuple
def getTuple(move):
    if(len(move)!=4):
        return None
    return (int(move[0]),int(move[1]),int(move[2]),int(move[3]))