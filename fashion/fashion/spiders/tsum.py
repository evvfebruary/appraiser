import re

import scrapy
from dotenv import load_dotenv

from fashion.fashion.items import FashionItem
from fashion.fashion.settings import TSUM_PARSER_SETTINGS

load_dotenv()


class TsumSpider(scrapy.Spider):
    name = "tsum_brands"
    start_urls = [f"https://www.tsum.ru/catalog/zhenskoe-18368/"]
    page_number_pattern = r"\/catalog\/zhenskoe-18368\/\?page=(\d+)"
    PAGES_DEFAULT = 1_000

    custom_settings = TSUM_PARSER_SETTINGS

    def parse(self, response, **kwargs):
        last_page_element = (
            response.css(".styles_numberBtn__9dddfa14")
            .xpath("@href")
            .getall()[-1]
        )
        last_page_finder = re.search(
            self.page_number_pattern, last_page_element
        )
        page_count = (
            int(last_page_finder.group(1)) + 1
            if last_page_finder
            else self.PAGES_DEFAULT
        )
        self.logger.info(f"Page count equal: {page_count}")
        yield from response.follow_all(
            [
                self.start_urls[0] + f"?page={page}"
                for page in range(1, page_count)
            ],
            callback=self.parse_page,
        )

    def parse_page(self, response, **kwargs):
        all_products_from_page = (
            response.css(".style__link___vsiWz").xpath("@href").getall()
        )
        yield from response.follow_all(
            all_products_from_page, callback=self.parse_product
        )

    def parse_product(self, response, **kwargs):
        info_section = (
            response.css(".style__infoBlock___N1KdA ul")
            .xpath("li//text()")
            .getall()
        )
        categories = (
            response.css(".style__breadcrumbs___dbDQw li a")
            .xpath("@href")
            .getall()
        )
        prices = (
            response.css(".style__price___l9Hm2 span").xpath("text()").extract()
        )
        description = (
            response.css(".style__infoBlock___N1KdA p").xpath("text()").get()
        )
        img_links = (
            response.css('.slick-track div[data-index="0"] img')
            .xpath("@src")
            .getall()
        )

        if img_links:
            img_links = img_links[:1]

        return FashionItem(
            info_section=info_section,
            categories=categories,
            prices=prices,
            description=description,
            image_urls=img_links,
            source_url=response.url,
        )
