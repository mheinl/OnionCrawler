import csv
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from OnionCrawler.items import OnionCrawlerScraperItem
import datetime

class OnionCrawler(CrawlSpider):

    name = 'OnionCrawler'

    global readURLsFromHSProbeLog
    global readURLsFromOnionList
    global parseSearchTerms
    global createItem
    
    # Process potential arguments to control program flow
    def __init__(self, *args, **kwargs):
        super(OnionCrawler, self).__init__(*args, **kwargs) 
        
          # Single Start_URL
        inputURL = kwargs.get('inputURL')
        if inputURL:
            self.start_urls = [inputURL]
            
        # Input File (.onion List)
        inputOnionList = kwargs.get('inputOnionList')
        if inputOnionList:
            if self.start_urls:
                self.start_urls.extend(readURLsFromOnionList(inputOnionList))
            else:
                self.start_urls = readURLsFromOnionList(inputOnionList)
        
        # Input File (HSProbe Logfile)
        inputHSProbeLog = kwargs.get('inputHSProbeLog')
        if inputHSProbeLog:
            if self.start_urls:
                self.start_urls.extend(readURLsFromHSProbeLog(inputHSProbeLog))
            else:
                self.start_urls = readURLsFromHSProbeLog(inputHSProbeLog)
        
        # Check if start_urls is still empty. If so, set it to default test value
        if not self.start_urls:
            self.start_urls = ['https://facebookcorewwwi.onion']
        
        # Searchterms to filter for
        global keywords
        keywords = ['']
        searchTerms = kwargs.get('searchTerms')
        if searchTerms:
            keywords = parseSearchTerms(searchTerms)
            
        # Search Term Conjunction
        global boolOR, boolAND
        searchMode = kwargs.get('searchMode')
        if searchMode == 'AND':
            boolAND = True
            boolOR = False
        else:
            boolOR = True
            boolAND = False
            
        # Pipeline Selection. To be processed in pipelines.py
        self.pipelineFile = kwargs.get('pipelineFile')
        self.pipelinePostgres = kwargs.get('pipelinePostgres')        
    
    # Define allowed domain, for all onion TLDs, just set "onion"
    allowed_domains = ["onion"]
    
    # Define crawling rules
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
    
    # Method to read start_urls[] from HSProbe Logfile
    def readURLsFromHSProbeLog(logfile):
        urlList = []
        with open(logfile, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if row[3] == 'DONE':
                    urlList.append(row[4] + '://' + row[0] + '.onion')
        return urlList
    
    # Method to read start_urls[] from List of .onion names
    def readURLsFromOnionList(list):
        urlList = open(list).read().splitlines()
        return urlList

    # Method to parse Search Terms
    def parseSearchTerms(searchTerms):
        searchTermList = [term.strip() for term in searchTerms.split(',')]
        return searchTermList
    
    def createItem(response):
        item = OnionCrawlerScraperItem()
        item['url'] = response.url
        item['body'] = response.body
        item['utctimestamp'] = datetime.datetime.utcnow()
        return item
       
    def parse_items(self, response):
        # If there are searchterms defined, chose whether websites should be scraped if ANY search term matches (OR) or only if ALL search terms match (AND).
        if keywords:
            if boolAND:
                if all(x in response.body for x in keywords):
                   yield createItem(response)
            if boolOR:
                if any(x in response.body for x in keywords):
                   yield createItem(response)
        # If there are no searchterms defined, yield all crawled websites
        else:
            yield createItem(response)
        return
