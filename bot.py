#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 16:28:16 2022
@author: soul
"""
import sqlite3 as sq
import datetime
from telegram.ext.updater import Updater
from telegram import *
from telegram.ext import *
import json
import csv
import pandas as pd
import cryptotrack as ct
import re
import math
etherscan = "https://etherscan.io/address/"
bscscan='https://bscscan.com/address/'
avascan='https://snowtrace.io/address/'
polyscan='https://polygonscan.com/address/'
ftmscan='https://ftmscan.com/address/'
blockchain = ['eth','bsc','avalanche','polygon','fantom']



startmsg = """
Welcome {0}
I’ll will track all transactions from your
     Ethereum wallet
     Binance Wallet
     Avalanche Wallet
     Polygon Wallet
     Fantom Wallet
and notify you immediately!
Bot will NEVER ask you for your PRIVATE KEYS. Always type ONLY PUBLIC KEYS.
By tracking your transactions, be the first to know when: 
    1) you get any tokens from ICO 
    2) you get Airdropped tokens 
    3) hackers trying to drain your wallet
To start tracking your wallet’s transactions send me your ETH or BTC wallet addresses (you can send several addresses separated by comma in one message):
"""
cryp = "5447226008:AAFxsOFQvj7sbgI0cDiDzGuju00aIjcgUCE" # This is the API KEY for bot
ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
telegram_url = 'https://api.telegram.org/bot'+cryp
buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
           [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
          ]

def start(update: Update, context: CallbackContext):
    """ This function is for command /start"""
    #context.user_data.clear()
    sqliteConnection = sq.connect('cryptoTrack.db')
    cursor = sqliteConnection.cursor()
    buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
               [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
               ]
    user = str(update.effective_chat.id)
    u = cursor.execute("select userid from user where userid='{0}'".format(user)).fetchall()
    if len(u) == 0: 
        update.effective_chat.send_message(text=startmsg.format(update.effective_chat.username),reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
        update.effective_chat.send_message(text="Please send you ethereum public address")
        context.user_data['point'] = 'getAddress'
        cursor.close()
        sqliteConnection.close()
    else:
        wallets = [x[0] for x in cursor.execute("select wallet from user where userid='{0}'".format(user)).fetchall()]
        msg=''
        for x in wallets:
            msg+='0x'+x.split('0x')[1].upper()+"\n"
        
        update.effective_chat.send_message("<b>Tracked Wallets:</b>\n{0}".format(msg),parse_mode=ParseMode.HTML,disable_web_page_preview=True,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
        cursor.close()
        sqliteConnection.close() 
        

def msgHandler(update: Update, context: CallbackContext):
    """This function handels states of logic tree flows"""
    
    print(context.user_data)
    print(update.message.text)        
            
            
            
    if "Add New Wallet" in update.message.text:
        context.user_data.clear()
        context.user_data['point']='getAddress'
        update.effective_chat.send_message("send your ETH/BSC/POLY/AVA/FANTOM wallet address")
        return
    elif "Delete Old Wallet" in update.message.text:
        context.user_data.clear()
        sqliteConnection = sq.connect('cryptoTrack.db')
        cursor = sqliteConnection.cursor()
        buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                   [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                   ]
        user = str(update.effective_chat.id)
        u = cursor.execute("select userid from user where userid='{0}'".format(user)).fetchall()
        if len(u) == 0: 
            update.effective_chat.send_message(text=startmsg.format(update.effective_chat.username),reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
            update.effective_chat.send_message(text="Please send you ethereum public address")
            context.user_data['point'] = 'getAddress'
            cursor.close()
            sqliteConnection.close()
            return
        else:
            data = cursor.execute("select wallet from user where userid='{0}'".format(user)).fetchall()
            msg=''
            for i in range(1,len(data)+1):
                msg+="{0})\n{1}\n".format(i,'0x'+data[i-1][0].split('0x')[1].upper())
            
            msg+="\n\n Send me the number of wallet or wallet address to delete"
            update.effective_chat.send_message(msg,parse_mode=ParseMode.HTML)
            context.user_data['point']='deleteWallet'
            return
    elif "Check All Wallets" in update.message.text:
        context.user_data.clear()
        sqliteConnection = sq.connect('cryptoTrack.db')
        cursor = sqliteConnection.cursor()
        buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                   [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                   ]
        user = str(update.effective_chat.id)
        u = cursor.execute("select userid from user where userid='{0}'".format(user)).fetchall()
        if len(u) == 0:
            update.effective_chat.send_message(text=startmsg.format(update.effective_chat.username),reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
            update.effective_chat.send_message(text="Please send you ethereum public address")
            context.user_data['point'] = 'getAddress'
            cursor.close()
            sqliteConnection.close()
            return
        else:
            wallets = cursor.execute("select wallet,wallet_name,last_block_mined,bsc_l_block,ava_l_block,poly_l_block,ftm_l_block from user where userid='{0}'".format(user)).fetchall()
            msg=''
            for x in wallets:
                if x[2]:
                    link = "<a href='{0}'>{1} (ETH)</a>"
                    msg+=link.format(etherscan+x[0],"0x"+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                if x[3]:
                    link = "<a href='{0}'>{1} (BSC)</a>"
                    msg+=link.format(bscscan+x[0],'0x'+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                    
                if x[4]:
                    link = "<a href='{0}'>{1} (AVA)</a>"
                    msg+=link.format(avascan+x[0],'0x'+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                if x[5]:
                    link = "<a href='{0}'>{1} (MATIC)</a>"
                    msg+=link.format(polyscan+x[0],'0x'+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                if x[6]:
                    link = "<a href='{0}'>{1} (FTM)</a>"
                    msg+=link.format(ftmscan+x[0],'0x'+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                if not x[2]:
                    link = "<a href=''>{0}</a>"
                    msg+=link.format('0x'+x[0].split('0x')[1].upper())+" "+"<b>"+x[1]+"</b>"+"\n\n"
                    
            
            update.effective_chat.send_message("<b>Tracked Wallets:</b>\n{0}".format(msg),parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            cursor.close()
            sqliteConnection.close()
            return
    elif "Name A Wallet" in update.message.text:
        context.user_data.clear()
        sqliteConnection = sq.connect('cryptoTrack.db')
        cursor = sqliteConnection.cursor()
        buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                   [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                   ]
        user = str(update.effective_chat.id)
        u = cursor.execute("select userid from user where userid='{0}'".format(user)).fetchall()
        if len(u) == 0: 
            update.effective_chat.send_message(text=startmsg.format(update.effective_chat.username),reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
            update.effective_chat.send_message(text="Please send you ethereum public address")
            context.user_data['point'] = 'getAddress'
            cursor.close()
            sqliteConnection.close()
            return
        else:
            data = cursor.execute("select wallet,wallet_name from user where userid='{0}'".format(user)).fetchall()
            msg=''
            for i in range(1,len(data)+1):
                msg+="{0})\n{1} <b>{2}</b>\n".format(i,'0x'+data[i-1][0].split('0x')[1].upper(),data[i-1][1])
            
            msg+="\n\n Send me the number of wallet and desired name (example 1 my_first_wallet)"
            update.effective_chat.send_message(msg,parse_mode=ParseMode.HTML)
            context.user_data['point']='walletName'
            return
    elif "Check All Balances" in update.message.text:   
        context.user_data.clear()
        sqliteConnection = sq.connect('cryptoTrack.db')
        cursor = sqliteConnection.cursor()
        buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                   [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                   ]
        user = str(update.effective_chat.id)
        u = cursor.execute("select userid from user where userid='{0}'".format(user)).fetchall()
        if len(u) == 0: 
            update.effective_chat.send_message(text=startmsg.format(update.effective_chat.username),reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
            update.effective_chat.send_message(text="Please send you ethereum public address")
            context.user_data['point'] = 'getAddress'
            cursor.close()
            sqliteConnection.close()
            return
        else:
            wallets = cursor.execute("select wallet,wallet_name from user where userid='{0}'".format(user)).fetchall()

            #wallets = ','.join([x for x in wallets])
            print(wallets)
            msg=''
            for wallet in wallets:
                msg+='0x'+wallet[0].split('0x')[1].upper()+" "+"<b>"+wallet[1]+"</b>"+"\n"
                
                for b in blockchain:
                    f=0
                
                    try:
                        assets = ct.getBalances(wallet[0],b)
                        if len(assets) != 0:
                            f=1
                            msg+="<b>{0}</b>\n\n".format(b.upper())
                            msg+='0x'+wallet[0].split('0x')[1].upper()+" <b>({0})</b>".format(b.upper())+"\n"
                            for _ in assets:
                                msg+=_['balance']+" "+_['tokenSymbol']+"\n"
                    except:
                        print("Error in balance")
                        continue
                    if f==1:
                        msg+="<b>---------------------------</b>\n\n"
            if len(msg)>=4096:
                
                for i in range(1,math.ceil(len(msg)/4096)+1):
                    update.effective_chat.send_message(text=msg[(4096*i)-4096:4096*i],parse_mode=ParseMode.HTML,disable_web_page_preview=True)
                return
                #update.effective_chat.send_message(text=msg[4096:],parse_mode=ParseMode.HTML)
            else:
                update.effective_chat.send_message(text=msg,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            cursor.close()
            sqliteConnection.close()
            return

    if 'point' in context.user_data.keys():
        
        
        if context.user_data['point']=='startName':
            name = update.message.text
            wallet = context.user_data['wallet']
            sqliteConnection = sq.connect('cryptoTrack.db')
            cursor = sqliteConnection.cursor()
            
            for i in wallet:
                print(type(i))
                cursor.execute("update user set wallet_name='{0}' where wallet='{1}'".format(name,i))
                sqliteConnection.commit()
            
            update.effective_chat.send_message("Wallet Name Updated!")
            context.user_data.clear()
            cursor.close()
            sqliteConnection.close()
            return
            
            
        
        elif context.user_data['point'] == 'getAddress':
            
            if len(update.message.text)==42 or ',' in update.message.text:
            
                buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                           [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                           ]
                address,user = update.message.text.split(','),str(update.effective_chat.id)
                sqliteConnection = sq.connect('cryptoTrack.db')
                cursor = sqliteConnection.cursor()
                
                wallets = cursor.execute("select wallet from user where userid='{0}'".format(user))
                wallets = wallets.fetchall()
                wallets = [x[0] for x in wallets]
                wt=0
                cm=[]
                msg=''
                for i in address:
                    if i in wallets:
                        update.effective_chat.send_message('This wallet is already in tracking, please send another wallet')
                    else:
                        wt+=1
                        username = update.effective_chat.username
                        latest_tx = ct.getlatestTransaction(address,0,ctrack,ct.acc)
                        print(latest_tx)
                        try:
                            if len(latest_tx)==0:
                                cursor.execute("insert into user (userid,username,wallet,wallet_name) values ('{0}','{1}','{2}','{3}')".format(user,username,i,' '))                    
                                sqliteConnection.commit()
                                msg+='0x'+i.split('0x')[1].upper()+"\n"
                                cm.append(i)
                            else:    
                                k = latest_tx[0]
                                print(k)
                                print(type(k))
                    
                    
                                cursor.execute("insert into user (userid,username,wallet,last_block_mined,last_hash,wallet_name) values ('{0}','{1}','{2}','{3}','{4}','{5}')".format(user,username,i,k['blockNumber'],k['hash'],' '))                    
                                sqliteConnection.commit()                    
                                msg+='0x'+i.split('0x')[1].upper()+"\n"
                                cm.append(i)
                        except:
                            update.effective_chat.send_message("Wrong Address Format, Try Again\n{0}".format(i))
                            
                cursor.close()
                sqliteConnection.close()
                if wt != 0:
                    msg='Okay the following wallet were added for tracking\n'+msg            
                    update.effective_chat.send_message(msg,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
                    context.user_data['point']='startName'
                    context.user_data['wallet'] = cm
                    update.effective_chat.send_message("Do you want to name the wallet? If yes, send me the name now. If you want to add the name later, just ignore the message")
                    return
                #context.user_data.clear()
            else:
                context.user_data.clear()
                return
        elif context.user_data['point']=='deleteWallet':
            sqliteConnection = sq.connect('cryptoTrack.db')
            cursor = sqliteConnection.cursor()
            buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                       [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                       ]
            user = str(update.effective_chat.id)
            msg = update.message.text
            
            if re.search(r"^(\d)$",msg):
                data = cursor.execute("select wallet,wallet_name from user where userid='{0}'".format(user)).fetchall()
                k = re.search(r"^(\d)$",msg).groups()
                wallet= data[int(k[0])-1][0]
                cursor.execute("delete from user where wallet='{0}'".format(wallet))
                sqliteConnection.commit()
                data = cursor.execute("select wallet,wallet_name from user where wallet='{0}'".format(wallet)).fetchall()
                txt="Wallet Successfully Deleted!"
                update.effective_chat.send_message(txt,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
                context.user_data.clear()
                cursor.close()
                sqliteConnection.close()
                return
            elif len(msg)==42:
                wallet = msg
                cursor.execute("delete from user where wallet='{0}'".format(wallet))
                sqliteConnection.commit()
                data = cursor.execute("select wallet,wallet_name from user where wallet='{0}'".format(wallet)).fetchall()
                txt="Wallet Successfully Deleted!"
                update.effective_chat.send_message(txt,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
                context.user_data.clear()
                cursor.close()
                sqliteConnection.close()     
                return
                                
            else:
                update.effective_chat.send_message("Wrong Format Try Again!",reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
                cursor.close()
                sqliteConnection.close()
                return
            
        elif context.user_data['point']=='walletName':
            sqliteConnection = sq.connect('cryptoTrack.db')
            cursor = sqliteConnection.cursor()
            buttons = [[KeyboardButton("Add New Wallet"),KeyboardButton("Delete Old Wallet"),KeyboardButton("Check All Wallets")],
                       [KeyboardButton("Name A Wallet"),KeyboardButton("Check All Balances")]
                       ]
            user = str(update.effective_chat.id)
            msg = update.message.text
            
            if re.search(r"(\d) (.*)",msg):
                data = cursor.execute("select wallet,wallet_name from user where userid='{0}'".format(user)).fetchall()
                k = re.search(r"(\d) (.*)",msg).groups()
                wallet,name = data[int(k[0])-1][0],k[1]
                cursor.execute("update user set wallet_name='{0}' where wallet='{1}'".format(name,wallet))
                sqliteConnection.commit()
                data = cursor.execute("select wallet,wallet_name from user where wallet='{0}'".format(wallet)).fetchall()
                txt="Wallet Name Changed\n"+'0x'+data[0][0].split('0x')[1].upper()+" "+data[0][1]
                update.effective_chat.send_message(txt,reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
                context.user_data.clear()
                cursor.close()
                sqliteConnection.close()
                return
            else:
                update.effective_chat.send_message("Wrong Format Try Again!")
                cursor.close()
                sqliteConnection.close()
                return
            

"""Below are the bot handelers, be careful while playing with those"""
application = Updater(cryp)
dispatcher = application.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters=Filters.text,callback=msgHandler))
application.start_polling()