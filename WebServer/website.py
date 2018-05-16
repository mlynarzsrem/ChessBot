from flask import Flask, session, redirect, render_template_string,render_template
from Game import Game
from WebServer.View import View
from WebServer.ServerValidation import *
import uuid
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
Games = {}
v = View()
dBaseloc ="F:\Projekty\chessbot2\ChessBot\Dbase\qlearn2.db"

@app.route('/')
def start_page():
   #return ''
    return render_template('index.html')

def getGame():
    try:
        game_id = session['game']
        game = Games[game_id]
    except:
        session.pop('game',None)
        return None
    return game

@app.route('/newgame/<mode>')
def create_new_game(mode):
    endGame()
    if 'game' not in session:
        session['game'] = uuid.uuid4()
        if(mode=='train'):
            Games[session['game']] = Game(dbaseLoc=dBaseloc)
        else:
            Games[session['game']] = Game(False,dbaseLoc=dBaseloc)
    game =getGame()
    if(game is None):
        return redirect('/newgame')
    return render_template_string(v.getCurrentBoard(game.board.getIntBoard()))


def endGame():
    if 'game' in session:
        game_id = session['game']
        if game_id in Games.keys():
            del Games[game_id]
        session.pop('game', None)

@app.route('/getmoves/<position>')
def get_Moves(position):
    position = str(position).replace("9","")
    if 'game' not in session:
        return redirect('/')
    if(isValidInput(position,2)==False):
        return redirect('/newgame')
    game =getGame()
    if(game is None):
        return redirect('/newgame')
    x = int(position[0])
    y = int(position[1])
    return render_template_string(v.getMoves(game.board,x,y))

def makeGameIteration(game,moveFull):
    if(moveFull not in game.board.getValidCheckStateMoves(CPU=False)):
        return None,0
    game.board.doMove(moveFull, False)
    endgame, state = game.computerMove()
    #print(game.board.getIntBoard())
    #print('---------------------------')
    return endgame,state

@app.route('/makemove/<move>')
def make_Move(move):
    move = str(move).replace("9", "")
    if 'game' not in session:
        return redirect('/')
    if(isValidInput(move,4)==False):
        return redirect('/newgame')
    game =getGame()
    if(game is None):
        return redirect('/newgame')
    moveFull = getTuple(move)
    endgame,state = makeGameIteration(game,moveFull)
    if(endgame is None):
        return redirect('/newgame')
    if(endgame==True):
        game.updateGameLog(WHOwon=state)
        endGame()
        if(state==0):
            return render_template('endgame.html', state='You draw!')
        if (state == 1):
            return render_template('endgame.html', state='You lost!')
        if (state == -1):
            return render_template('endgame.html', state='You won!')

    v = View()
    return render_template_string(v.getCurrentBoard(game.board.getIntBoard()))
@app.route('/giveup')
def giveUp():
    endGame()
    return  redirect('/')


if __name__ == '__main__':
    app.run()
