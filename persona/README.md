


#environment
	anaconda for python3
	after that is installed create the virtual environment
		conda env create --name per -f environment.yml
	pyflakes and pytest used throughout

./models.py createdb
./models.py sampledata gendata/clean500.csv


performance notes:
http://sqlite.org/speed.html
A series of tests were run to measure the relative performance of SQLite 2.7.6, PostgreSQL 7.1.3, and MySQL 3.23.41. The following are general conclusions drawn from these experiments:

SQLite 2.7.6 is significantly faster (sometimes as much as 10 or 20 times faster) than the default PostgreSQL 7.1.3 installation on RedHat 7.2 for most common operations.

SQLite 2.7.6 is often faster (sometimes more than twice as fast) than MySQL 3.23.41 for most common operations.

SQLite does not execute CREATE INDEX or DROP TABLE as fast as the other databases. But this is not seen as a problem because those are infrequent operations.

SQLite works best if you group multiple operations together into a single transaction.

The results presented here come with the following caveats:

These tests did not attempt to measure multi-user performance or optimization of complex queries involving multiple joins and subqueries.

These tests are on a relatively small (approximately 14 megabyte) database. They do not measure how well the database engines scale to larger problems.
