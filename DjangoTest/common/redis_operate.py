# -*- coding: utf-8 -*-
# @ModuleName: redis_operate
# @Time: 2022/7/13 11:43
# @Author     : WangPengDa
# @Description:
# @Software   : PyCharm

import json

from django_redis import get_redis_connection
from redis import Redis

PROJECT = "DjangoTest"

def get_token_from_redis(token):
    """
    :return:
    """
    conn: Redis = get_redis_connection()
    return conn.get(f"{PROJECT}:token:{token}")


def set_token_to_redis(token, user_info):
    conn: Redis = get_redis_connection()
    conn.set(f"{PROJECT}:token:{token}", json.dumps(user_info, ensure_ascii=False), ex=60 * 60 * 2)
