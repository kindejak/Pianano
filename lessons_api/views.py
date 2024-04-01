from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from .models import MusicLesson, Question, Student
from django.contrib.auth.models import User
from .serializers import LessonSerializer, LessonDetailSerializer, QuestionSerializer, StudentSerializer
# Create your views here.


   

@api_view(['POST'])
def register(request):
    # get username and password from request
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    # check if username is already taken
    if User.objects.filter(username=username).exists():
        return Response({'error':'Username already taken'})
    try:
        validate_email(email)
    except:
        return Response({'error':'Invalid email'})
    if User.objects.filter(email=email).exists():
        return Response({'error':'Email already used'})
    try:
        validate_password(password)
    except:
        return Response({'error':'Password is too weak'})
    # create user
    user = User.objects.create(username=username, password=make_password(password), email=email)
    # create student
    student = Student.objects.create(user=user)
    # get token
    token = Token.objects.get(user=user)
    return Response({'token':token.key})
    
    
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