# -*- coding: utf-8 -*-
from django.views.generic.base import View
from .models import Student


class StudentsListView(View):
    """
    获取学生列表
    """

    # def get(self, request):   # 说明django自带的View的功能是get请求和list的对应。但是序列化的问题没有处理

    #     students = Student.objects.all()[:20]
    #
    #     json_data = []
    #     for student in students:
    #         json_d = {}
    #         json_d['name'] = student.name
    #         json_d['sex'] = student.sex
    #         json_d['phone'] = student.phone
    #         json_d['card_physicalID'] = student.card_physicalID
    #         json_d['last_modified'] = student.last_modified  # django内建的View，没有处理时间的序列化的问题。
    #         json_data.append(json_d)
    #
    #     from django.http import HttpResponse
    #     import json
    #
    #     return HttpResponse(json.dumps(json_data), content_type='application/json')


    # def get(self, request):   # 在django自带的View的基础上，用model_to_dict转化，再序列化省了一些对应的代码。
    #                           # 但是model_to_dict将datetime和image field 过滤了， 还是没有很好的序列化。
    #     students = Student.objects.all()[:20]
    #
    #     from django.forms.models import model_to_dict
    #
    #     data_list = []
    #
    #     for student in students:
    #         data_list.append(model_to_dict(student))
    #
    #     from django.http import HttpResponse
    #     import json
    #
    #     return HttpResponse(json.dumps(data_list), content_type='application/json')


    def get(self, request):   # django.core自带的serializers模块有序列化的功能，但是还是有些复杂。
        students = Student.objects.all()[:20]

        from django.core import serializers
        students_json = serializers.serialize('json', students)

        from django.http import HttpResponse, JsonResponse

        # return HttpResponse(students_json, content_type='application/json')
        return JsonResponse(students_json, safe=False)