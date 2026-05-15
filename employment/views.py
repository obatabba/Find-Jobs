from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import filters
from rest_framework import status

from .filters import JobFilter
from .models import Application, Company, Employee, Job
from .serializers import *
from .services import ApplicationService
from .permissions import IsEmployee, IsEmployer, IsEmployerAndOwnerOrReadOnly, IsJobOwner, IsTheManager


class JobViewSet(ReadOnlyModelViewSet):
    queryset = Job.objects.select_related('company')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = JobFilter
    search_fields = ['title', 'tags__label']
    ordering_fields = ['salary', 'work_days', 'work_hours']
    ordering = ['-added']

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleJobSerializer
        if self.action == 'retrieve':
            return JobSerializer
        if self.action == 'apply':
            return ApplicationSerializer
        return EmptySerializer

    @action(detail=True, methods=['post'], permission_classes=[IsEmployee])
    def apply(self, request, pk):

        employee = request.user.employee
        job = get_object_or_404(Job, pk=pk)

        ApplicationService.apply(
            applicant=employee,
            job=job,
            data=request.data
        )

        return Response(
            {"success": "You have successfully applied to this job."},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[IsEmployee])
    def cancel_application(self, request, pk):
        employee = request.user.employee
        job = get_object_or_404(Job, pk=pk)

        ApplicationService.cancel_application(applicant=employee, job=job)

        return Response(
            {"success": "Your application has been canceled successfully."},
            status=status.HTTP_200_OK
        )


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.select_related('manager__user')
    permission_classes = [IsEmployerAndOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleCompanySerializer
        return CompanySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self.request.user, 'is_employer', False):
            context.update({'employer': self.request.user.employer})
        return context


class NestedJobViewSet(ModelViewSet):
    permission_classes = [IsTheManager]

    def get_queryset(self):
        return Job.objects.filter(company_id=self.kwargs['company_pk']).select_related('company__manager')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'POST']:
            return JobEditSerializer
        if self.action == 'list':
            return BasicJobSerializer
        if self.action == 'retrieve':
            return JobSerializer
        return JobSerializer

    def get_serializer_context(self):
        return {'company_id': self.kwargs['company_pk']}


class ApplicantsViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsJobOwner | IsAdminUser]

    def get_queryset(self):
        return Application.objects.filter(job_id=self.kwargs['job_pk']).select_related('applicant__address', 'applicant__user')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicationSerializer
        return SimpleApplicationSerializer


class EmployeeViewSet(ReadOnlyModelViewSet):
    queryset = Employee.objects.select_related('user')
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'expertise']
    ordering = ['user__first_name', 'user__last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicSimpleEmployeeSerializer
        if self.action == 'me':
            return EmployeeEditSerializer
        return PublicEmployeeSerializer

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsEmployee])
    def me(self, request):
        employee_profile = get_object_or_404(Employee, user_id=request.user.id)
        if request.method == 'GET':
            serializer = EmployeeEditSerializer(employee_profile, context={'request': request})
            return Response(serializer.data)
        if request.method in ['PUT', 'PATCH']:
            serializer = EmployeeEditSerializer(employee_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class EmployerViewSet(ReadOnlyModelViewSet):
    queryset = Employer.objects.select_related('user')
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name']
    ordering = ['user__first_name', 'user__last_name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployerSerializer
        if self.action == 'me':
            return EmployerSerializer
        return SimpleEmployerSerializer

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsEmployer])
    def me(self, request):
        employer_profile = get_object_or_404(Employer, user_id=request.user.id)
        if request.method == 'GET':
            serializer = EmployerSerializer(employer_profile)
            return Response(serializer.data)
        if request.method in ['PUT', 'PATCH']:
            serializer = EmployerSerializer(employer_profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
