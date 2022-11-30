import sqlite3 as sq
import mysql.connector
  
conn = mysql.connector.connect(host ="sql9.freemysqlhosting.net",user ="sql9581771",passwd ="F31X7VSfUT",   database = "sql9581771")
curs = conn.cursor()

def executeQuery(query,comt=None):

# preparing a cursor object
    
  
    if comt != None:
        curs.execute(query)
        conn.commit()
        print("commited")
        #conn.close()
        
    else:
        curs.execute(query)
        #k = cur.fetchall()
        #conn.close()
        return k


l = "select * from user"

sql = sq.Connection('cryptoTrack.db')

cur = sql.cursor()


k = cur.execute(l)
k = k.fetchall()

j = 1
for i in k:
    executeQuery("insert into users (userid,username,wallet,last_block_mined,last_hash,wallet_name,bsc_l_block,bsc_l_tx,ava_l_block,ava_l_tx,poly_l_block,poly_l_tx,ftm_l_block,ftm_l_tx) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13]),"commit")
    print("commit",j)
    j+=1

conn.commit()