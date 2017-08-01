# scrapy crawl sephora_sitemap_spider -o items.json --set DOWNLOAD_DELAY=.25

import scrapy
from varys.items import SephoraProduct
from varys.items import SephoraReview
from datetime import datetime

#sitemap_urls = ['http://www.sephora.com/products-sitemap.xml']
class SephoraSitemapSpider(scrapy.Spider):
    name = 'sephora_sitemap_spider'
    start_urls = ['http://www.sephora.com/products-sitemap.xml']

    # Parse Functions
    def parse(self, res):
        res.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        for url in res.xpath('//d:loc/text()').extract():
            yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, res):
        raw_name = self.extract_first(res, '//meta[@itemprop="name"]/@content')
        (name, brand) = self.name_and_brand(raw_name)
        image_url = self.extract_first(res, '//meta[@itemprop="image"]/@content')
        sephora_id = self.extract_first(res, '//meta[@property="product:id"]/@content')
        yield SephoraProduct( brand=brand
                            , url=res.url
                            , image_url=image_url
                            , sephora_id=sephora_id
                            , name=name
                            , source=res.text
                            , scraped_at = str(datetime.now())
                            )
        yield scrapy.Request( self.review_url(sephora_id, '1')
                            , callback=self.parse_review
                            )

    def parse_review(self, res):
        sephora_id = res.url.split('/')[4]

        review_elements = res.selector.xpath('//span[@itemprop="review"]')
        review_extract = [r.xpath('descendant::text()').extract()
                for r in review_elements]
        reviews = [reduce(lambda x, acc: x + " " + acc,  text_list).strip()
                for text_list in review_extract]

        for review in reviews:
            yield SephoraReview( sephora_id=sephora_id
                               , text=review
                               , url=res.url
                               , scraped_at = str(datetime.now())
                               )

        url = self.review_url(sephora_id, self.next_page(res.url))
        if self.go_to_next_page(res):
            yield scrapy.Request(url, callback=self.parse_review)

    # Helper / Utility Functions
    def extract_first(self, res, path):
        return res.xpath(path).extract()[0]

    def go_to_next_page(self, res):
        script_tuples = [s.split(':') 
                for s in res.xpath('//script/text()').extract()[-1].split(',')]
        total_pages = int([script_tuple[1]
                for script_tuple in script_tuples
                if script_tuple[0] == '"numPages"'][0])
        next_page = int(self.next_page(res.url))
        print "total_pages %s" % total_pages
        print "next_page %s" % next_page
        return total_pages >= next_page

    def name_and_brand(self, raw_name):
        # 'Brazilian Bum Bum Cream - Sol de Janeiro | Sephora' 
        # => ('Brazilian Bum Bum Cream', 'Sol de Janeiro | Sephora')
        name_brand = [s.strip() for s in raw_name.split('|')[0].split('-')]
        name = " ".join(name_brand[0:-1])
        brand = name_brand[-1]
        return tuple([name, brand])

    def next_page(self, url):
        return str(int(url.split('=')[-1]) + 1)

    def review_url(self, sephora_id, page):
        return 'http://reviews.sephora.com/8723abredes/{}/reviews.htm?format=embedded&page={}'.format(sephora_id, page)
