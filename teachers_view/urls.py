from django.urls import path
from .views import createStudentForm

urlpatterns = [
    path('create_student.html', createStudentForm.as_view(), name='create_student'),
]