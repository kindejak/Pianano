from django.contrib import admin

# Register your models here.
from .models import MusicLesson, Question, Student, StudentLesson

admin.site.register(MusicLesson)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(StudentLesson)
