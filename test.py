#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 17:28:31 2022

@author: soul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:11:54 2022

@author: soul
"""

tx="0x11019840d4545e40b7459ca465b794c0f0462d0c8f5cdef82c0fd54a946d02ef"

from web3 import Web3
url="https://rpc.ankr.com/eth/110f3788f48704c99c2f08ac88d56de0d2a1b0e3c769a85b9d8ce00d2d08f6d2"
web3 = Web3(Web3.HTTPProvider(url))
print(web3.eth.block_number)

print(web3.eth.getTransaction('0x1855d706041d8d660a329c46e7427d5a1ebb37275b9841784e4d5971d200ea53'))

y=web3.eth.getTransactionReceipt('0x11019840d4545e40b7459ca465b794c0f0462d0c8f5cdef82c0fd54a946d02ef')

data = "0x00000000000000000000000000000000000000000005ca4ec2a79a7f67000000"

transactions = []

for i in k:
    if 'transfer' in i['functionName']:
        transactions.append(i)
        
y = []

for i in transactions:
    k = web3.eth.getTransactionReceipt(i['hash'])
    y.append(k)
    

topics = y[0]['logs'][0]['topics']

d=topics[]

c = web3.eth.contract('0x8290333ceF9e6D528dD5618Fb97a76f268f3EDD4',abi=r)

abi = json.dumps(r)
c.functions.symbol().call()


import requests



















