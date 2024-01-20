from django.urls import path
from .views import LessonAPIView, LessonDetailAPIView, QuestionAPIView, login, register, test_token

urlpatterns = [
    path('lessons/', LessonAPIView.as_view()),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),
    path('questions/', QuestionAPIView.as_view()),
    path('login/', login),
    path('register/', register),
    path('test_token/', test_token),
]