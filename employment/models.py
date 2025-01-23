from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ACCOUNT_TYPE_CHOICES = {
        'employer': 'Employer',
        'employee': 'Employee'
    }

    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE_CHOICES)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    joined_in = models.DateField(auto_now_add=True)
    # resume = models.FileField(upload_to='employment/resumes', null=True, blank=True)

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
    added = models.DateField(auto_now_add=True)
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

# CURRENCY_CHOICES = {
#     'USD': 'US Dollar',
#     'EUR': 'Euro',
#     'SYP': 'Syrian pound'
# }