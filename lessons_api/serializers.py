from rest_framework import serializers
from .models import MusicLesson, Question, Student


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLesson
        fields = ('id', 'name', 'slug')

class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicLesson
        fields = ('id', 'name', 'questions', 'xp', 'slug', 'is_public')
        depth = 1
     
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'name','teacher', 'type', 'question_json')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ( 'name', 'user', 'nickname', 'login',  'password_hash')