from typing import Any

import pymongo
from fashion.database.config import MONGO_INSERT_MODE, InsertModes
from fashion.database.handlers import insert_many, insert_one
from itemadapter import ItemAdapter


class MongoPipeline:
    INSERT_MODE = MONGO_INSERT_MODE
    collection_name = "scrapy_items"
    items_to_insert: list[dict[str, Any]] = []

    def __init__(self, mongo_uri, mongo_db, batch_size: int = 10):
        self.db_handlers = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.batch_size = batch_size
        self.db, self.client = None, None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db_handlers = {
            "mongo_db": self.client[self.mongo_db],
            "mongo_collection": self.collection_name,
        }

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Pay attention, this pipeline only can be last one in pipelines chain
        # ToDo: get into https://github.com/scrapy/scrapy/pull/3672/files if you wish that's fix badly
        item_as_dict = ItemAdapter(item).asdict()

        match self.INSERT_MODE:
            case InsertModes.MANY:
                buffer_params = {
                    "buffer": self.items_to_insert,
                    "buffer_size": self.batch_size,
                }
                insert_many(
                    item_as_dict,
                    **buffer_params,
                    **self.db_handlers,
                )
            case _:
                insert_one(item_as_dict, **self.db_handlers)
