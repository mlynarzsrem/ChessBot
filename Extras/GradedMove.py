class GradedMove:
    def __init__(self,state,move):
        self.move=move
        self.state=state
        self.rank=0.0
    def updateRank(self,toAdd):
        self.rank+=toAdd
    def getTrainingData(self):
        finalReward =self.rank/float(100)
        return self.state,self.move,finalReward
    def getRank(self):
        return self.rank