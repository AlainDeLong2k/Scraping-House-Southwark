import scrapy
import json
from housescraper.items import HousescraperItem


class HousespiderSpider(scrapy.Spider):
    name = "housespider"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = [
        "https://www.rightmove.co.uk/house-prices/southwark-85215.html?soldIn=5&page=1"
    ]

    def parse(self, response):
        script_content = response.xpath(
            "//script[contains(text(),'window.__PRELOADED_STATE__')]//text()"
        ).get()[29:]

        data = json.loads(script_content)
        property_items = data["results"]["properties"]

        for item in property_items:
            # yield {
            #     "address": item["address"],
            #     "type": item["propertyType"],
            #     "transactions": item["transactions"],
            #     "location": item["location"],
            #     "url": item["detailUrl"],
            # }
            house_item = HousescraperItem()
            house_item["address"] = item["address"]
            house_item["description"] = item["propertyType"]
            house_item["transactions"] = item["transactions"]
            house_item["location"] = item["location"]
            house_item["url"] = item["detailUrl"]
            yield house_item

        split_current_url = response.url.split("page=")
        current_page = int(split_current_url[-1])
        next_page = current_page + 1

        if next_page <= 40:
            next_page_url = split_current_url[0] + f"page={next_page}"
            yield response.follow(next_page_url, callback=self.parse)
