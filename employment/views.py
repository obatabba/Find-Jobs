from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import status

from .models import Application, Company, Employee, Job
from .serializers import *
from .permissions import IsEmployee, IsEmployer, IsEmployerOrReadOnly, IsJobOwner, IsTheManager


class JobViewSet(ReadOnlyModelViewSet):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleJobSerializer
        if self.action == 'retrieve':
            return JobSerializer
        if self.action == 'apply':
            return ApplicationCreateSerializer
        return EmptySerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == 'apply':
            context.update({
                'applicant_id': self.request.user.employee.id,
                'job_id': self.kwargs['pk']
            })
        return context 

    @action(detail=True, methods=['post'], permission_classes=[IsEmployee])
    def apply(self, request, pk):
        employee = Employee.objects.get(user_id=request.user.id)
        job = get_object_or_404(Job, pk=pk)

        if Application.objects.filter(applicant=employee, job=job).exists():
            return Response(
                {"error":"You have already applied to this job."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ApplicationCreateSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "You have successfully applied to this job."})

    @action(detail=True, methods=['post'], permission_classes=[IsEmployee])
    def cancel_application(self, request, pk):
        employee = Employee.objects.get(user_id=request.user.id)
        job = get_object_or_404(Job, pk=pk)
        application = Application.objects.filter(applicant=employee, job=job)
        if application.exists():
            application.delete()
            return Response(
                {"success": "Your application has been canceled successfully."})

        return Response({"error": "You have not applied to this job."}, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsEmployerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleCompanySerializer
        return CompanySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self.request.user, 'is_employer', False):
            context.update({'employer_id': self.request.user.employer.id})
        return context


class NestedJobViewSet(ModelViewSet):
    permission_classes = [IsTheManager]

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


class ApplicantsViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsJobOwner | IsAdminUser]

    def get_queryset(self):
        return Application.objects.filter(job_id=self.kwargs['job_pk'])

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ApplicationSerializer
        return SimpleApplicationSerializer


class EmployeeViewSet(ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [IsAuthenticated]

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
    queryset = Employer.objects.all()
    permission_classes = [IsAdminUser]

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
