from lessons_api.models import MusicLesson, Question, Student
from django.contrib.auth.models import User
from django import forms


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'type', 'question_json']


class CreateLessonForm(forms.ModelForm):    
    class Meta:
        model = MusicLesson
        questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all())
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

class CreateClassForm(forms.Form):
    name = forms.CharField()
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
    lessons = forms.ModelMultipleChoiceField(queryset=MusicLesson.objects.all())

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    