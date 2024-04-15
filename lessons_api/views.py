import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import MusicLesson, Question, Student
from django.contrib.auth.models import User
from .serializers import LessonSerializer, LessonDetailSerializer, QuestionSerializer, StudentSerializer
# Create your views here.


@api_view(['POST'])
def update_student_lesson(request):
    # {"time_spent": time_spent, "answerd_questions": answerd_questions, "right_answers": right_answers, "is_finished": 1,"date_finished":date_finished,"time_finished":time_finished}, headers={"Content-Type": "application/json"})
    # get student
    user = request.user
    student = Student.objects.get(user=user)
    # get lesson
    lesson_id = request.data.get('lesson_id')
    lesson = MusicLesson.objects.get(id=lesson_id)
    # get student lesson
    student_lesson = student.studentlesson_set.get(music_lesson=lesson)
    # update student lesson
    student_lesson.time_spent = request.data.get('time_spent')
    student_lesson.answerd_questions = request.data.get('answerd_questions')
    student_lesson.right_answers = request.data.get('right_answers')
    student_lesson.is_finished = request.data.get('is_finished')
    student_lesson.date_finished = request.data.get('date_finished')
    student_lesson.time_finished = request.data.get('time_finished')


   

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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def students_time_spent(request):
    # get all that belong to the teacher
    teacher = request.user
    students = Student.objects.filter(teacher=teacher)
    student_time = []
    for student in students:
        lessons = student.studentlesson_set.all()
        time_spent = 0
        for lesson in lessons:
            time_spent += lesson.time_spent
        student_time.append({'student':student.user.username, 'time_spent':time_spent})
    # return json with students and time spent
    return Response(student_time)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def students_xp(request):
    # get all that belong to the teacher
    teacher = request.user
    students = Student.objects.filter(teacher=teacher)
    if students.count() == 0:
        return Response([])
    # return json with students and xp
    xp = []
    for student in students:
        # get all lessons that the student has finished
        lessons = student.studentlesson_set.filter(is_finished=True)
        xp_student = 0
        for lesson in lessons:
            xp_student += lesson.music_lesson.xp
        student.xp = xp_student
        student.save()
        xp.append({'student':student.user.username, 'xp':student.xp})
    return Response(xp)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def students_lessons_finished(request):
    # get all that belong to the teacher
    teacher = request.user
    students = Student.objects.filter(teacher=teacher)
    # return json with students and xp
    if students.count() == 0:
        return Response([])
    lessons = []
    for student in students:
        lessons_finished = student.studentlesson_set.filter(is_finished=True).count()
        lessons.append({'student':student.user.username, 'lessons_finished':lessons_finished})
    return Response(lessons)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])      
def get_self(request):
    user = request.user
    student = Student.objects.get(user=user)
    return Response({'username':user.username, 'email':user.email, 'xp':student.xp, 'streak':student.streak})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  
def get_students(request):
    teacher = request.user
    students = Student.objects.filter(teacher=teacher)
    if students.count() == 0:
        return Response([])
    student_array = []
    for student in students:
        student_array.append({'username':student.user.username, 'email':student.user.email, 'xp':student.xp, 'streak':student.streak})
    return Response(student_array)
