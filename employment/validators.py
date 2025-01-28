from django.core.exceptions import ValidationError
import magic


def validate_file_size(file):
    max_size_kb = 2048

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger that {max_size_kb}KB!')
    

def validate_file_content(file):
    allowed_mime_types = ['application/pdf']

    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in allowed_mime_types:
        raise ValidationError("Invalid file type. Only PDF files are allowed.")
    