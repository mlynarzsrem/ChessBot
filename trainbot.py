import time
import os
from Game import Game
import argparse

parser = argparse.ArgumentParser(description='Train the chessbot.')

parser.add_argument('hours', type=int,help='How many hours chessbot have to be trained')
parser.add_argument('--iterations', type=int, default=50,help='Number of iterations')
parser.add_argument('--dBaseLoc',default="Dbase/qlearn2.db",help="Location of database")
parser.add_argument('--turnOfAfter',type=bool,default=False,help="Turn of computer after finishing")
args = parser.parse_args()
def selfLearning(hours, turnOfAfer=False,nMoves=50,dBaseLoc = "Dbase/qlearn2.db"):
    calcTime =int(60*60*hours)
    t_end = time.time() + calcTime
    while time.time() < t_end:
        x = Game(dbaseLoc=dBaseLoc)
        x.traingGame(nMoves=nMoves)
        statinfo = os.stat(dBaseLoc)
        if(statinfo.st_size> 1000000000):
            raise 'Erorr'
    if(turnOfAfer == True):
        os.system('shutdown -s')

selfLearning(hours=args.hours,turnOfAfer=args.turnOfAfter,nMoves=args.iterations,dBaseLoc=args.dBaseLoc)