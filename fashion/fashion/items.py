import scrapy


class FashionItem(scrapy.Item):
    source_url = scrapy.Field()
    info_section = scrapy.Field()
    categories = scrapy.Field()
    prices = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
