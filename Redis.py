# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================

import redis


class Redis:
    connection = None
    def __new__(cls, redis_uri="redis://localhost:6379"):
        if cls.connection is None:
            cls.connection = redis.Redis.from_url(redis_uri)
        return cls.connection
    
    def get_connection(self):
        return Redis.connection

# redis_instance = Redis()
