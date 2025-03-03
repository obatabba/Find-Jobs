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


class EmployeeEditSerializer(serializers.ModelSerializer): # edit user's employee profile
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    expertise = serializers.CharField(required=False)
    address = AddressSerializer(required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'profile_picture', 'email', 'expertise', 'about', 'phone', 'birth_date', 'address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        address_data = validated_data.pop('address', None)
        if address_data:
            address, _ = Address.objects.get_or_create(employee=instance)
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
            instance.address = address
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
        fields = ['id', 'name', 'logo']


class CompanySerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField(read_only=True)

    def create(self, validated_data):
        return Company.objects.create(
            manager_id=self.context['employer_id'],
            **validated_data
        )

    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'manager', 'info']


class PublicSimpleEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['id', 'user', 'profile_picture', 'expertise']


class PublicEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ['user', 'profile_picture', 'expertise', 'about']


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
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', required=False)
    companies = SimpleCompanySerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return super().update(instance, validated_data)

    class Meta:
        model = Employer
        fields = ['first_name', 'last_name','about', 'email',  'phone', 'companies']
