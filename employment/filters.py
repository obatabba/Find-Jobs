from django_filters import rest_framework as filters

from employment.models import Job


class JobFilter(filters.FilterSet):
    min_salary = filters.RangeFilter('salary')

    class Meta:
        model = Job
        fields = ['company', 'tags']