import scrapy
from itemloaders import ItemLoader

from JioMartScraper.items import JiomartscraperItem


class GroceryscraperSpider(scrapy.Spider):
    name = 'groceries'
    allowed_domains = ['www.jiomart.com']
    start_urls = ['https://www.jiomart.com/c/groceries/2']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        products = response.css('div.product-list').css('div.col-md-3').css('div.cat-item')
        # id = 0
        for item in products:
            # id += 1
            l = ItemLoader(item=JiomartscraperItem(), selector=item)
            l.add_css("name", "span.clsgetname::text")
            l.add_css("selling_price", "span#final_price::text")
            if item.css("strike#price::text"):
                l.add_css("original_price", "strike#price::text")
            else:
                l.add_value("original_price", "NA")
            l.add_css("image", "img::attr('data-src')")
            yield l.load_item()

        next_page = response.css('li.next').css("a::attr('href')").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
