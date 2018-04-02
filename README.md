# ChessBot 1.0

##  About project

### Project's idea

ChessBot 1.0 is self-learning chess algorithm written in Python. The idea
of project is to learn neural network to play a chess by playing against a
human. Technically it is very difficult to achieve because neural network
has to play many games to how to play properly, and "many" doesn't mean
hundreds or even thousands it's rather about milions.

### So, how is it work?

Well... Actually it is not working at all. I encountered a problem which
I think results from wrong way of data's representation. But It's my
first machine learning project and I hope that I will find the issue and
I fix it someday.

### How it should work?

#### 1. Data's representation

The algorithm is using neural network to evalute state which is result of
execution of the specific move. State is rated in the range from -1
(bad state) to 1 (good state). State is represented by array of integers
about the size 8 by 8, which maps the current state of the board. The
possible values of the array are presented below:

* 0 - Empty field
* 1/-1 - Pawn
* 2/-2 - Knight
* 3/-3 - Bishop
* 4/-4 - Rook
* 5/-5 - Queen
* 6/-6 - King

**Black piece value / White piece value - Name of the piece**

#### 2. Learning strategy

**Encountered challenges**

Everyone who ever played chess know that this game is quite complex.
Observation of short-term effects of given move is not enough to state
if this move was good or bad. One mistake can cause that we'll lose our
chances to win the game, but the game will end after moves. One of
possible solutions of this problem is rating our moves only after
the game. This solution has, however, some drawback. We can do a lot of
good moves, and finally lose the game, because our opponent was to strong
for us. We can also make a lot of stupid moves, and win the game because
our opponent played very poorly. In both cases we'll rate our decisions
not properly.

**How did I solve it?**

I decided to rate decision taken by algorithm after execution of next
four moves. After execution of the move, it is inserted into special list.
The final rating is calculated based on events which took place on board.
For example if I destroy enemy's piece move's rank is incremented otherwise is
decremented. Final rating of the move is equal sum of old rating (given by neural network) and rank value (sum of
all rewards and penalties from events) divided by 100. Possible rewards or
penalties:

* Loss or clashing a piece - squared piece value from first point (multiplied by -1 if loss)
* Check - 10/-10
* Draw - 30/-30
* Checkmate - 100/-100

### Used libraries

In this project I have used following machine learning libraries:

* Keras
* Tensorflow

Web serwer was created in Flask.

In this project I use Neural Network to