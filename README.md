## step 1 - construct final dataset
create the `lab4.sql` to construct the final dataset for the machine learning, useless columns and fields are then removed

how to construct the dataset:
1. install mysql on local machine and run `source lahman2016.sql`
2. create the lab4.sql
3. `source lab4.sql`

## step 2 - export data from dataset (mysql) to CSV format
create `connect.py`

## step 3 - create data helpers and csv helpers
create `helper.py`

## step 4 - train and test; generate result and graph
create `train.py`

## step 5 - run program
`$ python3 train.py 1 gini source.csv`
`$ python3 train.py 1 entropy source.csv`

- `source.csv` is final dataset in csv format
