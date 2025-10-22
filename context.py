import redis.asyncio as redis
from dreema.helpers import getenv
# from urllib.parse import quote

class AppContext:
    def __init__(self):
        pass
        # try:
        #     self.redis = redis.Redis(   
        #                                 host=getenv("REDIS_HOST"),
        #                                 port=int(getenv("REDIS_PORT")),
        #                                 password=getenv("REDIS_PASSWORD"),
        #                                 decode_responses=True  # makes sure values are strings instead of bytes
        #                             )
        # except:
        #     self.redis = None