-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--DROP DATABASE IF EXISTS tournament;
--CREATE DATABASE tournament;
\c tournament;

DROP TABLE IF EXISTS matches cascade;
DROP TABLE IF EXISTS players cascade;

CREATE TABLE players(id serial primary key, name text);

CREATE TABLE matches(id integer, 
                     p1 integer references players(ID) on delete cascade, 
                     p2 integer references players(ID) on delete cascade, 
                     win integer references players(ID) on delete cascade,
                     lose integer references players(ID) on delete cascade, 
                     primary key(id,p1,p2));
                     
CREATE OR REPLACE VIEW swissPairing as 
select p1 as id1 , pl1.name as name1, p2 as id2, pl2.name as name2 
from matches m
join players pl1 
on m.p1 = pl1.id 
join players pl2 
on m.p2 = pl2.id 
where m.id = (select max(id) from matches);   

CREATE OR REPLACE VIEW playerstanding as 
select player ,name, sum(win) wins, (max(matchid))-1 as matches 
from
(select id as matchid, p1 as player, case when p1=win then 1 else 0 end win,case when p1=lose then 1 else 0 end lose from matches 
union
select id as matchid, p2 as player, case when p2=win then 1 else 0 end win,case when p2=lose then 1 else 0 end lose  from matches
) a 
join players 
on a.player = players.id
group by player,name 
order by wins desc;


