import redis
from src.config.settings import BLOOMFILTER_KEY # Updated import
from datetime import datetime
from functools import lru_cache
from src.utils.redis_manager import RedisConnectionManager # Updated import
from src.config.settings import Expected_items, False_positive_rate # Updated import

# RedisBloom 命令前缀
BF_RESERVE_CMD = 'BF.RESERVE'
BF_ADD_CMD = 'BF.ADD'
BF_EXISTS_CMD = 'BF.EXISTS'

class RedisBloomFilter(object):
    
    def __init__(self, expected_items, false_positive_rate, key=None, db=0):
        """
        初始化 RedisBloomFilter 实例。
        
        Args:
            expected_items (int): 预计插入布隆过滤器的元素数量。
            false_positive_rate (float): 误报率，取值范围在0到1之间。
            key (str, optional): 布隆过滤器在Redis中的key。默认为"BLOOMFILTER_KEY"。
            db (int, optional): Redis 数据库编号，默认为 REDIS_DB。
        
        Raises:
            ValueError: 如果误报率不在0到1之间或预计插入的元素数量小于0，则抛出此异常。
        """
        if not (0 < false_positive_rate < 1):
            raise ValueError("False positive rate must be between 0 and 1")
        if expected_items < 0:
            raise ValueError("Expected items count must be non-negative")

        self.server = RedisConnectionManager.get_connection(db)
        self.key = self.get_monthly_key(BLOOMFILTER_KEY if key is None else key)
        self._initialize(expected_items, false_positive_rate)

    def _initialize(self, expected_items, false_positive_rate):
        """
        在 Redis 中预留一个布隆过滤器。
        
        Args:
            expected_items (int): 预计插入布隆过滤器的元素数量。
            false_positive_rate (float): 误报率，取值范围在0到1之间。
        """
        
        if not self.server.exists(self.key):
               self.server.execute_command(BF_RESERVE_CMD, self.key, false_positive_rate, expected_items)
        else:
                print(f"Bloom filter is already created: {self.key}")    
       

    def is_contained(self, str_input):
        """
        判断字符串是否可能存在于过滤器中。
        
        Args:
            str_input (str): 待判断的字符串。
        
        Returns:
            bool: 如果字符串可能存在于过滤器中，则返回True；否则返回False。
        """
        try:
            return self.server.execute_command(BF_EXISTS_CMD, self.key, str_input)
        except redis.exceptions.RedisError as e:
            print(f"Error checking item existence: {e}")
            return False

    def add(self, str_input):
        """
        向过滤器中添加一个元素。
        
        Args:
            str_input (str): 待添加的字符串元素。
        """
        try:
            self.server.execute_command(BF_ADD_CMD, self.key, str_input)
        except redis.exceptions.RedisError as e:
            print(f"Error adding item: {e}")

    @staticmethod
    def get_monthly_key(key):
        """
        根据当前月份重置布隆过滤器key。
        
        Args:
            key (str): 需要重置的布隆过滤器key。
        
        Returns:
            str: 拼接当前月份后的布隆过滤器key。
        """
        now = datetime.now()
        return f"{key}:{now.year}:{now.month}"


# 示例使用，如果需要，可以取消注释或移至实际使用处
# bloomFilter = RedisBloomFilter(expected_items=Expected_items, false_positive_rate=False_positive_rate, key=BLOOMFILTER_KEY)
