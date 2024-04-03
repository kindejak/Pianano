from lessons_api.models import MusicLesson, Question, Student
from django.contrib.auth.models import User
from django import forms

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = MusicLesson
        fields = ['name', 'questions', 'xp', 'is_public']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    