all:
	scrapy crawl sephora_sitemap_spider --set DOWNLOAD_DELAY=.25
debug:
	scrapy crawl sephora_sitemap_spider -o items.json --set DOWNLOAD_DELAY=.25 --set FEED_FORMAT=jsonlines
