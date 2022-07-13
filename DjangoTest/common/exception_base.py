# -*- coding: utf-8 -*-
# @ModuleName: exception_base
# @Time: 2022/7/13 9:44
# @Author     : WangPengDa
# @Description:
# @Software   : PyCharm
import logging
import traceback

from django.db import connection, transaction
from django.http import Http404
from rest_framework import exceptions
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

from DjangoTest.common.response import ResponseDict


class ErrorDetail(str):
    """
    错误详情
    """
    code = None

    def __new__(cls, message, error_message, code):
        self = super().__new__(cls, message)
        self.code = code
        self.error_message = error_message
        return self

    def __eq__(self, other):
        r = super().__eq__(other)
        if r is NotImplemented:
            return NotImplemented
        try:
            return r and self.code == other.code
        except AttributeError:
            return r

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))


class ProjectException(Exception):
    """
    异常基类
    """
    default_message = '内部服务器错误'
    default_code = 500

    def __init__(self, message=None, error_message=None, code=None):
        self.detail = self._get_error_details(message, error_message, code)

    def __str__(self):
        return str(self.detail)

    def _get_error_details(self, message, error_message, code):
        if message is None:
            message = self.default_message
        if code is None:
            code = self.default_code
        return ErrorDetail(message, error_message, code)

    def get_codes(self):
        """
        获取错误码
        """
        return self.detail.code

    def get_full_details(self):
        """
        获取错误的全部信息
        """
        return {
            'code': self.detail.code,
            'message': self.detail,
            'errorMessage': self.detail.error_message
        }

    def export_return_dict(self):
        res = ResponseDict()
        res.code = self.detail.code
        res.message = self.detail
        res.errorMessage = self.detail.error_message
        res.success = False
        return res


def custom_exception_handler(exc, context):
    """
    将 ref 处理过的异常封装为需要的格式 视图函数的其他异常由中间件去处理
    :param exc: 异常
    :param context: 抛出异常的上下文
    :return: Response 响应对象
    """
    res = ResponseDict()
    request = context.get("request")
    log = logging.getLogger(request.path_info.split("/")[1])
    log.error(f"{request.traceId}--{traceback.format_exc()}")
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.ValidationError):
        res.message = "参数校验错误"
        res.errorMessage = exc.detail
        res.code = exc.status_code
    elif isinstance(exc, exceptions.APIException):
        # 其他 drf 异常
        res.message = "服务器内部错误"
        res.errorMessage = exc.detail
        res.code = exc.status_code

    elif isinstance(exc, ProjectException):
        res = exc.export_return_dict()
        res.traceId = getattr(request, "traceId", None)
        return Response(res)
    else:
        # 手动抛出的异常 value
        res.message = str(exc)
        res.errorMessage = str(exc)
        res.code = 500
    request = context.get("request")
    res.traceId = getattr(request, "traceId", None)
    set_rollback()
    return Response(res, status=200)


def set_rollback():
    """
    暂不知道有什么用
    :return:
    """
    atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)
