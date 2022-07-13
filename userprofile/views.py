from django.db.models import Q
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from DjangoTest.common.redis_operate import set_token_to_redis
from DjangoTest.common.response import ResponseDict
from userprofile.models import UserProfile
from userprofile.serializers import UserSerializer
from userprofile.token_generate import TokenGenerate


class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    serializer_class = UserSerializer


class LoginView(APIView):
    queryset = UserProfile.objects.all().order_by('id')

    def post(self, request, *args, **kwargs):
        """
        登录并且获取token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        res = ResponseDict()
        data = request.data
        username = data.get('username')
        password = data.get('password')
        users = self.queryset.filter(Q(username=username) | Q(mobile=username))
        if not users.exists():
            raise NotFound('用户不存在')
        user = users.first()
        if not user.check_password(password):
            raise ValidationError('密码错误')
        # 手动签发token
        token = TokenGenerate(user.id, user.username)

        # 将token存到redis缓存中
        set_token_to_redis(token, user.id)
        res.traceId = request.traceId
        res.data = {
            "token": token,
            "userId": user.id,
            "userName": user.username
        }
        return Response(res)
