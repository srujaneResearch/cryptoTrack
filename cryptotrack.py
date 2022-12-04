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
ankerPremium="110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"

anker = "https://rpc.ankr.com/multichain"
econtract = "https://api.etherscan.io/api?module=contract"
ethend = "https://rpc.ankr.com/eth/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"
avalancheend = "https://rpc.ankr.com/avalanche/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"
bscendpoint = "https://rpc.ankr.com/bsc/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"
fantomendpoint="https://rpc.ankr.com/fantom/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"
trxendpoint = "https://rpc.ankr.com/premium-http/tron/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"

trxTrnsactionInfo = "https://rpc.ankr.com/premium-http/tron/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2/wallet/gettransactionbyid"


a="https://rpc.ankr.com/multichain/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"

def getSymbol(contract,abi,endpoint):
    from web3 import Web3
    url=endpoint
    web3 = Web3(Web3.HTTPProvider(url))
    contract = web3.toChecksumAddress(contract)
    c = web3.eth.contract(contract,abi=abi)
    return c.functions.symbol().call(),c.functions.decimals().call()


def getABI(contract,ctrack,capi):
    txlist = {"action":"getabi",
              "address":contract,
              "apikey":ctrack
              }
    capi = capi.split('?module')[0]+"?module=contract"
    k = requests.get(capi,params=txlist)
    r = k.json()['result']
    return r


def getMultBTC(address):
    api = "https://blockchain.info/multiaddr?active={0}".format(address)
    l = requests.get(api)

def getlatestTransactionBTC(address):
    api = "https://blockchain.info/rawaddr/{0}".format(address)

    l = requests.get(api)

    return l.json()['txs']



def getBalanceBTC(address):
    api = "https://blockchain.info/balance?active={0}".format(address)
    l = requests.get(api)
    return l.json()[address]['final_balance']/100000000
def getTransactionLogTRX(txhash):
    para = {
        "value":txhash
    }
    
    trxTrnsactionInfo = "https://rpc.ankr.com/premium-http/tron/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2/wallet/gettransactionbyid"

    
    k = requests.post(trxTrnsactionInfo,data=json.dumps(para))
    contract = k.json()['raw_data']['contract'][0]['parameter']['value']['contract_address']
    value = k.json()['raw_data']['contract'][0]['parameter']['value']['data']


def getTransactionLog(txhash):
    para = {
    "jsonrpc": "2.0",
    "method": "ankr_getTransactionsByHash",
    "params": {
        "transactionHash": txhash,
        "decodeLogs": True,
        "decodeTxData": True
    },
    "id": 1
    }
    headers={'Content-Type': 'application/json',
             
             }
    
    end = "https://rpc.ankr.com/multichain"
    
    k = requests.post(end,headers=headers,data=json.dumps(para))
    check = k.json()['result']['transactions']
    contract = check[0]['logs'][0]['address']
    value = float(check[0]['logs'][0]['event']['inputs'][-1]['valueDecoded'])
    return contract,value

def getBalances(address,blockchain):
    para = {"jsonrpc": "2.0",
            "method": "ankr_getAccountBalance",
            "params": {
                "blockchain": blockchain,
                "walletAddress": address
                },
            "id": 1}
    headers={'Content-Type': 'application/json',
             'X-API-KEY': ankerPremium
             }
    k = requests.post(anker, headers=headers, data=json.dumps(para))
    r = k.json()['result']['assets']
    
    return r
    

def getlatestTransaction(address,block,ctrack,acc):
    txlist = {"action":"txlist",
              "address":address,
              "startblock":block,
              "page":"1",
              "offset":"20",
              "sort":"desc",
              "apikey":ctrack
              }

    k = requests.get(acc,params=txlist)
    r = k.json()['result']
    return r

def getlatestTransactionTRX(address):
    trxscan = "https://apilist.tronscan.org/api/transaction"
    params = {"address":address}
    k = requests.get(trxscan,params=params)
    r = k.json()['data']
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