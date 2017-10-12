import csv
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from OnionCrawler.items import OnionCrawlerScraperItem
import datetime
from booleanlogic import SearchTerm

class OnionCrawler(CrawlSpider):

    name = 'OnionCrawler'

    global readURLsFromHSProbeLog
    global readURLsFromOnionList
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
         
        # Case-sensitivity, default is False
        self.caseSensitive = kwargs.get('caseSensitive')
        if not self.caseSensitive or self.caseSensitive.lower() == 'false':
            self.caseSensitive = False
        elif self.caseSensitive.lower() == 'true':
            self.caseSensitive = True
            
         # Searchterms to filter for
        self.searchTerms = kwargs.get('searchTerms')
        if self.searchTerms:
            if self.caseSensitive:
                self.query = SearchTerm(phrase=str(self.searchTerms))
            else:
                self.query = SearchTerm(phrase=str(self.searchTerms).lower())
        else:
            self.query = False        
            
        # Pipeline selection. To be processed in pipelines.py
        self.pipelineFile = kwargs.get('pipelineFile')
         # Set Filesystem pipeline as default
        if not self.pipelineFile:
                self.pipelineFile = 'true'
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

    def createItem(response):
        item = OnionCrawlerScraperItem()
        item['url'] = response.url
        item['body'] = response.body
        item['utctimestamp'] = datetime.datetime.utcnow()
        return item
       
    def parse_items(self, response):
        # If there are searchterms defined, chose whether websites should be scraped if ANY search term matches (OR) or only if ALL search terms match (AND).
        if self.query:
            if self.caseSensitive:
                match = self.query.test(response.body)
            else:
                match = self.query.test(response.body.lower())
            if match:
                   yield createItem(response)
        # If there are no searchterms defined, yield all crawled websites
        else:
            yield createItem(response)
        return
