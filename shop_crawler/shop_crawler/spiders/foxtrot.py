import scrapy
import json
from ..items import ShopCrawlerItem


class FoxtrotSpider(scrapy.Spider):
    name = "foxtrot"
    allowed_domains = ["foxtrot.com.ua"]
    start_urls = ["https://www.foxtrot.com.ua/uk/shop/pylesosy.html", "https://www.foxtrot.com.ua/uk/shop/noutbuki_dell.html"]

    def parse(self, response, **kwargs):
        urls = response.css('div.listing__body-wrap div.card__image a::attr(href)').extract()
        for url in urls:
            print(url)
            yield scrapy.Request(
                url=response.urljoin(url),
                callback=self.parse_products,
                cb_kwargs={"breadcrumbs": response.xpath('//*[@id="breadcrumbs"]/div/ul/li[2]/a/text()').get()}
            )
        next_page = response.css('nav.listing__pagination ul li.listing__pagination-nav')[-1]
        if next_page is not None or len(next_page) != 0:
            page = next_page.attrib['data-page']
            yield scrapy.Request(
                url=f'{response.url.split("?")[0]}?page={page}',
                callback=self.parse,
                dont_filter=True
            )

    def parse_products(self, response, breadcrumbs):
        item = ShopCrawlerItem()
        item['url'] = response.url
        item['breadcrumbs'] = breadcrumbs.strip()
        item['name'] = response.css('h1.page__title').attrib['title']
        item['image'] = response.css('ul.product-img__list li.img picture.d-flex '
                                     'source.src-jpeg::attr(srcset)').getall()
        item['price'] = response.xpath('//*[@id="product-box-content"]/div[2]/div/div[3]/div[1]/'
                                       'div[2]/div[1]/div[2]/text()').get()
        item['rating'] = len(response.xpath(
            '//*[@id="product-box-content"]/div[2]/div/div[3]/div[1]/div[5]/div/div/i[contains(@class, "icon_orange")]').getall())

        item['characteristics'] = {
            "Гарантія": response.xpath('//*[@id="section-properties"]/div[1]/div/div/div[3]/span/a/text()').get()
        }
        for name, value in zip(response.xpath('//*[@id="product-card-props"]/div[2]/div/div[1]/text()').getall(),
                               response.xpath('//*[@id="product-card-props"]/div[2]/div/div[2]/text()').getall()):
            item['characteristics'][name.strip()] = value.strip()

        yield item
