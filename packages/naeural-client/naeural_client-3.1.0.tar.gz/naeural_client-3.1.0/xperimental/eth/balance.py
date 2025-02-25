import os
from copy import deepcopy

from naeural_client import Logger, const
from naeural_client.bc import DefaultBlockEngine



if __name__ == '__main__' :
  l = Logger("ENC", base_folder=".", app_folder="_local_cache")
  eng = DefaultBlockEngine(
    log=l, name="default", 
    verbosity=2,
  )
  with open("xperimental/eth/addrs.txt", "rt") as fd:
    lines = fd.readlines()
    addresses = [line.strip() for line in lines]
      
  
  l.P("Check #1", color='b')
  for address in addresses:
    eth_balance = eng.web3_get_balance_eth(address)    
    l.P(f"ETH Balance of {address} is {eth_balance:.4f} ETH")
    r1_balance = eng.web3_get_balance_r1(address)
    l.P(f"R1 Balance of {address} is {r1_balance:.4f} R1")
    
  
  l.P("Check #2", color='b')
  for address in addresses:
    eth_balance = eng.web3_get_balance_eth(address, network="mainnet")    
    l.P(f"ETH Balance of {address} is {eth_balance:.4f} ETH")
    r1_balance = eng.web3_get_balance_r1(address)
    l.P(f"R1 Balance of {address} is {r1_balance:.4f} R1")

  l.P("Check #3", color='b')
  for address in addresses:
    eth_balance = eng.web3_get_balance_eth(address)    
    l.P(f"ETH Balance of {address} is {eth_balance:.4f} ETH")
    r1_balance = eng.web3_get_balance_r1(address)
    l.P(f"R1 Balance of {address} is {r1_balance:.4f} R1")
    
  eng.reset_network("mainnet")

  l.P("Check #4", color='b')
  for address in addresses:
    eth_balance = eng.web3_get_balance_eth(address)    
    l.P(f"ETH Balance of {address} is {eth_balance:.4f} ETH")
    r1_balance = eng.web3_get_balance_r1(address)
    l.P(f"R1 Balance of {address} is {r1_balance:.4f} R1")
