Onion Crawler
==================

Scrapy spider to recursively crawl for TOR hidden services.


Prerequisites
=============

torsocks
Python 2.7
Scrapy

Additionally for PostgreSQL support:
python-sqlalchemy
python-psycopg2


Usage
=====

$ torsocks scrapy crawl OnionCrawler
to run OnionCrawler with default settings

OR 

$ torsocks scrapy crawl OnionCrawler [-a argument1=value1] [-a argument2=value2] [...]
to customize the Crawler's behaviour, the argument/value pairs described below can be passed each with a prefixed '-a'

Argument/Value				Description					
--------------				-----------
inputURL=<SingleURL>			Single URL to start crawling from
inputOnionList=<pathToOnionList>	Path to newline-separated .onion URL list			
inputHSProbeLog=<HSProbeLogFile> 	Read .onion names from HS Probe logfile
searchTerms=<SearchTerms>		Comma-separated search terms
searchMode=<ORorAND>			Search either for any or all search terms
pipelineFile=<trueOrFalse>		De-/Activate pipeline scraping to filesystem
pipelinePostgres=<trueOrFalse>		De-/Activate pipeline scraping to Postgres DB


Defaults
========

inputURL=https://facebookcorewwwi.onion/
searchMode=OR
pipelineFile=true
pipelinePostgres=false

By default, no search terms are set which means all crawled websites are scraped. A pipeline which stores scraped websites as files in ./files/ is activated and the .onion URL https://facebookcorewwwi.onion is the default start URL for crawling. No search terms are set, if you set some without defining the search mode, searching for any (OR) is default.


Examples
========

Reading hidden services from HSProbe logfile hsprobe.log, search crawled websites for one of the search terms "TOR" or "onion", and store in filesystem:
$ torsocks scrapy crawl OnionCrawler -a inputHSProbeLog=hsprobe.log -a searchTerms=TOR,onion 

Reading .onion names from list.txt, scrape all crawled websites which contain both search terms "TOR" and "onion", and store in PostgreSQL database:
$ torsocks scrapy crawl OnionCrawler -a inputOnionList=list.txt -a searchTerms=TOR,onion -a searchMode=AND -a pipelineFile=false -a pipelinePostgres=true


PostgreSQL
=========

In order to store scraped websites in a PostgreSQL database, the corresponding pipeline has to be activated in settings.py.
Furthermore, the following has to be done:

1. Set up the PostgreSQL database.
2. Change database credentials in setting.py's DATABASE dictionary accordingly.
3. Uncomment the parameter "AllowOutboundLocalhost 1" in the torsocks configuration file (/etc/tor/torsocks.conf).
