from django.urls import path
from .views import LessonAPIView, LessonDetailAPIView, QuestionAPIView, register, test_token
from rest_framework.authtoken import views

urlpatterns = [
    path('lessons/', LessonAPIView.as_view()),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),
    path('questions/', QuestionAPIView.as_view()),
    path('login/', views.obtain_auth_token),
    path('register/', register),
    path('test_token/', test_token),
]