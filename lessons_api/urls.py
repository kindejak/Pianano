from django.urls import path
from .views import LessonAPIView, LessonDetailAPIView, QuestionAPIView, register, test_token, students_xp, students_time_spent, students_xp, students_lessons_finished
from rest_framework.authtoken import views

urlpatterns = [
    path('lessons/', LessonAPIView.as_view()),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),
    path('questions/', QuestionAPIView.as_view()),
    path('login/', views.obtain_auth_token),
    path('register/', register),
    path('test-token/', test_token),
    path('students-xp/', students_xp, name='students_xp'),
    path('students-time-spent/', students_time_spent, name='students_time_spent'),
    path('students-lessons-finished/', students_lessons_finished, name='students_lessons_finished')
]