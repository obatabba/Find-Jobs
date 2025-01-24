from rest_framework import serializers

from .models import Company, Job


class JobListSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Job
        fields = ['id', 'title', 'company']


class JobDetailSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'work_days', 'work_hours', 'salary', 'payment_frequency', 'added', 'expire']


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanyDetailSerializer(serializers.ModelSerializer):
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
