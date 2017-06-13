-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players(id serial primary key, name text);

CREATE TABLE matches(id serial,
		                 winner integer references players(id) on delete cascade,
		                 loser integer references players(id) on delete cascade,
                     primary key(id,winner,loser));

CREATE OR REPLACE VIEW playerStanding as 
    select p.id, 
           p.name,  
           coalesce(sum(case when p.id = m.winner then 1 else 0 end),0) as wins, 
           coalesce(count(m.id),0) as matches 
    from players p 
    left join 
    matches m 
    on p.id = m.winner or p.id = m.loser 
    group by p.id, p.name 
    order by wins desc, id asc;
