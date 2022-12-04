#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:29:45 2022

@author: soul
"""
import cryptotrack as ct
import requests
cryp = "5447226008:AAFxsOFQvj7sbgI0cDiDzGuju00aIjcgUCE" # This is the API KEY for bot
ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
telegram_url = 'https://api.telegram.org/bot'+cryp
import sqlite3 as sq
import os
dfile = os.path.join(os.path.expanduser('~'),'Desktop','cryptoTrack','cryptoTrack.db')

btcscan = "https://www.blockchain.com/btc/address/"

import mysql.connector
  
sqliteConnection = mysql.connector.connect(host ="sql9.freemysqlhosting.net",user ="sql9581771",passwd ="F31X7VSfUT",   database = "sql9581771")
cursor = sqliteConnection.cursor()
data = cursor.execute("select * from user")
data = cursor.fetchall()

for i in data:

    if len(i[2])==34:
        try:
            
            if i[-4] != None: #block
                k = ct.getlatestTransactionBTC(i[2])
            else:
                k = ct.getlatestTransactionBTC(i[2])
            #print(k)
            cursor.execute("update user set btc_l_tx='{0}',btc_l_block='{1}' where wallet='{2}'".format(k[0]['hash'],k[0]['block_index'],i[2]))
            sqliteConnection.commit()
            #data.iloc[i][-1] = k[0]['blockNumber']
            
            if i[-3] != None: #hash
                print("Working For",i[1])
                
                for j in k:
                    msg=''
                    #print(j['hash'],i[11])
                    #time.sleep(30)
                    
                    if j['hash'] != i[-3]:
                        t = "<a href='{0}'>{1}</a>".format(btcscan.split('address/')[1]+"/tx/"+j['hash'],j['hash'].upper())
                        msg+="Latest Transaction\n"+t+"\nFrom:\n"



                        for _ in j['inputs']:
                            msg+=_['prev_out']['addr']+"\n"
                            msg+=str(_['value']/100000000)+"BTC"
                            msg+='\n'

                        msg+='\n\n'
                        msg+='To:\n'

                        for _ in j['out']:
                            msg+=_['addr']+"\n"
                            msg+=str(_['value']/100000000)+"BTC"
                            msg+='\n'

                        msg+='\n\n'

                        msg+='Amount: '+str(j['result']/100000000)+"BTC"

                        tele=requests.get(telegram_url+"/sendMessage",params={"chat_id":i[0],
                                                                        "text":msg,
                                                                        "parse_mode":"HTML",
                                                                        "disable_web_page_preview":"True"
                                                                        })
                        
                        #print(tele.json())
                            
                        #print("message sent")                
                    else:
                        break
        except:
            print("Invalid address",i)
        
    cursor.close()
    sqliteConnection.close()
#[print(x[4]) for x in data]
        
        
    
    
    
    
    

"""
start = time.time()
for i in data.index:
    print(data['username'][i])
    
    print(ct.getlatestTransaction(str(data['wallet'][i]), str(data['last_block_mine'][i]), ctrack))
end = time.time()
""" 
#print("time",end-start)
#asyncio.run(main())
