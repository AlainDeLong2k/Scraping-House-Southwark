import scrapy


class HousespiderSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://rightmove.co.uk"]

    def parse(self, response):
        pass
