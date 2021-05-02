import scrapy
from ..items import BooksItem


class BooksToScrapeSpider(scrapy.Spider):
    name = 'books_to_scrape'

    def start_requests(self):
        yield scrapy.Request(
            url='http://books.toscrape.com/',
            callback=self.parse
        )

    def parse(self, response):
        categories = response.css("div.side_categories > ul.nav-list ul a::attr(href)").extract()
        for category in categories:
            new_url = response.urljoin(category)
            yield scrapy.Request(
                url=new_url,
                callback=self.parse_category
            )

    def parse_category(self, response):
        pass
        items = BooksItem()
        for book in response.css("article.product_pod"):
            items["book_title"] = book.css("img.thumbnail::attr(alt)").extract_first()
            items["book_price"] = book.css("div.product_price > p.price_color::text").extract_first()
            items["book_image_URL"] = book.css("img.thumbnail::attr(src)").extract_first()
            items["book_detail_URL"] = book.css("div.image_container > a::attr(href)").extract_first()
            yield items
        next_url = response.css('li.next > a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_category
            )
