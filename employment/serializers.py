from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import Application, Company, Employee, Job, User


class UserSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account_type']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'account_type']


class BasicJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'title']


class SimpleJobSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'company']


class JobSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    def create(self, validated_data):
        instance = Job.objects.create(
            company_id=self.context['company_id'],
            **validated_data
        )
        return instance

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'work_days', 'work_hours', 'salary', 'payment_frequency', 'added', 'expire']


class JobEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'work_days', 'work_hours', 'salary', 'payment_frequency', 'expire']


class SimpleCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanySerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'manager', 'info']


class CompanyCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Company.objects.create(
            manager_id=self.context['user_id'],
            **validated_data
        )

    class Meta:
        model = Company
        fields = ['name', 'info']


class CompanyEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'info']


class SimpleEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['user', 'address']


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['user', 'about', 'email', 'phone', 'address']


class SimpleApplicationSerializer(serializers.ModelSerializer):
    applicant = SimpleEmployeeSerializer()

    class Meta:
        model = Application
        fields = ['id', 'applicant']


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = EmployeeSerializer()

    class Meta:
        model = Application
        fields = ['id', 'applicant', 'request_text', 'resume', 'applied_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        instance = Application.objects.create(
            applicant_id=self.context['applicant_id'],
            job_id=self.context['job_id'],
            **validated_data
        )
        return instance
        
    class Meta:
        model = Application
        fields = ['request_text', 'resume']


class EmptySerializer(serializers.Serializer):
    pass
