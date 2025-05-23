import re
from datetime import datetime, date
import logging
import time
import datetime as dt

logger = logging.getLogger(__name__)

class TimeUtils:
    def __init__(self, time_range_days: int = 7):
        self.time_range_days = time_range_days
        self.crawl_today = date.today()

    def is_time_out(self, time_obj: datetime) -> bool:
        """
        判断给定的时间是否超出了设定的时间范围。
        Args:
            time_obj (datetime.datetime): 待判断的时间点。
        Returns:
            bool: 若给定的时间点超出了设定的时间范围，则返回True；否则返回False。
        """
        if not isinstance(time_obj, datetime):
            logger.warning(f"Invalid type for time_obj: {type(time_obj)}. Expected datetime.")
            # 根据业务逻辑决定是返回True, False还是抛出异常
            return True # 假设无效输入视为超时
        return abs((time_obj.date() - self.crawl_today).days) > self.time_range_days

    @staticmethod
    def extract_date_from_string(string: str) -> str | None:
        """
        从字符串中提取 YYYY-MM-DD 格式的日期。
        Args:
            string (str): 待提取的字符串。
        Returns:
            str | None: 提取出的日期字符串，如果找不到则返回None。
        """
        if not isinstance(string, str):
            return None
        match = re.search(r'\d{4}-\d{2}-\d{2}', string)
        return match.group() if match else None

    @staticmethod
    def format_string_to_datetime(publish_time_str: str, date_format='%Y-%m-%d') -> datetime | None:
        """
        格式化日期字符串，将其转换为 datetime 对象。
        Args:
            publish_time_str (str): 日期字符串。
            date_format (str): 日期字符串的格式。
        Returns:
            datetime | None: 格式化后的 datetime 对象，如果格式错误则返回None。
        """
        if not isinstance(publish_time_str, str):
            return None
        try:
            return datetime.strptime(publish_time_str, date_format)
        except ValueError:
            logger.error(f"Time format error for: {publish_time_str} with format {date_format}")
            return None

    @staticmethod
    def clean_and_extract_date_str(publish_time: str) -> str | None:
        """
        清理常见的日期字符串中的干扰字符，并提取 YYYY-MM-DD 格式。
        Args:
            publish_time (str): 原始时间字符串。
        Returns:
            str | None: 清理并提取后的日期字符串，或None。
        """
        if not isinstance(publish_time, str):
            return None
        
        # 替换常见分隔符和中文字符
        replacements = {
            '(': '-', ')': '-', '/': '-', ' ': '',
            '.': '-', '[': '', ']': '',
            '年': '-', '月': '-', '日': ''
        }
        for old, new in replacements.items():
            publish_time = publish_time.replace(old, new)
        
        # 提取日期部分
        extracted_date = TimeUtils.extract_date_from_string(publish_time)
        
        if extracted_date and len(extracted_date) > 10:
            return extracted_date[:10]
        return extracted_date

    def is_stopping_condition_met(self, publish_time_str: str) -> bool:
        """
        判断根据发布时间字符串是否满足爬虫停止条件（如超时）。
        Args:
            publish_time_str (str): 发布时间字符串。
        Returns:
            bool: 如果满足停止条件则返回True，否则返回False。
        """
        cleaned_date_str = self.clean_and_extract_date_str(publish_time_str)
        if not cleaned_date_str:
            logger.warning(f"Could not parse date from: {publish_time_str}")
            return True # 无法解析日期，视为满足停止条件或按需处理
            
        datetime_obj = self.format_string_to_datetime(cleaned_date_str)
        if not datetime_obj:
            return True # 日期格式错误，视为满足停止条件
            
        return self.is_time_out(datetime_obj)

    @staticmethod
    def compare_datetime_strings(time_str1: str | None, time_obj2: datetime | None) -> bool:
        """
        比较一个日期时间字符串和一个datetime对象。
        Args:
            time_str1 (str | None): 第一个时间字符串 (YYYY-MM-DD)。如果为空或None，视为小于time_obj2。
            time_obj2 (datetime | None): 第二个datetime对象。如果为None，time_str1不为空则视为大于。
        Returns:
            bool: 如果 time_obj2 代表的时间晚于 time_str1 代表的时间，则返回 True。
                  如果任一输入为None或无效，会进行相应处理。
        """
        if time_obj2 is None:
            return False # time_obj2 无效，无法比较，或根据需求定义行为
        if time_str1 is None or time_str1 == '':
            return True # time_str1 无效或为空，视为 time_obj2 更晚

        try:
            datetime_obj1 = datetime.strptime(time_str1, '%Y-%m-%d')
            return time_obj2 > datetime_obj1
        except ValueError:
            logger.warning(f"Invalid date format for time_str1: {time_str1}")
            return True # time_str1 格式错误，根据需求可能视为 time_obj2 更晚

def get_current_timestamp():
    """获取当前时间戳"""
    return int(time.time())

def get_current_datetime_str(format_str="%Y-%m-%d %H:%M:%S"):
    """获取当前格式化的日期时间字符串"""
    return dt.datetime.now().strftime(format_str)

def timestamp_to_datetime_str(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
    """时间戳转换为格式化的日期时间字符串"""
    return dt.datetime.fromtimestamp(timestamp).strftime(format_str)

def str_to_timestamp(date_str, format_str="%Y-%m-%d %H:%M:%S"):
    """日期时间字符串转换为时间戳"""
    return int(time.mktime(dt.datetime.strptime(date_str, format_str).timetuple()))
