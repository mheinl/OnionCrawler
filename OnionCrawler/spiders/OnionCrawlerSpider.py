import csv
import os
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from OnionCrawler.items import OnionCrawlerScraperItem


class OnionCrawler(CrawlSpider):
    
    name = 'OnionCrawler'
    global saveSiteToFile
    global readURLsFromHSProbeLog
    
    is_allowed = [".onion"]
    
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]
    
   
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
    
    
    
    # Method to write HTML into subdirectories and files
    def saveSiteToFile(site):
        # Filename includes path
        urlWithoutProtocol = site.url.split("://")[1].strip('/')
        if '/' not in urlWithoutProtocol:
            filename = 'files/' + urlWithoutProtocol + '/index.html'
        else:
            filename = 'files/' + urlWithoutProtocol + '.html'        
        # Directory is only path to file without filename at the end
        directory = filename[0:(len(filename)-len(filename.split('/')[-1]))]
        # Check if directory already exists. If not, create it.
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Write HTML to file named filename
        with open(filename, 'wb') as f:
            f.write(site.body)
        
                

    # Method for parsing items
    def parse_items(self, response):
        
        # Save response into filesystem
        saveSiteToFile(response)
       
        # List of items found on scraped page
        items = []
        # Extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Go through all the found links
        for link in links:
            # Check if domain of the URL is within scope
            is_allowed = False
            for domain in self.is_allowed:
                if domain in link.url:
                    is_allowed = True
            # If in scope, create a new item and add it to the list of found items
            if is_allowed:
             item = OnionCrawlerScraperItem()
             item['url_from'] = response.url
             item['url_to'] = link.url
             items.append(item)
        # Return all found items
        return items