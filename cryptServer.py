#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:29:45 2022

@author: soul
"""
etherscan = "https://etherscan.io/address/"

import cryptotrack as ct
import requests
cryp = "5730421955:AAF_pJBJcfrWiDV4M0Pfa_w1k5WfunLecnU" # This is the API KEY for bot
ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
telegram_url = 'https://api.telegram.org/bot'+cryp

import sqlite3 as sq
import os
dfile = os.path.join(os.path.expanduser('~'),'Desktop','cryptoTrack','cryptoTrack.db')

dfile='cryptoTrack.db'
sqliteConnection = sq.connect(dfile)
cursor = sqliteConnection.cursor()
data = cursor.execute("select * from user").fetchall()
for i in data:
    #print(i)
    try:
        k = ct.getlatestTransaction(i[2],0, ct.ctrack,ct.acc)
        print(k)
        cursor.execute("update user set last_hash='{0}',last_block_mined='{1}' where wallet='{2}'".format(k[0]['hash'],k[0]['blockNumber'],i[2]))
        sqliteConnection.commit()
        #data.iloc[i][-1] = k[0]['blockNumber']
        if i[3] != None:
            print("Working For",i[1])
            for j in k:
                msg=''
                print(j['hash'],i[4])
                #time.sleep(30)
                
                if j['hash'] != i[4]:
                    print("True")
                    msg+="Latest Transaction\n"+str(i[2]).upper()+"\nFrom"
                    if j['from'] == str(i[2]):
                        msg+=" <b>(Your Wallet):</b>\n"+ "<a href='{0}'>{1}</a>".format(ct.etherscan+j['from'],j['from'].upper())+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['from'],j['from'].upper())
                        msg+=":\n"+link+"\n"
                    if j['to'] == str(i[2]):
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['to'],j['to'].upper())
                        msg+="To<b>(Your Wallet)</b>:\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['to'],j['to'].upper())
                        msg+="To:\n"+link+"\n"
                    if 'transfer' in j['functionName']:
                            
                        contract,value = ct.getTransactionLog(j['hash'])
                        abi = ct.getABI(contract,ct.ctrack,ct.acc)
                        symbol = ct.getSymbol(contract, abi, ct.ethend)    
                        msg+="<i>Token transfer: {0} {1}</i>".format(value,symbol)
                    else:    
                        msg+="Ether transfer: {:.18f}".format(float(j['value'])/10**18)
                    
                    tele=requests.get(telegram_url+"/sendMessage",params={"chat_id":i[0],
                                                                    "text":msg,
                                                                    "parse_mode":"HTML"
                                                                    })
                    
                    print(tele.json())
                        
                    print("message sent")                
                else:
                    break
    except:
        print("Invalid address",i[2])
    
cursor.close()
sqliteConnection.close()