import scrapy


class LivrariaSpiderSpider(scrapy.Spider):
    name = 'livraria_spider'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        livros = response.css('article.product_pod a::attr(href)').extract()
        for livro in livros:
            yield response.follow(livro, callback=self.parse_livro)
            next_page = response.css('li.next a::attr(href)').extract_first()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def parse_livro(self, response):
        title = response.css('div.col-sm-6.product_main h1::text').extract_first()
        genre = response.css('ul.breadcrumb a::text').extract()[2]
        price = response.css('div.col-sm-6.product_main p.price_color::text').extract_first()
        stock = response.css('div.col-sm-6.product_main p.instock.availability::text').extract()
        stock = ''.join(stock).strip()
        upc = response.css('table.table.table-striped td::text').extract_first()

        yield{'title': title,
              'genre': genre,
              'price': price,
              'stock': stock,
              'upc': upc}
