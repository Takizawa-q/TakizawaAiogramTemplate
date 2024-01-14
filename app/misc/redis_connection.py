from redis import asyncio as aioredis
from app.config import config

redis = aioredis.Redis(host=config.redis.host,
                       port=config.redis.port,
                       decode_responses=True)