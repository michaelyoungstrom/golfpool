GolfPool [Under Development]
========
Golfpool is a django application to help run a fantasy style golf tournament with friends.

Please note I am still working on tidying this up. This is by no means a finished project.

Format
======
For PGA tournaments, golfers get split into individual pools. Users pick one player from
each pool (before a tournament begins) to be a part of their team. Once the event takes place,
the lowest **n** scores (where n is a varying number based on the tournament) will be
added for each tournament round, and the user with the lowest score wins.

Currently, scoring can be updated by running management commands that pull from ESPN's
website directly.
