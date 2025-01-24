from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Company, Job
from .serializers import CompanyCreateSerializer, CompanyDetailSerializer, CompanyEditSerializer, CompanyListSerializer, JobListSerializer, JobDetailSerializer


class JobViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        elif self.action == 'detail':
            return JobDetailSerializer
        return JobDetailSerializer
    

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return CompanyEditSerializer
              
        if self.action == 'list':
            return CompanyListSerializer
        if self.action == 'detail':
            return CompanyDetailSerializer
        return CompanyDetailSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
