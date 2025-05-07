# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from baseSpider.items import BaseItem
from baseSpider.utils.RedisManage import RedisConnectionManager
import logging

logger = logging.getLogger(__name__)

class baseSpiderPipeline:

    def __init__(self) -> None:
        self.redis = RedisConnectionManager().get_connection()

    def process_item(self, item, spider):
        try:
            if isinstance(item, BaseItem):
                self.save_item(item, self.redis)
                self.calculate_flag(item, spider)
            else:
                logger.warning("Item is not an instance of BaseItem")
            return item
        except Exception as e:
            logger.error(f"Error processing item: {e}")
            raise

    def calculate_flag(self, item, spider):
        try:
            spider.successCount += 1
            spider.failed_urls.remove(item['url'])
            spider.add_url(item['url'])
        except Exception as e:
            logger.error(f"Error calculating flag: {e}")
            raise

    def save_item(self, item, redis_conn):
        try:
            item_dict = dict(item)
            item_json = json.dumps(item_dict, ensure_ascii=False)
            redis_conn.lpush('result', item_json)
        except Exception as e:
            logger.error(f"Error saving item to Redis: {e}")
            raise
