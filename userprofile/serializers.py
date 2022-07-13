from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    # style表示前台输入是密文，write_only表示序列化时不会序列化该字段
    password = serializers.CharField(write_only=True, max_length=256)

    class Meta:
        model = UserProfile
        fields = "__all__"

    # 创建用户时更新密码为密文
    def create(self, validated_data):
        user = super().create(validated_data)
        password = make_password(validated_data['password'])
        user.password = password
        user.save()
        return user

    # 更新用户时更新密码为密文
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = make_password(validated_data['password'])
        if 'password' in validated_data.keys():
            user.password = password
        user.save()
        return user

    # 重写to_representation方法，自定义响应中的json数据
    def to_representation(self, instance):
        # 返回结果中id字段中间有横线，需要去除
        ret = super().to_representation(instance)
        return ret
