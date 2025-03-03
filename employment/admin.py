from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db.models import Count
from django.forms import ModelMultipleChoiceField
from django.utils.timezone import localdate
from django.utils.html import format_html

from admin_extend.extend import add_bidirectional_m2m, extend_registered, registered_form
from .models import Company, Employee, Employer, Job, User


class CompanyInline(admin.TabularInline):
    model = Company
    extra = 0


class EmployerInline(admin.StackedInline):
    model = Employer
    show_change_link = True


class EmployeeInline(admin.StackedInline):
    model = Employee


class JobInline(admin.StackedInline):
    model = Job
    extra = 0
    exclude = ['applicants']


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


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    model = Employer
    inlines = [CompanyInline]
    list_display = ['user__first_name', 'user__last_name', 'companies_count']
    list_per_page = 20
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name', 'user__last_name']

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .annotate(companies_count=Count('companies'))

    @admin.display(ordering='companies_count')
    def companies_count(self, employer):
        return employer.companies_count


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['user__first_name', 'user__last_name']
    list_per_page = 20
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name', 'user__last_name']
    readonly_fields = ['profile_pic']

    def profile_pic(self, instance):
        return format_html(f'<img src="{instance.profile_picture.url}" class="thumbnail">')
    
    class Media:
        css = {
            'all': ['employment/styles.css']
        }


@extend_registered
class ExtendedSiteAdminForm(add_bidirectional_m2m(registered_form(Employee))):

    applied_jobs = ModelMultipleChoiceField(
        queryset=Job.objects.all(),
        widget=FilteredSelectMultiple('Jobs', False),
        required=False
    )

    def _get_bidirectional_m2m_fields(self):
        return super(ExtendedSiteAdminForm, self).\
            _get_bidirectional_m2m_fields() + [('applied_jobs', 'applied_jobs')]


class JobFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'expire'

    def lookups(self, request, model_admin):
        return [
            ('<now', 'expired'),
            ('>now', 'available')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<now':
            return queryset.filter(expire__lt=localdate())
        if self.value() == '>now':
            return queryset.filter(expire__gte=localdate())


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    search_fields = ['title']
    list_display = ['title', 'company', 'salary', 'expire']
    list_per_page = 20
    ordering = ['added']
    list_filter = [JobFilter]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'manager']
    inlines = [JobInline]
    list_display = ['name', 'manager', 'jobs_count']
    list_per_page = 20
    ordering = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .annotate(jobs_count=Count('jobs'))

    @admin.display(ordering='jobs_count')
    def jobs_count(self, company):
        return company.jobs_count
