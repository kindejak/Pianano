
from django.shortcuts import render

from django.views import View

from  .forms import CreateLessonForm, LoginForm, SettingsForm

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from lessons_api.models import StudentLesson, Student
from django.contrib.auth.models import User


@login_required(login_url="/teacher/login/")
def hello(request):
    context = {}
    # get last 5 studentlessons that were finished and belong to the teacher
    students = Student.objects.filter(teacher=request.user)
    student_lessons = []
    for student in students:
        student_lessons += student.studentlesson_set.filter(is_finished=True).order_by('-date_finished')
    # sort by date_finished
    student_lessons = sorted(student_lessons, key=lambda x: x.date_finished, reverse=True)
    student_lessons = student_lessons[:5]
    context_lessons = []
    for student_lesson in student_lessons:
        student = student_lesson.student
        context_lessons.append({
            'student': student.user.username,
            'avatar_id': student.avatar_id,
            'time_spent': student_lesson.time_spent,
            'finished': student_lesson.date_finished,
        })
    context['student_lessons'] = context_lessons
    print(context)
    return render(request, 'dashboard.html', context)


@login_required(login_url="/teacher/login/")
def students(request):
    return render(request, 'students.html')

@login_required(login_url="/teacher/login/")
def edit_lesson(request):
    form = CreateLessonForm()

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base.html')
    
    context = {'form': form}
    return render(request, 'edit_lesson.html', context)

@login_required(login_url="/teacher/login/")
def create_lesson(request):
    form = CreateLessonForm()

    if request.method == 'POST':
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base.html')
    
    context = {'form': form}
    return render(request, 'create_lesson.html', context)

@login_required(login_url="/teacher/login/")
def settings_page(request):
    if request.method == 'POST':
        user = request.user
        form = SettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.info(request, "Settings updated successfully")
            return render(request, 'settings.html', {'form': form})
    else:
        user = request.user
        form = SettingsForm(instance=user)
        return render(request, 'settings.html', {'form': form})



def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'dashboard.html')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    return render(request, 'login.html', {'form': form})

            

