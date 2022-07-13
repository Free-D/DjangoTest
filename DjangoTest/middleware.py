# -*- coding: utf-8 -*-
# @ModuleName: middleware
# @Time: 2022/7/13 9:42
# @Author     : WangPengDa
# @Description:
# @Software   : PyCharm
import asyncio
import sys
import time
import logging
import threading
import traceback

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from DjangoTest.common.exception_base import ProjectException
from DjangoTest.common.response import ResponseDict


class ExceptionMiddleWare(MiddlewareMixin):
    """
    该中间件给每个请求加一个编号 该请求中发生的异常都使用该编号
    """

    timer = 0

    def process_request(self, request):
        log = logging.getLogger(request.path_info.split("/")[1])
        log.info("-------------------------------------------")
        log.info(f"{request.method} {request.path_info}")
        par = request.GET or request.POST or request.body
        if isinstance(par, bytes):
            par = par.decode()
        log.info(f"{par}")
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        log.info(f"ip: {ip}")
        request.traceId = self.get_trace_id()
        self.timer = time.time()

    def process_exception(self, request, exc):
        log = logging.getLogger(request.path_info.split("/")[1])
        log.error(f"{request.traceId}--{traceback.format_exc()}")
        if isinstance(exc, ProjectException):
            res = exc.export_return_dict()
            res.traceId = request.traceId
            return JsonResponse(res)
        else:
            res = ResponseDict()
            res.traceId = request.traceId
            res.code = 500
            res.message = "服务器内部错误"
            res.success = False
            exc_type, exc_value, exc_obj = sys.exc_info()
            res.errorMessage = f"{exc_type}:{exc_value}"
            return JsonResponse(res)

    def process_response(self, request, response):
        log = logging.getLogger(request.path_info.split("/")[1])
        log.info(f"耗时：{(time.time() - self.timer) * 1000} ms")
        log.info("***************************************")
        return response

    def get_trace_id(self):
        t = threading.currentThread()
        return f"{t.ident}-{time.time() * 1000}"
