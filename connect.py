import pymysql
# v1

import pandas

conn = pymysql.connect(user='root', password='', database='lahman2016')
cursor = conn.cursor()
query = 'select playerID,yearID,B_G,B_AB,B_R,B_H,B_2B,B_3B,B_HR,B_RBI,B_SB,B_CS,B_BB,B_SO,B_IBB,B_HBP,P_W,P_L,P_G,P_GS,P_CG,P_SHO,P_SV,P_IPOuts,P_H,P_ER,P_HR,P_BB,P_SO,P_BAOpp,P_ERA,P_IBB,P_WP,P_HBP,P_BK,P_BFP,P_GF,P_R,Classification from (select playerID, yearID, sum(Classification) >= 1 as Classification from smallerhof group by playerID, yearID) as therealhof left join career_record using (playerID);'

results = pandas.read_sql_query(query, conn)
results.to_csv("source.csv", index=False)