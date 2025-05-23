import os
from dataclasses import dataclass
from typing import Optional

# This file can be used to load environment-specific configurations.
# For example, using python-dotenv to load a .env file:
# from dotenv import load_dotenv
# load_dotenv()

@dataclass
class RedisConfig:
    host: str = os.getenv('REDIS_HOST', 'localhost')
    port: int = int(os.getenv('REDIS_PORT', 6379))
    password: Optional[str] = os.getenv('REDIS_PASSWORD')
    db: int = int(os.getenv('REDIS_DB', 0))

@dataclass
class SpiderConfig:
    max_page: int = int(os.getenv('MAX_PAGE', 10))
    time_range: int = int(os.getenv('TIME_RANGE', 7))
    max_failures: int = int(os.getenv('MAX_FAILURES', 10))
