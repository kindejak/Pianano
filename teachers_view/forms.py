from lessons_api.models import Student
from django import forms

"""
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'nickname', 'login', 'password_hash']
        widgets = {
            'password_hash': forms.PasswordInput(),
        }

    def __str__(self):
        return self.nickname
"""