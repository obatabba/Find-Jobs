from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import Application, Company, Employee, Employer, Job, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street']


class UserSerializer(BaseUserSerializer):
    account_type = serializers.CharField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account_type']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'account_type']


class EmployeeUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    address = AddressSerializer()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'expertise', 'about', 'phone', 'birth_date', 'address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UserSerializer(instance.user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        address_data = validated_data.pop('address', {})
        if not instance.address:
            address_serializer = AddressSerializer(data=address_data)
        else:
            address_serializer = AddressSerializer(instance.address, data=address_data)
        address_serializer.is_valid(raise_exception=True)
        instance.address = address_serializer.save()
        return super().update(instance, validated_data)


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


class PublicSimpleEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'expertise']


class PublicEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['user', 'expertise', 'about']


class SimpleEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'expertise', 'address']


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    address = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['user', 'expertise', 'about', 'email', 'phone', 'address']


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


class SimpleEmployerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Employer
        fields = ['id', 'user']


class EmployerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    companies = SimpleCompanySerializer(many=True)

    class Meta:
        model = Employer
        fields = ['first_name', 'last_name','about', 'email',  'phone', 'companies']
