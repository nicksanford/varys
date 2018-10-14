all:
	scrapy crawl sephora_sitemap_spider --set DOWNLOAD_DELAY=.25
debug:
	FEED_FORMAT=jsonlines  scrapy crawl -L DEBUG --pdb  --set DOWNLOAD_DELAY=.25 -o items.json sephora_sitemap_spider
