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

## update:
use this quey for outputing the csv file
on mac os, need to 
have

```
[mysqld]
secure_file_priv  
```

in /etc/my.cnf and then restart mysql server

```
mysql> select playerID,yearID,B_G,B_AB,B_R,B_H,B_2B,B_3B,B_HR,B_RBI,B_SB,B_CS,B_BB,B_SO,B_IBB,B_HBP,P_W,P_L,P_G,P_GS,P_CG,P_SHO,P_SV,P_IPOuts,P_H,P_ER,P_HR,P_BB,P_SO,P_BAOpp,P_ERA,P_IBB,P_WP,P_HBP,P_BK,P_BFP,P_GF,P_R,Classification from  (   select playerID, yearID, sum(Classification) >= 1 as Classification from smallerhof group by playerID, yearID  ) as realhof left join career_record using (playerID) INTO OUTFILE '/var/tmp/source2.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\n';
Query OK, 4024 rows affected (6.58 sec)
```