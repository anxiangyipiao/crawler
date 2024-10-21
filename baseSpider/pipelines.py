# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from baseSpider.items import BaseItem
from baseSpider.utils.RedisManage import RedisConnectionManager


class BasePipeline:

    def __init__(self) -> None:
        
        self.redis = RedisConnectionManager().get_connection()


    def process_item(self, item, spider):
        

        print("开始处理item")
        # 判断是否是BaseItem的实例
        if isinstance(item, BaseItem):
            
            # 保存item
            self.save_item(item)
        
            # 更新标识
            self.calculate_flag(item, spider)

        else:
            print("不是BaseItem")

        return item
    

    def calculate_flag(self,item,spider):
        
         # 计算成功数量
        spider.successCount += 1

        # 将成功的url从失败的url中移除
        spider.failed_urls.remove(item['url'])

        # 将url插入到布隆过滤器
        spider.add_url(item['url'])
    

    def save_item(self,item):

        # 将item转换为字典
        item_dict = dict(item)
        # 将item_dict转换为json字符串
        item_json = json.dumps(item_dict)
        # 将item_json存入redis
        self.redis.lpush('result', item_json)

        
    # def os_exit(self,spider):

    #     if spider.stop_flag:

    #         # 执行关闭爬虫
    #         spider.closed('max_failures')
    #         # 立即终止进程
    #         os._exit(1)