class View:
    def __init__(self):
        self.begin = open("static/site/begin.txt",'r').read()
        self.end = open("static/site/end.txt",'r').read()
        self.imgDecBeg ="{{ url_for('static', filename='img/"
        self.imgDecEnd= ".png') }}"

    def buildURLgetMoves(self,x,y):
        return "{{ url_for('get_Moves',position="+'9'+str(x)+str(y)+")}}"
    def buildURLmakeMove(self,x1,y1,x2,y2):
        return "{{ url_for('make_Move',move="+'9'+str(x1)+str(y1)+str(x2)+str(y2)+")}}"
    def getImgUrl(self,char,value):
        return self.imgDecBeg+char+str(abs(value))+self.imgDecEnd
    def getMoveHtml(self,x,y,color,char,value,active=''):
        return '<a href="'+self.buildURLgetMoves(x,y)+'"><div class ="field_' + color + active+'"><img src="'+self.getImgUrl(char,value)+'" width="80px" ></div></a>'
    def getCPUHtml(self,color,char,value):
        return '<div class ="field_' + color + '"><img src="'+self.getImgUrl(char,value)+'" width="80px" ></div>'
    def getEmpty(self,color):
        return '<div class ="field_'+color+'"></div>'
    def getCurrentBoard(self,board):
        html=''
        for x in range(8):
            for y in range(8):
                value = board[x,y]
                if((x +y) % 2==0):#White
                    color ='white'
                else:
                    color='black'
                if(value==0):#empty field
                    html +=self.getEmpty(color)
                if (value > 0): #cpu
                    html += self.getCPUHtml(color,'b',value)
                if (value < 0): #player
                    html += self.getMoveHtml(x,y,color,'w',value,active='')
            html+='<div style="clear: both"></div>'
        return self.begin+html+self.end
    def getMoves(self,board,r,c):
        if(board.board[r,c] is None or  board.board[r,c].getId()>0):
            return self.getCurrentBoard(board.getIntBoard())
        html = ''
        moveList = board.getValidCheckStateMoves(CPU=False)
        moveList = [(m[2],m[3]) for m in moveList if m[0]==r and m[1]==c]
        print(moveList)
        intBoard =board.getIntBoard()
        for x in range(8):
            for y in range(8):
                value = intBoard[x,y]
                if((x +y) % 2==0):#White
                    color ='white'
                else:
                    color='black'
                if(x==r and y==c):
                    html += self.getMoveHtml(x,y,color,'w',value,active='_active')
                    continue
                if((x,y) in moveList):
                    if (value == 0):  # empty field
                        html += '<a href="'+self.buildURLmakeMove(r,c,x,y)+'"><div class ="field_' + color + '_toclick"></div></a>'
                    if (value > 0):  # cpu
                        html += '<a href="'+self.buildURLmakeMove(r,c,x,y)+'"><div class ="field_' + color + '_toclick"><img src="'+self.getImgUrl('b',value)+'" width="80px" ></div></a>'
                    continue
                if(value==0):#empty field
                    html +=self.getEmpty(color)
                if (value > 0): #cpu
                    html += self.getCPUHtml(color,'b',value)
                if (value < 0): #player
                    html += self.getMoveHtml(x,y,color,'w',value,active='')
            html+='<div style="clear: both"></div>'
        return self.begin+html+self.end