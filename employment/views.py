from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status

from .models import Company, Employee, Job
from .serializers import CompanyCreateSerializer, CompanySerializer, CompanyEditSerializer, JobEditSerializer, SimpleCompanySerializer, BasicJobSerializer, SimpleJobSerializer, JobSerializer, EmptySerializer


class JobViewSet(ReadOnlyModelViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleJobSerializer
        if self.action == 'retrieve':
            return JobSerializer
        return JobSerializer
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk):
        employee = Employee.objects.get(user_id=request.user.id)
        job = get_object_or_404(Job, pk=pk)
        if job in employee.applied_jobs.all():
            return Response(
                {"error":"You have already applied to this job."}, status=status.HTTP_400_BAD_REQUEST)

        job.applicants.add(employee)
        return Response({"success": "You have successfullt applied to this job"})


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyCreateSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return CompanyEditSerializer
              
        if self.action == 'list':
            return SimpleCompanySerializer
        if self.action == 'retrieve':
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
        if self.action == 'retrieve':
            return JobSerializer
        return JobSerializer
    
    def get_serializer_context(self):
        return {'company_id': self.kwargs['company_pk']}