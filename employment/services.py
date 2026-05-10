from rest_framework.exceptions import ValidationError

from .models import Application, Employee, Job
from .serializers import ApplicationCreateSerializer


class ApplicationService:
    
    @staticmethod
    def get_application(*, applicant: Employee, job: Job) -> Application | None:
        application = Application.objects.filter(
            applicant=applicant,
            job=job
        ).first()

        return application

    @staticmethod
    def apply(*, applicant: Employee, job: Job, data) -> Application | None:
        if ApplicationService.get_application(
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
    
    @staticmethod
    def cancel_application(*, applicant: Employee, job: Job) -> None:
        application = ApplicationService.get_application(
            applicant=applicant,
            job=job
        )
        
        if not application:
            raise ValidationError("You have not applied to this job.")
        
        application.delete()
