from lessons_api.models import MusicLesson, Question, Student
from django.contrib.auth.models import User
from django import forms

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = MusicLesson
        fields = ['name', 'questions', 'xp', 'is_public']

class CreateStudentForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    avatar_id = forms.IntegerField()


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    