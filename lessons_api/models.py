from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50, unique=True)
    login = models.CharField(max_length=50, unique=True, blank=True)
    password_hash = models.CharField(max_length=40, blank=True) # sha1
    xp = models.IntegerField(default=0)

  
class Question(models.Model):
    QUESTION_TYPES = [
        ('NI','Note idetification')
    ]
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=QUESTION_TYPES)
    question_json = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.type} - {self.teacher.username}'


class MusicLesson(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    xp = models.IntegerField()
    slug = models.SlugField(max_length=40,null=True,unique=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.teacher.username}'
    
class PianoClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
    lessons = models.ManyToManyField(MusicLesson)

    def __str__(self):
        return f'{self.name} - {self.teacher.username}'
    
class StudentLesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(PianoClass, on_delete=models.CASCADE, null=True)
    music_lesson = models.ForeignKey(MusicLesson, on_delete=models.CASCADE)
    time_spent = models.IntegerField(default=0)
    answerd_questions = models.IntegerField(default=0)
    right_answers = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.student.nickname} - {self.music_lesson.name} - {self.music_lesson.teacher.username}'