# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins, generics, viewsets, status
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from random import choice
from users.models import VerifyCode
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码之前
    """

    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        code = self.generate_code()

        # Todo 发送短信验证码
        sms_result = True

        # 验证短信是否发送成功
        if sms_result:
            verify_code = VerifyCode(mobile=mobile, code=code)
            verify_code.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                # Todo 将短信发送失败的messageg替代"短信发送给失败"
                "mobile": "短信发送失败"
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin ,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    serializer_class = None
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = User.objects.all()

    # def get_queryset(self):   # 用这个方法，url中后面应该接user.id。 这样其实就在url中暴露了用户ID，不推荐
    #
    #     pk = int(self.kwargs['pk'])
    #     if pk == self.request.user.id:
    #         queryset = User.objects.filter(pk=pk)
    #         return queryset

    def get_object(self):   # 用这个方法， Url中不管接什么id, 都返回登录用户的信息。用户猜不到自己的ID. 推荐
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'retrieve':   # self.action 这个action只用用ViewSet才有， APIView没有。
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def get_permissions(self):

        if self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create()

        re_dict = serializer.data
        # 创建好用户信息之后生成Token
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        # return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
        # serializer.data 会返回到UserRegSerializer的fields中主键对应的值，
        # 但是在UserRegSerializer的validate方法中，已经把code字段删除了。
        # 所以用serializer.data会报错，说code没有这个键。

    def perform_create(self, serializer):
        return serializer.save()







