from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import Company, Job
from .serializers import CompanyCreateSerializer, CompanySerializer, CompanyEditSerializer, JobEditSerializer, SimpleCompanySerializer, BasicJobSerializer, SimpleJobSerializer, JobSerializer


class JobViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleJobSerializer
        if self.action == 'detail':
            return JobSerializer
        return JobSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return CompanyEditSerializer
              
        if self.action == 'list':
            return SimpleCompanySerializer
        if self.action == 'detail':
            return CompanySerializer
        return CompanySerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class NestedJobViewSet(ModelViewSet):

    def get_queryset(self):
        return Job.objects.filter(company_id=self.kwargs['company_pk'])

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return JobEditSerializer
        if self.action == 'list':
            return BasicJobSerializer
        if self.action == 'detail':
            return JobSerializer
        return JobSerializer
    
    def get_serializer_context(self):
        return {'company_id': self.kwargs['company_pk']}