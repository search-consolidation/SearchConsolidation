from .spiders.NDTVSpider import NDTVSpider
from .spiders.TimesOfIndiaSpider import TimesOfIndiaSpider
from .spiders.OnionSpider import OnionSpider
from .spiders.AmazonSpider import AmazonSpider
from .spiders.FlipkartSpider import FlipkartSpider

from scrapy.crawler import CrawlerProcess, CrawlerRunner

import sys
import time
from twisted.internet import reactor

class Controller:

    #initializing runner with CrawlerProcess() 
    def __init__(self):
        self.output = {}
        self.runner = CrawlerRunner(settings={'LOG_ENABLED': False})

    #Adds spiders to the queue of the reactor 
    def start_crawler(self,runner, spider, product=None):
        if product is not None:
            self.runner.crawl(spider, args={'callback': self.yield_output,'product':product})
        else:
            self.runner.crawl(spider, args={'callback': self.yield_output})

    #gets the data from the spider's close method and stores it in the output
    def yield_output(self,data,spider_name):
        self.output[spider_name] = data

    #controls the execution of spiders
    def controller(self,keyword,product=None):

        #if the keyword is headlines
        if keyword == 'headlines':    
            self.start_crawler(self.runner,NDTVSpider)
            # self.start_crawler(self.runner,TimesOfIndiaSpider)
            # self.start_crawler(self.runner,OnionSpider)
        #if the keyword is product
        elif keyword == 'product':
            self.start_crawler(self.runner,AmazonSpider,product)
            self.start_crawler(self.runner,FlipkartSpider,product)
        else:
            return "Invalid keyword"

        #starts the crawling one by one
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        #returns the output
        return self.output
