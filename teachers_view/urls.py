from django.urls import path
from .views import hello, edit_lesson, login_page, settings_page, students

urlpatterns = [
    path('', hello),
    path('edit_lesson/', edit_lesson),
    path('dashboard/', hello, name='dashboard'),
    path('lessons/', edit_lesson, name='lessons'),
    path('students/', students, name='students'),
    path('settings/', settings_page, name='settings'),
    path('login/', login_page),
]
