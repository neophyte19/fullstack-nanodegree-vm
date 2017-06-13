Swiss-system Tournament
=============

This project accompanies the Intro to Relational Database course from Udacity. It can be used to keep track of players, matches, and standings in a Swiss-system tournament as well as determine match pairs for each round. Ranking is determined by number of wins. The assumption here is that there are even number of players, so no player is left without a match.

PostgreSQL is used to manage the database system, and Python's psycopg2 package is used as the implementation of the Python DB-API.

A tournament can be simulated by hosting the database on a virtual machine such as VirtualBox and running commands in python. The environment and all of the dependencies needed can be installed using Vagrant and the exact configuration can be found on the following Github page from Udacity:

https://github.com/udacity/fullstack-nanodegree-vm

After installing VirtualBox and Vagrant, clone the repository in the link above. Replace the files in the tournament folder with those from this repository. From the tournament folder, power on the virtual machine from the command line using vagrant up. Once in the virtual machine, you can load the database with psql -c '\i tournament.sql' and execute python tournament_test.py to simulate a tournament. 
