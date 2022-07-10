import scrapy
from itemloaders import ItemLoader
from JioMartScraper.items import SmartwatchesscraperItem


class SmartwatchesscraperSpider(scrapy.Spider):
    name = 'smart-watches'
    allowed_domains = ['www.amazon.in']
    start_urls = ['https://www.amazon.in/s?k=smart+watches&i=watches&ref=nb_sb_noss']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        products = response.css('div.s-main-slot').css('div.s-result-item').css('div.aok-relative').css(
            'div.a-section').css('div.sg-row')

        for item in products:
            l = ItemLoader(item=SmartwatchesscraperItem, selector=item)
            l.add_css('name', "span.a-text-normal::text")
            l.add_css('rating', "i.a-icon span.a-icon-alt::text")
            l.add_css('selling_price', "span.a-price span.a-offscreen::text")
            l.add_css('original_price', "span.a-text-price span.a-offscreen::text")
            l.add_css('image', "img::attr('src')")
            yield l.load_item()

        next_page = response.css('div.s-pagination-container').css("span.s-pagination-strip").css(
            "a.s-pagination-next::attr('href')").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
