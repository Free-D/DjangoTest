# -*- coding: utf-8 -*-
# @ModuleName: response
# @Time: 2022/7/13 9:45
# @Author     : WangPengDa
# @Description:
# @Software   : PyCharm


class DictClass(dict):

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        super().__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setattr__(key, value)
        super().__setitem__(key, value)


class ResponseDict(DictClass):
    """
    traceId: 唯一标识
    message: 友好提示
    errorMessage: 错误提示
    """
    __slots__ = ['traceId', "code", "data", "message", 'success', 'errorMessage']

    def __init__(self, data=None, trace_id=None, code=200, message="", success=True, error_message=""):
        super().__init__()
        self.traceId = trace_id
        self.code = code
        self.data = data
        self.message = message
        self.success = success
        self.errorMessage = error_message
