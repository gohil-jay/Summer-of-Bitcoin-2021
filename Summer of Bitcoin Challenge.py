# Jupyter notebook is converted to python here.

# Importing libraries
import pandas as pd

# Defining few global values....
max_weight = 4000000
block_weight = 0
block_fee = 0
included_transactions = []
data = 'Add location here'

# Function to check whether transaction should be allowed to be added to block transactions or not.
# This function checks parent requirements only, as weight threshold check is done later.

def allow_tx(id):
  if id == "None": #If there's no parent, allow transaction.
    return True
  temp_id = id.split(';') #If there are parents, split them into an array.

  # Check if all of parents are present in pre-transaction list
  return (set(temp_id).issubset(set(included_transactions)))

# Read CSV file, and create a pandas dataframe for viable accessibility
df = pd.read_csv(data)

# Printing the dataframe
df

# Sorting the dataframe to keep highest-fee transactions first
sorted_df = df.sort_values(by='fee', ascending=False)

# Filling NaN (Not a Number) or empty values with 'None'
sorted_df = sorted_df.fillna("None")

# Printing the sorted and updated dataframe
sorted_df

# Resetting the index of transactions in dataframe
sorted_df.reset_index(inplace = True)

# Printing the reset-indexed dataframe
sorted_df

# Traversing through dataframe to create a set of transaction ids as per the challenge requirements
for i in range(len(sorted_df)): # Traversing through dataframe

  if ( (block_weight + (sorted_df['weight'][i])) <= max_weight ): # Check if the addition of this transaction will cross the max-weight value (if not, continue)

    temp_parent = sorted_df.iloc[:, 4][i] # Take parents of the transaction into a variable

    if (allow_tx(temp_parent)): # checking if the parent transactions are present earlier

      # If all conditions are satisfied, move forward with adding the transaction to block transaction list.

      block_weight += sorted_df['weight'][i] # Adding transaction weight to block weight
      block_fee += sorted_df['fee'][i] # Adding transaction fee to block fee
      included_transactions.append(sorted_df['tx_id'][i]) # Adding transaction id to block transaction-ids

      # This addition to global variables will help in dynamic checking and addition process of transaction-ids due to constant updates in global variables

print("\n")
print("The total miner fee for the block :", block_fee)
print("\n")
print("The total weight for the block :", block_weight)
print("\n")

print("The number of transactions in the block :", len(included_transactions))

print("The list of transactions included in the block : ")
print("\n")
included_transactions

# Adding '\n' to end of each transaction
write_data = []
for i in included_transactions:
  temp = i + "\n"
  write_data.append(temp)

# Writing all the transaction ids to block.txt
with open("block.txt",'w') as f:
  for line in write_data:
    f.write(line)

print("File write process successful!")

# Thank you!
