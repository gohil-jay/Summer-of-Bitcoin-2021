# [Summer of Bitcoin Code](https://www.summerofbitcoin.org/) Challenge 2021

This repository contains my work on cryptocurrency based problem statement for Summer of Bitcoin 2021.

## The problem

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
  
## Input file
  
Here are two lines of the ``` mempool.csv ``` file:

``` 2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0,452,1620, ```

This is a transaction with txid ``` 2e3da8... ```, fees of 452 satoshis, weight of 1620, and no parent transactions in the mempool.
  
``` 9d317fb308fd5451fd0ec612165638cb9e37bd8aa8918dff99a48fe05224276f,350,1400,288ea91bb52d8cb28289f4db0d857356622e39e78f33f26bf6df2bbdd3810fad;b5b993bda3c23bdefe4a1cf75b1f7cbdfe43058f2e4e7e25898f449375bb685c;c1ae3a82e52066b670e43116e7bfbcb6fa0abe16088f920060fa41e09715db7d ```
  
This is a transaction with txid ``` 9d317f... ``` , fees of 350 satoshis, weight of 1400 and three parent transactions in the mempool with txids ``` 288ea9.... ``` , ``` b5b993... ``` and ``` c1ae3a... ```


## Parsing the input file
  
Here is some sample Python code to parse the input file. You may use this snippet in your solution if you want:

```
class MempoolTransaction():
  def __init__(self, txid, fee, weight, parents):
    self.txid = txid
    self.fee = int(fee)
    # TODO: add code to parse weight and parents fields

def parse_mempool_csv():
  """Parse the CSV file and return a list of MempoolTransactions."""
  with open('mempool.csv') as f:
    return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])
```
  
## Hints

- The total weight of transactions in a block must not exceed 4,000,000 weight. For this exercise assume that there is no coinbase transaction.
- A transaction may only appear in a block if all of its parents appear **_earlier_** in the block.

## General Advice

- Spend no more than two to three days on the exercise. The idea is not that you come up with a perfect solution, but that you think about your approach. First, make a naive solution that constructs a valid block, then iterate to improve it.
- We’re most familiar with Python, C++, JavaScript, Java, Rust, Scheme, Lisp, Ruby, and Elixir and would prefer to receive solutions in those languages. If you’d like to use a different language, please check with us first to make sure we’ll be able to review it!
- You should be able to explain your reasoning, design decisions, and trade-offs.
  
## What to send us

 - the source code for your solution (sending a GitHub repo URL works as well -- you will need to do this if you used JS)
 - the output from running the program with mempool.csv as block.txt .
 - You may optionally also include .git files to show your commit history

<hr>
<br>

# Solution

```
import pandas as pd

max_weight = 4000000
block_weight = 0
block_fee = 0
included_transactions = []
data = '/content/drive/MyDrive/Colab Notebooks/Summer of Bitcoin/mempool.csv'

def allow_tx(id):
  if id == "None":
    return True
  temp_id = id.split(';')

  return (set(temp_id).issubset(set(included_transactions)))

df = pd.read_csv(data)
sorted_df = df.sort_values(by='fee', ascending=False)
sorted_df = sorted_df.fillna("None")
sorted_df.reset_index(inplace = True)

for i in range(len(sorted_df)):

  if ( (block_weight + (sorted_df['weight'][i])) <= max_weight ):
    temp_parent = sorted_df.iloc[:, 4][i]

    if (allow_tx(temp_parent)):
      block_weight += sorted_df['weight'][i]
      block_fee += sorted_df['fee'][i]
      included_transactions.append(sorted_df['tx_id'][i])

write_data = []
for i in included_transactions:
  temp = i + "\n"
  write_data.append(temp)

with open("block.txt",'w') as f:
  for line in write_data:
    f.write(line)

from google.colab import files
files.download('block.txt')
```
                                                             
# Output
                                                             
```
59f0495cf66d1864359dda816eb7189b9d9a3a9cd9dc50a3707776b41a6c815b
3bfc4c22fc7aaded4b02c6a6d67b4a7bad297377e46e4c300208f3bc3d65aae1
87784075804f10dad1f815de867dde2875e73a13da798c317fcddd75e03efc95
0c8ebf9c75f63b7e5ff176e2937f24c694aa6b3bde0e59b5647983bbb7dd38d6
c3fef085fca34891e6456489d840ab68139b24857eb1f925b943066ebb988732
826c80c43044cc00bebdf021a42dca6946591f02710e4e6da58c094be8e62d00
2a75876d05905369cda2997032a66e0a0f12253aa5736a23c005d26b22983c1a
6a709ddadfcf13b2e302cf0f75163538b0273923cc55fccc158f7466abebc1a9
de669dad7f8d8b37a789cb8f86ddd62b93b7b8323d90ff29fa61ca1f41f8c73f
b8894fbe99628c253fa93cf178679727e117d04fea5e5079de002548a0dd6511
8de07b4f7af6f61dfb0ac878ba45bd7b8b7184a1376e5286c90cd983679447f5
fac0417aafa46ea002ed3e04fc38087b45aca6a15a47bd4e5026e1e6cefa7967
f3c2f6cb4573cf137178f355af9301f3c0dbebf23c172804a894a7e4f899c110
7f264c468f624b62071dbcb531de5af722b327d5b098f426314622340cf17512
7a7fc507db228511f2bf1d36b3cbc8ec2cc93d2ea86e8afed5f98a4d83602c5d
128ef32e064da2b40139ea8e71ee67a73062ee68ab183281d0d1ab7affe6c775
1b732f5cee1df25358edcf94492e0bc454b0531514316c3400586c329899a0f1
f7d6053d97ab5c113b23c5b59daed275650253a4c3414b7227f6f0ff9c34a53a
4e861a2201efaa7a8ec671924485f45b6fa66f3ed9b015a95c7aa073eca538aa
6f4338ff2f475cd89efe98ee6a3a8cbdfbac8abadc5f71b393dad1e9a4f411aa
671346a3a15ee138df436372867b5bb87d9fc1e4dcb32de24bf0e11782f46e4b
09264c7fbca91de06dca916190bde4612b7ee873b12c9cd04a55a7b0d41ccde5
846e6dbccb06faa9b83333c2fc2a6c1544fad5f0a9a5616f6fa1fca53c2744b0
2858f0a19605fede1c37462f9e599efc6020dd00c66a4a20db8ff64888e506e8
7c674bed714a08281921d6b0f11fac2fc07db4a120caf3357d4aa23b026bde2b
...
```
                                                             
To view the complete output, <a href="https://github.com/gohil-jay/Summer-of-Bitcoin-2021/blob/main/block.txt">click here</a>.
