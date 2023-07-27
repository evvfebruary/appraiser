import os

BOT_NAME = "fashion"

SPIDER_MODULES = ["fashion.spiders"]
NEWSPIDER_MODULE = "fashion.spiders"

DOWNLOADER_MIDDLEWARES = {
    "scrapeops_scrapy.middleware.retry.RetryMiddleware": 550,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
}

EXTENSIONS = {
    "scrapeops_scrapy.extension.ScrapeOpsMonitor": 500,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
MONGODB_PASS, MONGODB_USER = (
    os.environ["MONGODB_PASS"],
    os.environ["MONGODB_USER"],
)
TSUM_PARSER_SETTINGS = {
    "ITEM_PIPELINES": {
        "scrapy.pipelines.images.ImagesPipeline": 1,
        "fashion.fashion.pipelines.MongoPipeline": 2,
    },
    "MONGO_URI": f"mongodb://{MONGODB_USER}:{MONGODB_PASS}@127.0.0.1:28123/",
    "MONGO_DATABASE": "clothes",
    "IMAGES_STORE": "gs://dataswamp/fashion_images/",
    "GCS_PROJECT_ID": "datadogs",
}

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
SCRAPEOPS_API_KEY = os.environ["SCRAPEOPS_API_KEY"]
