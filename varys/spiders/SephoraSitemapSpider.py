# scrapy crawl sephora_sitemap_spider -o items.json --set DOWNLOAD_DELAY=.25 --set FEED_FORMAT=jsonlines

from scrapy import Spider, Request
from varys.items import SephoraProduct, SephoraReview
from datetime import datetime
from functools import reduce

from ..parsers import review_json

import logging
logger = logging.getLogger(__name__)

REVIEW_URL_TEMPLATE = 'http://reviews.sephora.com/8723abredes/{sephora_id}/reviews.htm?format=embedded&page={page}'

class SephoraSitemapSpider(Spider):
    name = 'sephora_sitemap_spider'
    start_urls = ['http://www.sephora.com/products-sitemap.xml']

    # Parse Functions
    def parse(self, response):
        response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        for url in response.xpath('//d:loc/text()').extract():
            logger.info("processing url %s", url)
            yield Request(url, callback=self.parse_product)

    def parse_product(self, response):
        # Formatted like this: 'Sephora: NARS : Single Eye Shadow : eyeshadow'
        raw_title = response.xpath('//meta[@property="og:title"]/@content').extract_first()
        if raw_title:
            try:
                _, brand, name, category = [item.strip() for item in raw_title.split(':')]
            except Exception as e:
                logger.error("exception %s", str(e))
                logger.error("raw_title %s", raw_title)
                raise e
            image_url = response.xpath('//meta[@property="og:image"]/@content').extract_first()
            sephora_id = response.xpath('//meta[@property="product:id"]/@content').extract_first()

            yield SephoraProduct( brand=brand
                                , url=response.url
                                , image_url=image_url
                                , sephora_id=sephora_id
                                , name=name
                                , source=response.text
                                , category=category
                                , scraped_at = str(datetime.now())
                                )
            yield Request( REVIEW_URL_TEMPLATE.format(sephora_id=sephora_id, page='1')
                         , callback=self.parse_review
                         )

    def parse_review(self, response):
        sephora_id = response.url.split('/')[4]

        review_elements = response.selector.xpath('//span[@itemprop="review"]')

        review_extract = [r.xpath('descendant::text()').extract() for r in review_elements]

        reviews = [reduce(lambda x, acc: x + " " + acc,  text_list).strip()
                   for text_list in review_extract]

        for review in reviews:
            yield SephoraReview( sephora_id=sephora_id
                               , text=review
                               , url=response.url
                               , scraped_at=str(datetime.now())
                               , review_json=review_json.from_review(review)
                               )

        url = REVIEW_URL_TEMPLATE.format( sephora_id=sephora_id
                                        , page=self.next_page(response.url)
                                        )

        if self.go_to_next_page(response):
            yield Request(url, callback=self.parse_review)

    def go_to_next_page(self, response):
        raw_script_text = response.xpath('//script/text()').extract()[-1]
        if '"numPages"' in raw_script_text:

            script_tuples = [s.split(':') for s in raw_script_text.split(',')]
            try:
                total_pages = int([element[1] for element in script_tuples
                                          if element[0] == '"numPages"'][0])
            except Exception as e:
                logger.error("exception %s", str(e))
                logger.error("script_tuples %s", script_tuples)
                raise e
            next_page = int(self.next_page(response.url))
            logger.info("total_pages %s", total_pages)
            logger.info("next_page %s", next_page)
            return total_pages >= next_page

        else:
            return False

    def next_page(self, url):
        return str(int(url.split('=')[-1]) + 1)
