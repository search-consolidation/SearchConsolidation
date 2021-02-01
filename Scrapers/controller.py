from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor

from .spiders.GoogleNewsSpider import GoogleNewsSpider
from .spiders.AmazonSpider import AmazonSpider
from .spiders.FlipkartSpider import FlipkartSpider
class Controller:

    #initializing runner with CrawlerProcess() 
    def __init__(self):
        self.output = {}
        self.runner = CrawlerRunner(settings={'LOG_ENABLED': False})

    #Adds spiders to the queue of the reactor 
    def start_crawler(self, runner, spider, query=None):
        if query is not None:
            self.runner.crawl(spider, args={'callback': self.yield_output,'query':query})
        else:
            self.runner.crawl(spider, args={'callback': self.yield_output})

    #gets the data from the spider's close method and stores it in the output
    def yield_output(self,data,spider_name):
        self.output[spider_name] = data

    #controls the execution of spiders
    def controller(self,keyword,query=None):

        #if the keyword is headlines
        if keyword == 'headlines':    
            self.start_crawler(self.runner,GoogleNewsSpider, query)
        #if the keyword is query
        elif keyword == 'product':
            self.start_crawler(self.runner,AmazonSpider,query)
            self.start_crawler(self.runner,FlipkartSpider,query)
        else:
            return "Invalid keyword"

        #starts the crawling one by one
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        #returns the output
        return self.output
