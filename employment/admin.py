from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .models import Address, Company, Employee, Employer, Job, User


class EmployerInline(admin.StackedInline):
    model = Employer


class EmployeeInline(admin.StackedInline):
    model = Employee


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_filter = BaseUserAdmin.list_filter + ('account_type',)
    list_per_page = 20
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('account_type',)
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name", "account_type"),
            },
        ),
    )

    def get_inlines(self, request, obj):
        if obj:
            if obj.account_type == 'employee':
                return [EmployeeInline]
            elif obj.account_type == 'employer':
                return [EmployerInline]
        return []


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    search_fields = ['title']
    list_display = ['title', 'company', 'salary']
    list_per_page = 20
    ordering = ['added']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_per_page = 20
    ordering = ['name']