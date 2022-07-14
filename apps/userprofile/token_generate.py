# -*- coding: utf-8 -*-
# @ModuleName: token_generate
# @Time: 2022/7/13 11:06
# @Author     : WangPengDa
# @Description:
# @Software   : PyCharm

import jwt
from DjangoTest.settings import dev


def TokenGenerate(userid, username, *args):
    """
    生成token
    :param userid:
    :param username:
    :param args:
    :return:
    """
    headers = {
        'typ': ' jwt',
        'alg': 'HS256'
    }
    payload = {
        'userid': userid,  # 用户表id
        'user_code': username  # 用户名
    }
    salt = dev.SECRET_KEY
    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
    return token

