
from django_filters import rest_framework as filters
from .models import Student




class StudentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')
    card_physicalID = filters.CharFilter(field_name="card_physicalID", lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name', 'card_physicalID']