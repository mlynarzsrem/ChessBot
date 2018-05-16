import sqlite3
from sqlite3 import Error

class DBase():
    def createConnection(self,dbaseLoc):
        try:
            self.conn =sqlite3.connect(dbaseLoc)
            self.conn.isolation_level =None
        except Error as e:
            print(e)
    def createTables(self):
        sql_create_moves_table="""CREATE TABLE IF NOT EXISTS moves(
        state varchar PRIMARY KEY,
        nextmoves VARCHAR NOT NULL 
        );"""
        try:
            c =self.conn.cursor()
            c.execute(sql_create_moves_table)
        except Error as e:
            print(e)
    def getMovesInState(self,state):
        c =self.conn.cursor()
        c.execute("Select nextmoves from moves WHERE state=?",(state,))
        rows =c.fetchall()
        return rows
    def insertMoves(self,state,nextmoves):
        c =self.conn.cursor()
        c.execute("insert into moves VALUES (?,?)",(state,nextmoves,))
        c.execute("VACUUM")
        self.conn.commit()
    def updateMoves(self,state,nextmoves):
        c =self.conn.cursor()
        c.execute("update moves set nextmoves =? where state=?",(nextmoves,state,))
        c.execute("VACUUM")
        self.conn.commit()
    def __init__(self,dbaseLoc="qlearn2.db"):
        self.createConnection(dbaseLoc)
        self.createTables()
