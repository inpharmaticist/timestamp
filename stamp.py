#!/usr/bin/env python
 
import os
import json
import sys
import datetime

def getblockhash(block):
    return json.loads(os.popen('bitcoin-cli getblockstats '+str(block)).read())['blockhash']

def getblocktimestamp(block):
    return str(json.loads(os.popen('bitcoin-cli getblockstats '+str(block)).read())['time'])

def readablets():
	return datetime.datetime.now().strftime('%Y%m%d%H%M')

try:
    argument = sys.argv[1]
except:
    argument = 'test'

try:
    argument = os.popen("echo '"+argument+"'|gpg --clear-sign").read()
except:
    True

try:
    currentblock = int(os.popen('bitcoin-cli getblockcount').read().splitlines()[0])
except:
    currentblock = os.popen('curl -sSL "https://mempool.space/api/blocks/tip/height"').read()

tosign = argument+"""
Block Hash Timestamp
"""+str(currentblock)+' '+getblockhash(currentblock)+' '+getblocktimestamp(currentblock)+' '+"""
"""+str(currentblock-1)+' '+getblockhash(currentblock-1)+' '+getblocktimestamp(currentblock-1)+' '+"""
"""+str(currentblock-2)+' '+getblockhash(currentblock-2)+' '+getblocktimestamp(currentblock-2)

ts=readablets()
with open('ots_stamp_'+ts+'.txt', "w") as write:
    write.write(tosign)
os.system('ots stamp ots_stamp_'+ts+'.txt')