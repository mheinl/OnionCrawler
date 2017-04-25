import csv
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from OnionCrawler.items import OnionCrawlerScraperItem
import datetime

class OnionCrawler(CrawlSpider):

    name = 'OnionCrawler'
    global saveSiteToFile
    global saveSitetoDB
    global readURLsFromHSProbeLog
    
    # define alowed domain, for all onion TLDs, just set "onion"
    allowed_domains = ["onion"]
    
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback='parse_items'
        )
    ]
    
    # Keywords to filter for
    global keywords
    keywords = ['.onion', 'darknet', 'dark net', 'darkweb', 'dark web', 'TOR']
    # Method to read start_urls[] from HSProbe Logfile
    def readURLsFromHSProbeLog(logfile):
        urlList = []
        with open(logfile, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[3] == 'DONE':
                    urlList.append(row[4] + '://' + row[0] + '.onion') #:' + row[1])
        return urlList


    # EITHER use hard coded URLs
    start_urls = ['https://facebookcorewwwi.onion']
    # OR read HSPRobe log from filesystem
    #start_urls = readURLsFromHSProbeLog('HSProbe.log')
       
    def parse_items(self, response):
        if any(x in response.body for x in keywords):
            item = OnionCrawlerScraperItem()
            item['url'] = response.url
            item['body'] = response.body
            item['time'] = datetime.datetime.now()
            yield item
        return
