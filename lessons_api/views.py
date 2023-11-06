from django.shortcuts import render

from rest_framework import generics

from .models import MusicLesson, Question
from .serializers import LessonSerializer, LessonDetailSerializer, QuestionSerializer
# Create your views here.

class LessonAPIView(generics.ListAPIView):
    queryset = MusicLesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = MusicLesson.objects.all()
    serializer_class = LessonDetailSerializer

class QuestionAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer