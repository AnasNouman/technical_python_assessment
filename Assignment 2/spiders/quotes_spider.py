import scrapy
from scrapy_splash import SplashRequest
from ..items import QuotesItem


class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes_spider'

    def start_requests(self):
        yield SplashRequest(
            url='http://quotes.toscrape.com/js',
            callback=self.parse
        )

    def parse(self, response):
        items = QuotesItem()
        for quote in response.css("div.quote"):
            items["quote"] = quote.css("span.text::text").extract_first()
            items["author"] = quote.css("small.author::text").extract_first()
            items["tags"] = quote.css("div.tags > a.tag::text").extract()
            yield items
        next_url = response.css('li.next > a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield SplashRequest(
                url=next_url,
                callback=self.parse
            )
