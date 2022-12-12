#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 00:10:13 2022

@author: soul
"""

#!/usr/bin/env python3
#satchit
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
avascan='https://snowtrace.io/address/'


import mysql.connector
  
sqliteConnection = mysql.connector.connect(host ="172.107.32.113",port="10003",user ="admin",passwd ="agz8BRE0",database = "blockalert")  

cursor = sqliteConnection.cursor()
data = cursor.execute("select * from user")
data = cursor.fetchall()

for i in data:
    #print(i)
    try:
        if i[8] != None:
            
            k = ct.getlatestTransaction(i[2],i[8],ct.avatrack,ct.avaacc)
        else:
            k = ct.getlatestTransaction(i[2],0,ct.avatrack,ct.avaacc)
            
        #print(k)
        cursor.execute("update user set ava_l_tx='{0}',ava_l_block='{1}' where wallet='{2}'".format(k[0]['hash'],k[0]['blockNumber'],i[2]))
        sqliteConnection.commit()
        #data.iloc[i][-1] = k[0]['blockNumber']
        
        if i[8] != None:
            print("Working For",i[1])
            
            for j in k:
                msg=''
                #print(j['hash'],i[9])
                #time.sleep(30)
                
                if j['hash'] != i[9]:
                    t = "<a href='{0}'>{1}</a>".format(avascan.split('address')[0]+"tx/"+j['hash'],'0x'+j['hash'].split('0x')[1].upper())
                    msg+="Latest Transaction\n"+t+"\nFrom"
                    if j['from'] == str(i[2]):
                        link = "<a href='{0}'>{1}</a>".format(avascan+j['from'],'0x'+j['from'].split('0x')[1].upper())
                        msg+=" <b>(Your Wallet):</b>\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(avascan+j['from'],'0x'+j['from'].split('0x')[1].upper())
                        msg+=":\n"+link+"\n"
                    if j['to'] == str(i[2]):
                        link = "<a href='{0}'>{1}</a>".format(avascan+j['to'],'0x'+j['to'].split('0x')[1].upper())
                        msg+="To<b>(Your Wallet)</b>:\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(avascan+j['to'],'0x'+j['to'].split('0x')[1].upper())
                        msg+="To:\n"+'0x'+j['to'].split('0x')[1].upper()+"\n"
                        
                    if 'transfer' in j['functionName']:
                            
                        contract,value = ct.getTransactionLog(j['hash'])
                        abi = ct.getABI(contract,ct.avatrack,ct.avaacc)
                        symbol,decimal = ct.getSymbol(contract, abi, ct.avalancheend)    
                        msg+="<b><i>Token transfer: {0:.6f} {1}</i></b>".format(value/10**decimal,symbol)
                    else:    
                        try:
                            contract,value = ct.getTransactionLog(j['hash'])
                            abi = ct.getABI(contract,ct.avatrack,ct.avaacc)
                            symbol,decimal = ct.getSymbol(contract, abi, ct.avalancheend)    
                            msg+="<b><i>Token transfer: {0:.6f} {1}</i></b>".format(value/10**decimal,symbol)
                        except:
                            value = '{:.6f}'.format(float(j['value'])/10**18).rstrip()
                            
                            msg+="<b><em>AVA transfer: {0} </em></b>".format(value)
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
[print(x[4]) for x in data]
        
        
    
    
    
    
    

"""
start = time.time()
for i in data.index:
    print(data['username'][i])
    
    print(ct.getlatestTransaction(str(data['wallet'][i]), str(data['last_block_mine'][i]), ctrack))
end = time.time()
""" 
#print("time",end-start)
#asyncio.run(main())
