class GradedMove:
    def __init__(self,move,mProb,mRank):
        self.move=move
        self.prob=mProb
        self.rank=mRank
    def updateRank(self,toAdd):
        self.rank+=toAdd
    def getTrainingData(self):
        finalProb=self.prob+(float(self.rank)/100)
        finalProb = min(1,max(0,finalProb))
        return self.move,finalProb
    def getRank(self):
        return self.rank