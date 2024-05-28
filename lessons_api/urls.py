from django.urls import path
from .views import LessonAPIView, LessonDetailAPIView, QuestionAPIView
from .views import register, test_token, students_xp, students_time_spent, students_xp, get_students_lessons_finished, get_self, get_students, update_student_lesson
from rest_framework.authtoken import views

urlpatterns = [
    path('lessons/', LessonAPIView.as_view()),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),
    path('questions/', QuestionAPIView.as_view()),
    path('login/', views.obtain_auth_token),
    path('self/', get_self),
    path('register/', register),
    path('test-token/', test_token),
    path('students-xp/', students_xp, name='students_xp'),
    path('students-time-spent/', students_time_spent, name='students_time_spent'),
    path('students-lessons-finished/', get_students_lessons_finished, name='students_lessons_finished'),
    path('students-from-teacher/', get_students, name='students_from_teacher'),
    path('update-student-lesson/',update_student_lesson)
]