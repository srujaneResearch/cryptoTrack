#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 16:55:08 2022

@author: soul
"""

ctrack = "TKXCYFK7SYWXWSN1CIWGSB16DHI33181M3" # This is etherscan api key
import json
import requests
acc = "https://api.etherscan.io/api?module=account"
test = "https://api-ropsten.etherscan.io/api?module=account"
erc20 = "https://api-rinkeby.etherscan.io/api?module=account"
bsctrack = "2C14SU4GV6ZYX4W17FY7SU71HPXUIKTFWY"
polytrack = "2UM16KM5WP8JYCRIEVUC46A4DNH7FATN9E"
avatrack="NWFSTFZ17R62NKVPV27CQPX33DNNK3QY8C"
ftmtrack = "8FDGZFWBRVWCI8NCF58FTIQIVGXPX5RAGG"
bscacc="https://api.bscscan.com/api?module=account"
polyacc="https://api.polygonscan.com/api?module=account"
avaacc="https://api.snowtrace.io/api?module=account"
ftmacc="https://api.ftmscan.com/api?module=account"
anker = "https://rpc.ankr.com/multichain"

def getBalances(address,blockchain):
    para = {"jsonrpc": "2.0",
            "method": "ankr_getAccountBalance",
            "params": {
                "blockchain": blockchain,
                "walletAddress": address
                },
            "id": 1}
    headers={'Content-Type': 'application/json',
             'X-API-KEY':'22e282df02e47a6dc906c48db9830304e93e9f12bb74a179152c747c01d4e7b7'
             }
    k = requests.post(anker, headers=headers, data=json.dumps(para))
    r = k.json()['result']['assets']
    
    return r
    

def getlatestTransaction(address,block,ctrack,acc):
    txlist = {"action":"txlist",
              "address":address,
              "startblock":block,
              "sort":"desc",
              "apikey":ctrack
              }

    k = requests.get(acc,params=txlist)
    r = k.json()['result']
    return r

def test(address,block,ctrack):
    txlist = {"action":"txlist",
              "address":address,
              "startblock":block,
              "sort":"desc",
              "apikey":ctrack
              }

    k = requests.get(test,params=txlist)
    r = k.json()['result']
    return r