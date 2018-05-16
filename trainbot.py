import time
import os
from Game import Game
def selfLearning(hours, turnOfAfer,nMoves=50):
    calcTime =60*60*hours
    t_end = time.time() + calcTime
    while time.time() < t_end:
        x = Game()
        x.traingGame(nMoves=nMoves)
        statinfo = os.stat('F:\Projekty\chessbot2\ChessBot\Dbase\qlearn2.db')
        if(statinfo.st_size> 1000000000):
            raise 'Erorr'
    if(turnOfAfer == True):
        os.system('shutdown -s')