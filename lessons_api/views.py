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

from .models import MusicLesson, Question, Student, PianoClass, StudentLesson
from django.contrib.auth.models import User
from .serializers import LessonSerializer, LessonDetailSerializer, QuestionSerializer, StudentSerializer
# Create your views here.


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
def update_student_lesson(request):
    # {"time_spent": time_spent, "answerd_questions": answerd_questions, "right_answers": right_answers, "is_finished": 1,"date_finished":date_finished,"time_finished":time_finished}, headers={"Content-Type": "application/json"})
    # get student
    user = request.user
    if not Student.objects.filter(user=user).exists():
        return Response({'error':'User is not a student'})
    student = Student.objects.get(user=user)
    # get lesson
    slug = request.data.get('slug')
    try:
        print(slug)
        lesson = MusicLesson.objects.get(slug=slug)
    except:
        return Response({'error':'Lesson not found'}, status=404)
    # get student lesson
    if StudentLesson.objects.filter(student=student, music_lesson=lesson).first() is None:
        #create student lesson
        student_lesson = StudentLesson.objects.create(student=student, music_lesson=lesson)
    else:
        student_lesson = StudentLesson.objects.get(student=student, music_lesson=lesson)
    # update student lesson

    student_lesson.time_spent = request.data.get('time_spent')
    student_lesson.answerd_questions = request.data.get('answerd_questions')
    student_lesson.right_answers = request.data.get('right_answers')
    student_lesson.is_finished = request.data.get('is_finished')
    datetime = request.data.get('date_finished') + ' ' + request.data.get('time_finished')
    student_lesson.datetime_finished = datetime

    student_lesson.save()
    # update student xp
    if student_lesson.is_finished:
        student.xp += lesson.xp
        student.save()
    return Response({'message':'Student lesson updated'})


   

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

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
class LessonAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    quearyset = None

    def get(self, request):
        print(request.user)
        print(request.headers)
        data = MusicLesson.objects.filter(is_public=True)
        if request.user.is_authenticated and Student.objects.filter(user=request.user).exists():
            student = Student.objects.get(user=request.user)
            print(student)
            classes = PianoClass.objects.filter(students = student)
            for c in classes:
                data = data | c.lessons.all()
            self.queryset = data
            return super().get(request)
        else:
            # return only public lessons
            self.queryset = data
            return super().get(request)

@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = MusicLesson.objects.all()
    serializer_class = LessonDetailSerializer
    # TODO: add permission to only allow students to see lessons that belong to their teacher

    def get(self, request, pk):
        lesson = get_object_or_404(MusicLesson, pk=pk)
        if lesson.is_public:
            return super().get(request, pk)
        else:
            student = Student.objects.get(user=request.user)
            classes = PianoClass.objects.filter(students = student)
            for c in classes:
                if lesson in c.lessons.all():
                    return super().get(request, pk)
            return Response({'error':'Lesson not found'})
    




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
def get_students_lessons_finished(request):
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
