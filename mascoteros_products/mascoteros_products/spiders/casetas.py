# -*- coding: utf-8 -*-
import scrapy
from ..items import MascoterosProductsItem


class CasetasSpider(scrapy.Spider):
    name = 'casetas'
    page_num = 2
    start_urls = ['http://mascoteros.com/']

    def parse(self, response):

        if CasetasSpider.start_urls[0][-1] == '/':
            CasetasSpider.start_urls[0] = CasetasSpider.start_urls[0][:-1].replace('', '')

        url = response.css('.margin-top-20:nth-child(6) .menu-category-l3+ .menu-category-l3').xpath('@href').extract_first()
        casetas_url = CasetasSpider.start_urls[0] + url

        yield scrapy.Request(casetas_url, callback=self.parse_caseta_url)

    def parse_caseta_url(self, response):

        data = response.css('.product-card-content')
        caseta_url = data.css('div.list_name_prod_box').xpath('//a[contains(@href, "/my-dog-caseta-tela-desmontable")]/@href').extract_first()

        if caseta_url is not None:
            yield scrapy.Request(caseta_url, callback=self.parse_caseta)
        else:
            next_page = 'https://www.mascoteros.com/perros/en-casa/casetas?page=' + str(CasetasSpider.page_num)
            if CasetasSpider.page_num <= 8:
                CasetasSpider.page_num += 1
                yield response.follow(next_page, callback=self.parse_caseta_url)

    def parse_caseta(self, response):

        items = MascoterosProductsItem()
        rating = 0

        product_name = response.xpath('//h1[@class="product-title"]/span/text()')[0].extract()
        product_short_description = response.xpath('//p[@class="description"]//span[@itemprop="description"]/text()').extract()
        product_description_details = response.xpath('//span[@class="product-description"]/p//text()').extract()
        product_rating = response.xpath('//div[@class="col-md-12 no-padding-xs"]//div[@class="rating-stars"]//fieldset[@class="rating"]//*[contains(text(), "half") or (text(), "full")]//@class').extract()
        # product = response.xpath('//div[@class="col-md-12 no-padding-xs"]//div[@class="rating-stars"]//fieldset[@class="rating"]//@class').extract()
        # for item in product_rating:
        #     print(item)

        product_image_url = response.xpath('//div[@class="col-md-10 col-xs-10 col-sm-10 no-padding"]//img/@src')[0].extract()

        items['product_name'] = product_name
        items['product_short_description'] = ''.join(product_short_description).rstrip()
        items['product_description_details'] = ''.join(product_description_details).rstrip()
        items['product_rating'] = product_rating
        items['product_image_url'] = product_image_url

        yield items

