## Dependencies
	1. Python
	2. python-MySQLdb
		http://sourceforge.net/projects/mysql-python/
	3. python Scrapy
		http://scrapy.org/download/

## Installation
	1. create db
		$ mysql -uroot -proot
		mysql> create database podcastdb;
	2. create table
		$ mysql -uroot -proot podcastdb < db/mysql.sql
	
	3. start crawler server
		$ scrapy server
		
	4. register the spider in the server
		$ curl http://localhost:6800/schedule.json -d project=default -d spider=itunes
		
	5. Just keep watching the spiders making their work:
		http://localhost:6800/