from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from .models import MusicLesson, Question, Student
from .serializers import LessonSerializer, LessonDetailSerializer, QuestionSerializer, StudentSerializer
# Create your views here.


@api_view(['POST'])
def login(request):
    student = get_object_or_404(Student, login=request.data['login'])
    if not check_password(request.data['password'], student.password_hash):
        return Response({'message':'Not found'})
    return Response({'message':'login'})

@api_view(['POST'])
def register(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        #change password to password_hash
        serializer.validated_data['password_hash'] = make_password(serializer.validated_data['password_hash'])
        serializer.save()
        student = Student.objects.get(login=request.data['login'])
        token = "1234"#token = Token.objects.create(user=student)
        return Response({'token':str(token),'user':serializer.data})
    print(serializer.errors)
    return Response({'message':'Not valid'})

@api_view(['POST'])
def test_token(request):
    return Response({'message':'test_token'})

class LessonAPIView(generics.ListAPIView):
    queryset = MusicLesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = MusicLesson.objects.all()
    serializer_class = LessonDetailSerializer

class QuestionAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer