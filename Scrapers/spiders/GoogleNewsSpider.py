import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class GoogleNewsSpider(scrapy.Spider):

    name = "GoogleNews"
    start_urls = ["https://news.google.com/search?hl=en-IN&gl=IN&ceid=IN%3Aen&q="]
    products = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_callback = kwargs.get('args').get('callback')
        self.query = kwargs.get('args').get('query')
        self.start_urls[0] = self.start_urls[0] + self.query

    #scrapes the required data from the response
    def parse(self, response):

        all_title = response.css('a.DY5T1d.RZIKme::text').extract()
        all_authors = response.css('a.wEwyrc.AVN2gc.uQIVzc.Sksgp::text').extract()
        all_links = response.css('a.DY5T1d.RZIKme::attr(href)').extract()
        for title, author, link in zip(all_title, all_authors, all_links):
            self.products.append({
                "title": title,
                "author": author,
                "link": "https://news.google.com"+link[1:],
            })

    #tes when the spider finished scraping
    def close(self, spider, reason):
        self.output_callback(self.products, "GoogleNews")