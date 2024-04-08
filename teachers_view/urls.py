from django.urls import path
from .views import hello, login_page
from .views import edit_lesson, lesson, create_lesson, delete_lesson
from .views import students, create_student
from .views import settings_page, delete_account

urlpatterns = [
    path('', hello),
    path('dashboard/', hello, name='dashboard'),
    path('lessons/', lesson, name='lessons'),
    path('lessons/<int:id>/edit/', create_lesson),
    path('lessons/<int:id>/delete/', delete_lesson),
    path('lessons/edit/', edit_lesson),
    path('lessons/create/', create_lesson, name='create_lesson'),
    path('students/', students, name='students'),
    path('students/create/', create_student, name='create_student'),
    path('settings/', settings_page, name='settings'),
    path('settings/delete/', delete_account, name='delete_account'),
    path('login/', login_page, name='login-page'),
]
