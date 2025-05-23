# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter # Ensure itemadapter is in requirements.txt
from src.models.items import BaseItem # Updated import path
from src.utils.redis_manager import RedisConnectionManager # Updated import path
import logging

logger = logging.getLogger(__name__)

class BasePipeline:
    # Renamed from baseSpiderPipeline to BasePipeline for better naming convention

    def __init__(self) -> None:
        # Consider making the Redis DB configurable, e.g., via settings
        self.redis = RedisConnectionManager().get_connection() 
        # It might be beneficial to pass the spider to the pipeline to access settings or other spider-specific attributes

    def open_spider(self, spider):
        # It's good practice to initialize resources like DB connections in open_spider
        # and close them in close_spider.
        # self.redis = RedisConnectionManager().get_connection(db=spider.settings.getint('REDIS_PIPELINE_DB', 0))
        logger.info(f"Opened spider {spider.name}, connected to Redis for pipeline.")

    def close_spider(self, spider):
        # Clean up resources, e.g., close DB connection if it's not managed by a pool that handles it automatically.
        # If RedisConnectionManager uses a connection pool, explicit closing might not be needed here for each connection.
        logger.info(f"Closed spider {spider.name}.")

    def process_item(self, item, spider):
        try:
            if isinstance(item, BaseItem):
                self.save_item(item, spider) # Pass spider to save_item if needed
                self.update_spider_stats(item, spider) # Renamed for clarity
            else:
                logger.warning(f"Item is not an instance of BaseItem: {type(item)}")
            return item
        except Exception as e:
            logger.error(f"Error processing item {item.get('url', 'Unknown URL')}: {e}", exc_info=True)
            # Depending on the error, you might want to drop the item or raise DropItem exception
            # from scrapy.exceptions import DropItem
            # raise DropItem(f"Error processing item: {e}")
            return item # Or re-raise to see it in Scrapy logs as an error

    def update_spider_stats(self, item, spider):
        # This method updates spider-specific statistics.
        # Ensure the spider instance has these attributes (successCount, failed_urls, add_url method)
        try:
            if hasattr(spider, 'successCount'):
                spider.successCount += 1
            
            # The logic for failed_urls and add_url seems more related to request/response tracking or bloom filter,
            # rather than a typical pipeline item processing stat. Consider if this is the right place.
            # If failed_urls is a list of URLs that failed and are now being processed successfully,
            # then removing it here makes sense.
            if hasattr(spider, 'failed_urls') and item.get('url') in spider.failed_urls:
                try:
                    spider.failed_urls.remove(item['url'])
                except ValueError:
                    logger.warning(f"URL {item.get('url')} not found in spider.failed_urls for removal.")

            if hasattr(spider, 'add_url') and callable(spider.add_url):
                # This seems like adding to a bloom filter or a similar seen-URLs set.
                # This is usually done in a spider middleware or the spider itself before yielding an item.
                spider.add_url(item['url'])
            logger.debug(f"Stats updated for item from {item.get('url')}")
        except Exception as e:
            logger.error(f"Error updating spider stats for item {item.get('url', 'Unknown URL')}: {e}", exc_info=True)
            # Not re-raising here to allow item processing to continue if stats update fails

    def save_item(self, item, spider): # Added spider parameter
        # Saves the item to Redis.
        try:
            item_dict = ItemAdapter(item).asdict() # Use ItemAdapter for robust conversion
            item_json = json.dumps(item_dict, ensure_ascii=False)
            
            # Get Redis list key from spider settings or use a default
            redis_list_key = getattr(spider, 'redis_key', spider.settings.get('PIPELINE_REDIS_KEY', 'default_result_list'))
            
            self.redis.lpush(redis_list_key, item_json)
            logger.info(f"Saved item from {item_dict.get('url')} to Redis list '{redis_list_key}'.")
        except Exception as e:
            logger.error(f"Error saving item {item.get('url', 'Unknown URL')} to Redis: {e}", exc_info=True)
            # Depending on policy, you might want to raise DropItem here
            # raise DropItem(f"Failed to save item to Redis: {e}")
