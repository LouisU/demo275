# -*- coding: utf-8 -*-
from rest_framework import serializers
from users.models import VerifyCode
from demo275.settings import REGEX_MOBILE
from datetime import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
import re

User = get_user_model()


class SmsSerializer(serializers.Serializer):

    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile: 手机号码
        :return: 手机号
        """
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'mobile', 'email', 'is_active')


class UserRegSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=50, allow_null=True, allow_blank=True,
                                     label='电话',
                                     validators=[UniqueValidator(queryset=User.objects.all() , message="电话已经存在")]
                                     )
    password = serializers.CharField(style={'input_type': 'password'},help_text='密码', label='密码', write_only=True )
    code = serializers.CharField(
        required=True ,max_length=4, min_length=4, write_only=True,
        error_messages={
         "blank": "请输入验证码",
         "required": "请输入验证码",
         "max_length": "验证码格式错误",
         "min_length": "验证码格式错误"
     }, label='验证码')
    username = serializers.CharField(max_length=11, min_length=11, allow_blank=True, allow_null=True, default='', label='用户名')

    # 重新定义create方法，实现密码加密保存
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     # 上面的super()方法只是保证了用户创建，但是密码是显式的展现在数据库中的。
    #     # 接下来调用AbstractUser里面django自带的方法，set_password(), 可以将密码加密后存入数据库。
    #     user.set_password(validated_data['password'])
    #     user.save()  # 这样可以将显式的密码给覆盖掉
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['mobile']).order_by('-add_time')

        if verify_records.count():
            record = verify_records[0]

            # 验证时间是否过期
            one_mins_ago = datetime.now() - timedelta(minutes=1)
            if one_mins_ago > record.add_time:
                raise serializers.ValidationError('验证码过期')

            # 验证码是否相等
            if code != record.code:
                raise serializers.ValidationError('验证码错误')

        else:
            raise serializers.ValidationError('验证码错误')


    # validate()方法是在所有的validate_字段()方法结束之后，返回字段值。attrs字典类型。
    def validate(self, attrs):
        # 删除User model中没有的code字段。
        attrs["username"] = attrs["mobile"]
        del attrs["code"]

        return attrs


    class Meta:
        model = User
        fields = ('username', 'code', 'password', 'mobile')