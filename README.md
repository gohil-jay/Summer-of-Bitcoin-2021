# Summer of Bitcoin Code Challenge 2021

This repository contains my work on cryptocurrency based problem statement for Summer of Bitcoin 2021.

# The problem

Bitcoin miners construct blocks by selecting a set of transactions from their mempool. Each transaction in the mempool:

- includes a ``` fee ``` which is collected by the miner if that transaction is included in a block
- has a ``` weight ```, which indicates the size of the transaction
- may have one or more ``` parent transactions ``` which are also in the mempool

The miner selects an ordered list of transactions which have a combined weight below the maximum block weight. Transactions with parent transactions in the mempool may be included in the list, but only if all of their parents appear before them in the list.

Naturally, the miner would like to include the transactions that maximize the total fee.

Your task is to write a program which reads a file mempool.csv, with the format:

``` <txid>, <fee>, <weight>, <parent_txids> ```

- ``` txid ``` is the transaction identifier
- ``` fee ``` is the transaction fee
- ``` weight ``` is the transaction weight
- ``` parent_txids ``` is a list of the txids of the transaction’s unconfirmed parent transactions (confirmed parent transactions are not included in this list). It is of the form: <txid1>;<txid2>;...

The output from the program should be txids, separated by newlines, which make a valid block, maximizing the fee to the miner. Transactions **MUST** appear in order (no transaction should appear before one of its parents).

We've included a non-working ``` block_sample.txt ``` file to demonstrate the expected format.
  
# Input file
  
Here are two lines of the ``` mempool.csv ``` file:

``` 2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0,452,1620, ```

This is a transaction with txid ``` 2e3da8... ```, fees of 452 satoshis, weight of 1620, and no parent transactions in the mempool.
  
``` 9d317fb308fd5451fd0ec612165638cb9e37bd8aa8918dff99a48fe05224276f,350,1400,288ea91bb52d8cb28289f4db0d857356622e39e78f33f26bf6df2bbdd3810fad;b5b993bda3c23bdefe4a1cf75b1f7cbdfe43058f2e4e7e25898f449375bb685c;c1ae3a82e52066b670e43116e7bfbcb6fa0abe16088f920060fa41e09715db7d ```
  
This is a transaction with txid ``` 9d317f... ``` , fees of 350 satoshis, weight of 1400 and three parent transactions in the mempool with txids ``` 288ea9.... ``` , ``` b5b993... ``` and ``` c1ae3a... ```
