# -*- coding: utf-8 -*-
import scrapy
from ..items import MascoterosProductsItem


class VerseleLagaSpider(scrapy.Spider):
    name = 'versele-laga'
    page_num = 2
    start_urls = ['http://mascoteros.com/']

    def parse(self, response):

        if VerseleLagaSpider.start_urls[0][-1] == '/':
            VerseleLagaSpider.start_urls[0] = VerseleLagaSpider.start_urls[0][:-1].replace('', '')

        url = response.xpath('//div[@class="row category-menu category-pajaros hidden"]//a[contains(@href,"/comida-loros")]//@href').get()
        versele_laga = VerseleLagaSpider.start_urls[0] + url

        yield scrapy.Request(versele_laga, callback=self.parse_versele_laga_marca)

    def parse_versele_laga_marca(self, response):

        if VerseleLagaSpider.start_urls[0][-1] == '/':
            VerseleLagaSpider.start_urls[0] = VerseleLagaSpider.start_urls[0][:-1].replace('', '')

        versele_laga_marca = response.css('div.list_name_prod_box').xpath('//a[contains(@href,"/versele-laga-p15-original-pienso-papagayos-10-kg")]/@href').get()

        if versele_laga_marca is not None:
            yield scrapy.Request(versele_laga_marca, callback=self.parse_versele_laga_item)
        else:
            next_page = 'https://www.mascoteros.com/pajaros/alimentacion/comida-loros?page=' + str(VerseleLagaSpider.page_num)
            if VerseleLagaSpider.page_num <= 8:
                VerseleLagaSpider.page_num += 1
                yield response.follow(next_page, callback=self.parse_versele_laga_marca)


    def parse_versele_laga_item(self, response):

        items = MascoterosProductsItem()
        rating = 0

        product_name = response.xpath('//*[@id="productPage"]/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/h1/span/text()')[0].extract()
        product_short_description = response.xpath('//p[@class="description"]//span[@itemprop="description"]/text()').extract()
        product_description_details = response.xpath('//span[@class="product-description"]/p//text()').extract()
        product_rating = response.xpath('count(//div[@class="col-md-12 no-padding-xs"]//div[@class="rating-stars"]//span[position() = 1])').get()
        product_image_url = response.xpath('//div[@class="col-md-10 col-xs-10 col-sm-10 no-padding"]//img/@src')[0].extract()

        items['product_name'] = product_name
        items['product_short_description'] = ''.join(product_short_description).strip()
        items['product_description_details'] = ''.join(product_description_details).strip()
        items['product_rating'] = product_rating
        items['product_image_url'] = product_image_url

        yield items