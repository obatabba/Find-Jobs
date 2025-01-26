from rest_framework_nested import routers
from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter
from .import views


router = DefaultRouter()
router.register('jobs', views.JobViewSet)
router.register('companies', views.CompanyViewSet)

companies_router = NestedDefaultRouter(router, 'companies', lookup='company')
companies_router.register('jobs', views.NestedJobViewSet, basename='company-jobs')

nested_jobs_router = NestedDefaultRouter(companies_router, 'jobs', lookup='job')
nested_jobs_router.register('applicants', views.ApplicantsViewSet, basename='job-applicants')

urlpatterns = router.urls + companies_router.urls + nested_jobs_router.urls