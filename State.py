class State:
    def __init__(self,move,state):
        self.state= state
        self.move = move
    def getMove(self):
        return self.move
    def getState(self):
        return self.state

