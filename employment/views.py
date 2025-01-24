from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Job
from .serializers import JobListSerializer, JobDetailSerializer


class JobViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        elif self.action == 'detail':
            return JobDetailSerializer
        return JobDetailSerializer
