from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_file_content, validate_file_size


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = {
        'employer': 'Employer',
        'employee': 'Employee'
    }

    email = models.EmailField(unique=True, blank=True)
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE_CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def is_employee(self):
        return self.account_type == 'employee'
    
    @property
    def is_employer(self):
        return self.account_type == 'employer'


class Address(models.Model):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.street} - {self.city}, {self.country}'


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Company(models.Model):
    manager = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='companies')
    name = models.CharField(max_length=255, unique=True)
    info =models.TextField()

    def __str__(self):
        return self.name
    

class Job(models.Model):
    PAYMENT_FREQUENCY_CHOICES = {
        'H': 'Hourly',
        'D': 'Daily',
        'W': 'Weekly',
        'M': 'Monthly'
    }

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    work_days = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    work_hours = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(24)]
    )
    added = models.DateField(auto_now_add=True, null=True)
    expire = models.DateField(null=True, blank=True)
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal(1))]
    )
    payment_frequency = models.CharField(max_length=1, choices=PAYMENT_FREQUENCY_CHOICES,default='M')

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joined_in = models.DateField(auto_now_add=True)
    applied_jobs = models.ManyToManyField(Job, through='Application', blank=True, related_name='applicants')
    # resume = models.FileField(upload_to='employment/resumes', null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def email(self):
        return self.user.email


class Application(models.Model):
    applicant = models.ForeignKey(Employee, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    request_text = models.TextField()
    resume = models.FileField(
        upload_to='employment/resumes',
        validators=[validate_file_size, validate_file_content]
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'job'], name='unique-application')
        ]
