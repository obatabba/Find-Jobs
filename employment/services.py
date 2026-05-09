from rest_framework.exceptions import ValidationError

from .models import Application, Employee, Job
from .serializers import ApplicationCreateSerializer


class ApplicationService:
    
    @staticmethod
    def check_application_existence(*, applicant: Employee, job: Job) -> bool:
        return Application.objects.filter(
            applicant=applicant,
            job=job
        ).exists()

    @staticmethod
    def apply(*, applicant: Employee, job: Job, data):
        if ApplicationService.check_application_existence(
            applicant=applicant,
            job=job
        ):
            raise ValidationError("You have already applied to this job")
    
        serializer = ApplicationCreateSerializer(data=data, context={'applicant': applicant, 'job': job})
        serializer.is_valid(raise_exception=True)
        
        application = Application.objects.create(
            applicant = applicant,
            job = job,
            **serializer.validated_data
        )

        return application