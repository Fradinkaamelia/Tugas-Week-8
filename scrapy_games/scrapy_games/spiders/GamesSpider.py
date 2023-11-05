import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import pandas as pd

class scrapySpider(CrawlSpider):
    name = "scrapy"
    allowed_domains = ["store.playstation.com"]
    base_url = "https://store.playstation.com/en-id/category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/"
    
    def start_requests(self):
        for page in range(1,17):
            url = f"{self.base_url}{page}/"
            yield scrapy.Request(url=url, callback=self.parse)

    rules = (
        Rule(LinkExtractor(allow="category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/\d+")),
        Rule(LinkExtractor(allow="product/"), callback="parse_item")
    )

    def parse(self,response):
        title = response.css("span.psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2::text").getall()
        price = response.css("span.psw-m-r-3::text").getall()

        for i,j in zip(title, price):
            yield{
                "Title" : i.strip(),
                "Price" : j.strip().replace(",",".").replace("\xa0","")
            }