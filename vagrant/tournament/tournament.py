#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from matches;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players;")
    num = c.fetchone()
    num = num[0]
    conn.close()
    return(num)

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players(name) values(%s)", (name,))
    conn.commit()
    n = countPlayers()
    c.execute("select max(id) from matches")
    curmatch = c.fetchone()[0]
    if(n % 2 == 0):
        i = 0
        c.execute("select id from players")
        players = c.fetchall()
        while( i < n ):
            c.execute("insert into matches(id,p1,p2) values(%s , %s)",(curmatch+1,players[i][0],players[i+1][0],))
            conn.commit()
            i = i + 2
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select * from playerstanding")
    res = c.fetchall()
    conn.close()
    return(res)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("update matches set win = %s where p1 = %s or p2 = %s",(winner,winner,winner,))
    c.execute("update matches set lose = %s where p1 = %s or p2 = %s",(loser,loser,loser,))
    c.commit()
    conn.close()

    
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    n = countPlayers()
    c.execute("select max(id) from matches")
    curmatch = c.fetchone()[0]
    if(n % 2 == 0):
        i = 0
        c.execute("select player as id from playerstanding")
        players = c.fetchall()
        while( i < n ):
            c.execute("insert into matches(id,p1,p2) values(%s , %s)",(curmatch+1,players[i][0],players[i+1][0],))
            conn.commit()
            i = i + 2
    c.execute("select * from swisspairing;")
    res = c.fectchall()
    conn.close()
    return(res)
    
