from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.
# token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar_id = models.IntegerField(default=0)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    streak = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)

    def __str__(self):
        if self.user:
            return self.user.username
        return 'None'
  
class Question(models.Model):
    QUESTION_TYPES = [
        ('NI','Note idetification'),
        ('CI','Chord idetification'),
        ('PN', 'Play note'),
        ('PC', 'Play chord')
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
    date_finished = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.music_lesson.name} - {self.music_lesson.teacher.username}'