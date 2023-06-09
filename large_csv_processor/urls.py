"""
    API setup, routes and url patterns.
"""
from django.contrib import admin
from django.urls import path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from ninja import UploadedFile, File, NinjaAPI
from celery.result import AsyncResult
from .tasks import process_csv_task

api = NinjaAPI(
    title='CSV Processing',
    version="0.1.0",
)

@api.post('/process_csv')
def schedule_processing(request, input_file: UploadedFile = File(...)):
    """
        Input: CSV file upload
        Output: ID of the processing task
    """
    file = input_file
    file_sys = FileSystemStorage()
    filename = file_sys.save(file.name, file)

    task_id = process_csv_task.delay(filename)

    return {'task_id': str(task_id)}

@api.get('/download_csv/{task_id}')
def download_csv(request, task_id):
    """
        Input: task_id
        Return: resulting CSV if processing is done
    """
    result = AsyncResult(task_id)
    if result.ready():
        file_path = result.get()
        with open(file_path, 'rb') as csv:
            response = HttpResponse(csv.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=processed'
            return response
    else:
        return {'status': 'processing'}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
