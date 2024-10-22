# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from baseSpider.items import BaseItem
from baseSpider.utils.RedisManage import RedisConnectionManager


class baseSpiderPipeline:

    def __init__(self) -> None:
        
        self.redis = RedisConnectionManager().get_connection()


    def process_item(self, item, spider):
        

        # 判断是否是BaseItem的实例
        if isinstance(item, BaseItem):
            
            # 保存item
            self.save_item(item,self.redis)
        
            # 更新标识
            self.calculate_flag(item, spider)

        else:
            print("不是BaseItem")

        return item
    

    def calculate_flag(self,item,spider):
        """
        计算flag值。
        
        Args:
            item (dict): 包含需要处理的数据的字典，其中必须包含'url'键。
            spider (Spider): Spider实例，用于操作相关属性。
        
        Returns:
            None
        
        """
        
         # 计算成功数量
        spider.successCount += 1

        # 将成功的url从失败的url中移除
        spider.failed_urls.remove(item['url'])

        # 将url插入到布隆过滤器
        spider.add_url(item['url'])
    

    def save_item(self,item,redis_conn):
        """
        将指定的item存入Redis列表。
        
        Args:
            item (tuple or list): 需要存储的项，其内容将被转换为字典。
            redis_conn (Redis): Redis连接对象，用于与Redis数据库进行交互。
        
        Returns:
            None
        
        """

        # 将item转换为字典
        item_dict = dict(item)
        # 将item_dict转换为json字符串
        item_json = json.dumps(item_dict,ensure_ascii=False)
        # 将item_json存入redis
        redis_conn.lpush('result', item_json)

        
    # def os_exit(self,spider):

    #     if spider.stop_flag:

    #         # 执行关闭爬虫
    #         spider.closed('max_failures')
    #         # 立即终止进程
    #         os._exit(1)