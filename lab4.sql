#Create new table smaller hall of fame and add column to it called 'Classification'
#Set Classification to 1 if that player was already inducted or not
drop table if exists smallerhof;
create table smallerhof as select * from HallOfFame;

drop procedure if exists createClassification;

DELIMITER @@
create procedure createClassification()
begin


ALTER TABLE smallerhof
ADD COLUMN Classification INT;

update smallerhof set Classification := 0;
update smallerhof set Classification := 1 where smallerhof.inducted = 'Y';

update smallerhof set Classification := 1 where smallerhof.inducted = 'N'
and smallerhof.votedBy = 'Run Off'
and smallerhof.needed_note = '1st';
END@@
DELIMITER ;


call createClassification();

#Feature Extraction
alter table smallerhof
drop column votedBy,
drop column ballots,
drop column needed,
drop column votes,
drop column inducted,
drop column category,
drop column needed_note;

#Get batting stats and add to table smallerbatting
drop table if exists smallerbatting;
create table smallerbatting as
select playerID, sum(G) AS B_G, sum(AB) AS B_AB, sum(R) AS B_R, sum(H) AS B_H, sum(2B) AS B_2B, sum(3B) AS B_3B, sum(HR) AS B_HR, sum(RBI) AS B_RBI, 
    sum(SB) AS B_SB, sum(CS) AS B_CS, sum(BB) AS B_BB, sum(SO) AS B_SO, sum(IBB) AS B_IBB, sum(HBP) AS B_HBP, sum(SH) AS B_SH, sum(SF) AS B_SF, 
    sum(GIDP) AS B_GIDP from Batting group by playerID;

alter table smallerbatting add constraint `pk_smallerbatting` primary key (playerID);

#Get pitching stats and add to table smallerpitching
drop table if exists smallerpitching;
create table smallerpitching as
select playerID as P_playerID, sum(W) AS P_W, sum(L) AS P_L, sum(G) AS P_G, sum(GS) AS P_GS, sum(CG) AS P_CG, sum(SHO) AS P_SHO, sum(SV) AS P_SV, sum(IPOuts) AS P_IPOuts,
    sum(H) AS P_H, sum(ER) AS P_ER, sum(HR) AS P_HR, sum(BB) AS P_BB, sum(SO) AS P_SO, avg(BAOpp) AS P_BAOpp, avg(ERA) AS P_ERA, sum(IBB) AS P_IBB, sum(WP) AS P_WP,
    sum(HBP) AS P_HBP, sum(BK) AS P_BK, sum(BFP) AS P_BFP, sum(GF) AS P_GF, sum(R) AS P_R, sum(SH) AS P_SH, sum(SF) AS P_SF, sum(GIDP) AS P_GIDP from Pitching 
    group by P_playerID;

alter table smallerpitching add constraint `pk_smallerpitching` primary key (p_playerID);

-- SELECT 'TEST1';
#Get fielding stats and add to table smallerfielding
drop table if exists smallerfielding;
create table smallerfielding as
SELECT `fielding`.`playerID` as f_playerID,
    -- sum(`fielding`.`yearID`),
    -- sum(`fielding`.`stint`),
    -- sum(`fielding`.`teamID`),
    -- sum(`fielding`.`lgID`),
    -- sum(`fielding`.`POS`) as f_POS,
    sum(`fielding`.`G`) as f_G,
    -- sum(`fielding`.`GS`) as f_GS,
    -- sum(`fielding`.`InnOuts`) as f_InnOuts,
    sum(`fielding`.`PO`) as f_PO,
    sum(`fielding`.`A`) as f_A,
    sum(`fielding`.`E`) as f_E,
    sum(`fielding`.`DP`) as f_DP,
    sum(`fielding`.`PB`) as f_PB,
    sum(`fielding`.`WP`) as f_WP,
    sum(`fielding`.`SB`) as f_SB,
    sum(`fielding`.`CS`) as f_CS,
    sum(`fielding`.`ZR`) as f_ZR
FROM `lahman2016`.`fielding`
group by f_playerID;
-- SELECT 'TEST1';

-- alter table smallerfielding add constraint 'pk_smallerfielding' primary key (f_playerID);



#Combine pitching and batting stats into one table career_records
drop table if exists career_record;
create table career_record as 
-- select * from smallerbatting left join smallerpitching on smallerbatting.playerID = smallerpitching.P_playerID union select * from smallerbatting right join smallerpitching on smallerbatting.playerID = smallerpitching.P_playerID;
select * 
from smallerbatting 
left join smallerpitching on smallerbatting.playerID = smallerpitching.P_playerID 
left join smallerfielding on smallerbatting.playerID = smallerfielding.f_playerID 
union all
select * from smallerpitching 
left join smallerbatting on smallerbatting.playerID = smallerpitching.P_playerID
left join smallerfielding on smallerpitching.P_playerID = smallerfielding.f_playerID
where smallerbatting.playerID IS NULL
union all
select * from smallerfielding 
left join smallerbatting on smallerbatting.playerID = smallerfielding.f_playerID
left join smallerpitching on smallerpitching.P_playerID = smallerfielding.f_playerID
where smallerbatting.playerID IS NULL AND smallerpitching.P_playerID IS NULL
;

-- select playerID,yearID,B_G,B_AB,B_R,B_H,B_2B,B_3B,B_HR,B_RBI,B_SB,B_CS,B_BB,B_SO,B_IBB,B_HBP,P_W,P_L,P_G,P_GS,P_CG,P_SHO,P_SV,P_IPOuts,P_H,P_ER,P_HR,P_BB,P_SO,P_BAOpp,P_ERA,P_IBB,P_WP,P_HBP,P_BK,P_BFP,P_GF,P_R,Classification
-- from (select playerID, yearID, sum(Classification) >= 1 as Classification from smallerhof group by playerID, yearID) as therealhof left join career_record using (playerID);
