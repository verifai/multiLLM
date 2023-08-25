# ==============================================================================
# Copyright 2023 VerifAI All Rights Reserved.
# https://www.verifai.ai
# License: 
#
# ==============================================================================

import redis
import json
import os

if os.getenv("REDIS_URI"):
    REDIS_URI = os.getenv("REDIS_URI")
else:
    REDIS_URI = "redis://localhost:6379"
    
class Redis:
    connection = None
    def __new__(cls, redis_uri=REDIS_URI):
        if cls.connection is None:
            cls.connection = redis.Redis.from_url(redis_uri)
        return cls.connection
    
    def get_connection(self):
        return Redis.connection
    
    @staticmethod
    def publish_to_redis(type="multillm", taskid=None, result=None, meta_data=None):
        redis_conn = Redis.connection
        if redis_conn == None:
            return
        res = {"type": type, "taskId": taskid, "result" : result, "meta_data": meta_data }
        payload = json.dumps(res)
        try:
            redis_conn.publish(type, payload)
        except Exception as e:
            print('(MultiLLM:publish_to_redis()) could not publish to redis: {0}' .format(str(e)))

redis_instance = Redis()
