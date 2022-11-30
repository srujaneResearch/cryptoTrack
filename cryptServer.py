#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:29:45 2022

@author: soul
"""
etherscan = "https://etherscan.io/address/"

import cryptotrack as ct
import requests
cryp = "5421348805:AAH1WT8c4baviLO-E5m7P1nmIqNFUYYRExI" # This is the API KEY for bot
ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
telegram_url = 'https://api.telegram.org/bot'+cryp

import sqlite3 as sq
import os
dfile = os.path.join(os.path.expanduser('~'),'Desktop','cryptoTrack','cryptoTrack.db')

#dfile='cryptoTrack.db'
sqliteConnection = sq.connect(dfile)
cursor = sqliteConnection.cursor()
data = cursor.execute("select * from user").fetchall()
for i in data:
    #print(i)
    try:
        if i[3] != None:
            k = ct.getlatestTransaction(i[2],i[3], ct.ctrack,ct.acc)
        else:
            k = ct.getlatestTransaction(i[2],0, ct.ctrack,ct.acc)
        #print(k)
        cursor.execute("update user set last_hash='{0}',last_block_mined='{1}' where wallet='{2}'".format(k[0]['hash'],k[0]['blockNumber'],i[2]))
        sqliteConnection.commit()
        #data.iloc[i][-1] = k[0]['blockNumber']
        if i[3] != None:
            print("Working For",i[1])
            for j in k:
                msg=''
                
                #time.sleep(30)
                
                if j['hash'] != i[4]:
                    t = "<a href='{0}'>{1}</a>".format(etherscan.split('address')[0]+"tx/"+j['hash'],'0x'+j['hash'].split('0x')[1].upper())
                    msg+="Latest Transaction\n"+t+"\nFrom"
                    if j['from'] == i[2]:
                        msg+=" <b>(Your Wallet):</b>\n"+ "<a href='{0}'>{1}</a>".format(ct.etherscan+j['from'],'0x'+j['from'].split('0x')[1].upper())+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['from'],'0x'+j['from'].split('0x')[1].upper())
                        msg+=":\n"+link+"\n"
                    if j['to'] == i[2]:
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['to'],'0x'+j['to'].split('0x')[1].upper())
                        msg+="To<b>(Your Wallet)</b>:\n"+link+"\n"
                    else:
                        link = "<a href='{0}'>{1}</a>".format(etherscan+j['to'],'0x'+j['to'].split('0x')[1].upper())
                        msg+="To:\n"+link+"\n"
                    if 'transfer' in j['functionName']:
                            
                        contract,value = ct.getTransactionLog(j['hash'])
                        #value = '{:.18f}'.format(value)
                        abi = ct.getABI(contract,ct.ctrack,ct.acc)
                        symbol,decimal = ct.getSymbol(contract, abi, ct.ethend)    
                        msg+="<b><em>Token transfer: {0:.6f} {1}</em></b>".format(value/10**decimal,symbol)
                    else:
                        try:
                            contract,value = ct.getTransactionLog(j['hash'])
                            #value = '{:.18f}'.format(value)
                            abi = ct.getABI(contract,ct.ctrack,ct.acc)
                            symbol,decimal = ct.getSymbol(contract, abi, ct.ethend)    
                            msg+="<b><em>Token transfer: {0:.6f} {1}</em></b>".format(value/10**decimal,symbol)
                        except:
                            value = '{:.6f}'.format(float(j['value'])/10**18).rstrip()
                            
                            msg+="<b><em>Ether transfer: {0} </em></b>".format(value)
                    
                    tele=requests.get(telegram_url+"/sendMessage",params={"chat_id":i[0],
                                                                    "text":msg,
                                                                    "parse_mode":"HTML",
                                                                    "disable_web_page_preview":"True"
                                                                    
                                                                    })
                    print(tele)
                    
                else:
                    break
    except:
        print("Invalid address",i[2])
    
cursor.close()
sqliteConnection.close()