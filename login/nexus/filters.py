import django_filters

from . models import *
 

class OrderFilter(django_filters.FilterSet):
    class Meta :
        model= VoltageData
        fields='__all__'