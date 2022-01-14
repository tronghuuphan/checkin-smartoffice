from django_filters.filters import DateFilter, DateFromToRangeFilter
from django_filters.rest_framework import FilterSet
from .models import Log, ClassSH


class SimpleLogFilter(FilterSet):
    class Meta:
        model = Log
        fields = {
            "camera": ["exact"],
            "mask": ["exact"],
            "date": ["iexact", "gte", "lte"]
        }


class LogFilter(SimpleLogFilter):
    class Meta:
        model = SimpleLogFilter.Meta.model
        SimpleLogFilter.Meta.fields.update({"student": ["exact"]})
        fields = SimpleLogFilter.Meta.fields

class ClassSHFilter(FilterSet):
    class Meta:
        model = ClassSH
        fields = {
            "department": ["exact"],
        }
