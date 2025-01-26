from rest_framework import serializers

from .models import Company, Job


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


class EmptySerializer(serializers.Serializer):
    pass
