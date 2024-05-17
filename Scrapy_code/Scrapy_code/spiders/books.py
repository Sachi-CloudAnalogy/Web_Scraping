import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["http://www.values.com/inspirational-quotes"]

    def parse(self, response):
        for quote in response.css('div.col-6.col-lg-4.text-center.margin-30px-bottom.sm-margin-30px-top'):
            img_alt = quote.css('img::attr(alt)').get()
            if img_alt:
                line, author = img_alt.split(" #")
                yield {
                    'lines': line,
                    'author': author,
                }
