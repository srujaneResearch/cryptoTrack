#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 00:12:08 2022

@author: soul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 00:10:13 2022

@author: soul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:29:45 2022

@author: soul
"""
import cryptotrack as ct
import requests
cryp = "5730421955:AAF_pJBJcfrWiDV4M0Pfa_w1k5WfunLecnU" # This is the API KEY for bot
ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
telegram_url = 'https://api.telegram.org/bot'+cryp
import sqlite3 as sq
import os
dfile = os.path.join(os.path.expanduser('~'),'Desktop','cryptoTrack','cryptoTrack.db')
ftmscan='https://ftmscan.com/address/'


sqliteConnection = sq.connect(dfile)
cursor = sqliteConnection.cursor()
data = cursor.execute("select * from user").fetchall()
for i in data:
    #print(i)
    try:
        k = ct.getlatestTransaction(i[2],0,ct.ftmtrack,ct.ftmacc)
        #print(k)
        cursor.execute("update user set ftm_l_tx='{0}',ftm_l_block='{1}' where wallet='{2}'".format(k[0]['hash'],k[0]['blockNumber'],i[2]))
        sqliteConnection.commit()
        #data.iloc[i][-1] = k[0]['blockNumber']
        
        if i[-2] != None:
            #print("Working For",i[1])
            
            for j in k:
                msg=''
                #print(j['hash'],i[-1])
                #time.sleep(30)
                
                if j['hash'] != i[-1]:
                    t = "<a href={0}>{1}</a>".format(ftmscan.split('address')[0]+"tx/"+j['hash'],j['hash'].upper())
                    msg+="Latest Transaction\n"+t+"\nFrom"
                    if j['from'] == i[2]:
                        link = "<a href='{0}'>{1}</a>".format(ftmscan+j['from'],j['from'].upper())
                        msg+=" <b>(Your Wallet):</b>\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(ftmscan+j['from'],j['from'].upper())
                        msg+=":\n"+link+"\n"
                    if j['to'] == str(i[2]):
                        link = "<a href='{0}'>{1}</a>".format(ftmscan+j['to'],j['to'].upper())
                        msg+="To<b>(Your Wallet)</b>:\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(ftmscan+j['to'],j['to'].upper())
                        msg+="To:\n"+j['to'].upper()+"\n"
                    if 'transfer' in j['functionName']:
                            
                        contract,value = ct.getTransactionLog(j['hash'])
                        abi = ct.getABI(contract,ct.avatrack,ct.avaacc)
                        symbol = ct.getSymbol(contract, abi, ct.avalancheend)    
                        msg+="<i>Token transfer: {0} {1}</i>".format(value,symbol)
                    else:    
                        msg+="FTM transfer: {:.18f}".format(float(j['value'])/10**18)
                    
                    tele=requests.get(telegram_url+"/sendMessage",params={"chat_id":i[0],
                                                                    "text":msg,
                                                                    "parse_mode":"HTML"
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
