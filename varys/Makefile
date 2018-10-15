all:
	scrapy crawl sephora_sitemap_spider --set DOWNLOAD_DELAY=.25
debug:
	FEED_FORMAT=jsonlines scrapy crawl sephora_sitemap_spider -o items.jsonlines
