import scrapy

class FlipkartSpider(scrapy.Spider):
    
    name = "flipkart"
    start_urls = ["https://www.flipkart.com/search?q="]
    products = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.output_callback = kwargs.get('args').get('callback')
        self.product = kwargs.get('args').get('query')

        self.start_urls[0] = self.start_urls[0] + self.product
    
    #scrapes the required data from the response    
    def parse(self, response):

        all_products_names = response.css('._4rR01T::text').extract()
        all_products_prices = response.css('._30jeq3._1_WHN1::text').extract()
        all_products_links = response.css('._1fQZEK::attr(href)').extract()

        for i in range(5):

            product_name = all_products_names[i]
            product_price = all_products_prices[i]
            product_link = "https://www.flipkart.com" +all_products_links[i]

            self.products.append({
                "name": product_name,
                "price": product_price[1:],
                "link": product_link,
                "soldBy": 'Flipkart'
            })

    #executes when the spider finished scraping
    def close(self, spider, reason):
        self.output_callback(self.products,"Flipkart")
