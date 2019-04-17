# -*- coding: utf-8 -*-
from django.shortcuts import render
from .serializers import StudentsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student
from rest_framework import status, mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .filters import StudentFilter

# Create your views here.


# class StudentsListView(APIView):
#     # 为了演示rest_framework框架提供的底层APIView的功能。 将get\post\delete\put等http协议的方法绑定
#     # 另外展示了rest_framework 序列化的方法
#     """
#     学生列表
#     """
#
#     def get(self, request):
#         students = Student.objects.all()[:20]
#
#         serializer = StudentsSerializer(students, many=True)
#
#         return Response(serializer.data)
#
#
#     def post(self, request):
#         serializer = StudentsSerializer(request.data)  # rest_framework的request.data中可以取到GET\POST\Body来的参数，非常方便
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StudentsListView(mixins.ListModelMixin, generics.GenericAPIView):
#
#     # 为了说明mixins模块generics模块
#     # 模块mixins中将get\post\delete\put方法与GET/POST/DELETE/PUT动作绑定，而且做了分页处理。
#     # 模块generics 处理了模型序列化的问题，过滤问题。更有更高级的继承了mixinx里面的类，使得更多更简便的使用GET|POST|DELETE|PUT
#     queryset = Student.objects.all()
#     serializer_class = StudentsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


###### 演示generics模块的LISTAPIView的用法： 继承了mixins.ListModelMixin 和 generics.GenericsAPIView类， 可以直接完成上面描述方法的功能。
###### 演示分页功能的使用。
class StudentsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


# class StudentsListView(generics.ListAPIView):
#
#     # 为了说明mixins模块generics模块
#     # 模块mixins中将get\post\delete\put方法与GET/POST/DELETE/PUT动作绑定，而且做了分页处理。
#     # 模块generics 处理了模型序列化的问题，过滤问题。更有更高级的继承了mixinx里面的类，使得更多更简便的使用GET|POST|DELETE|PUT
#     queryset = Student.objects.all()
#     serializer_class = StudentsSerializer
#     pagination_class = StudentsPagination


class StudentsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer
    pagination_class = StudentsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )
    # filterset_fields = ('name', 'card_physicalID')  # 这种过滤方式比较简单粗暴，比较弱。
    filterset_class = StudentFilter
    search_fields = ('name', 'card_physicalID')
    ordering_fields = ('name', 'card_physicalID')
    throttle_classes = (UserRateThrottle, AnonRateThrottle)


    # 演示了自己修改基类APIView的get_queryset()方法来实现数据过滤
    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases
    #     for the currently authenticated user.
    #     """
    #     queryset = Student.objects.all()
    #     students = queryset.filter(card_physicalID__isnull=True)
    #     return students

